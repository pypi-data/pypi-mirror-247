#!/usr/bin/env python3

"""Starts a process and logs file access (later maybe more)"""

# pylint: disable=fixme

import logging
import os
import re
import sys
from argparse import Namespace
from asyncio import CancelledError, StreamReader, create_subprocess_exec, gather, run
from asyncio.subprocess import PIPE
from collections.abc import AsyncIterable, Iterator, Sequence
from contextlib import contextmanager, suppress
from datetime import datetime
from pathlib import Path
from typing import TextIO

import aiofiles
import yaml


def log() -> logging.Logger:
    """Convenience function retrieves 'our' logger"""
    return logging.getLogger("cmk-dev.procmon")


def load_filter_pattern(file_path: str | Path) -> str:
    """Returns the content of the 'exclude' element from given YAML file"""
    with suppress(FileNotFoundError):
        with Path(file_path).expanduser().open(encoding="utf-8") as config_file:
            file_content = yaml.load(config_file, Loader=yaml.BaseLoader)
            return "|".join(
                rf".*{pattern}.*"
                for pattern in (
                    pattern.replace("~", str(Path("~").expanduser()))
                    for pattern in file_content["exclude"]
                )
            )
    return ""


async def extract_paths(
    stream: AsyncIterable[str],
) -> AsyncIterable[tuple[str, str, Path, str, str]]:
    """Traverses `openat` strace lines and yields file access"""
    fds = {}
    async for line in (l.rstrip() async for l in stream):
        if match := re.match(
            r'^(\d*) openat\(([A-Z_]+|\d+), "(.*)",'
            r" ([A-Z_\|]+).*\s=\s((\?|-?\d+)( [A-Z_]+)?( \(.*\))?)$",
            line,
        ):
            log().debug("%s", line)

            pid, location, raw_path_entry, flags, _result, result_nr, *_rest = match.groups()
            if location == "AT_FDCWD" and (pid, location) not in fds:
                fds[(pid, location)] = Path()

            # should be an assertion as soon as using ttrace to parse strace lines
            if (pid, location) not in fds:
                continue

            path = ((df_dir := fds[(pid, location)]) / raw_path_entry).resolve()

            # todo: only if path.is_dir(), but only after ttrace integration
            fds[(pid, result_nr)] = path

            # should be an assertion as soon as using ttrace to parse strace lines
            if not df_dir.is_dir() or not path.exists():
                continue

            yield line, location, path, flags, result_nr

        elif re.match(
            r"^\d* ((<\.\.\. .* resumed>)|(\?\?\?\?\( <unfinished \.\.\.>)|(\+\+\+ )|(\-\-\- )).*$",
            line,
        ):
            pass
        else:
            log().warning("cannot parse: %s", line)


async def process_strace_lines(filename: Path, out_file: TextIO) -> None:
    """For testability: provides content of a file to process_strace()"""
    filter_pattern = load_filter_pattern("~/.config/procmon-exclude.yaml")
    accessed_files = set()
    try:
        async with aiofiles.open(filename) as afp:
            async for line, location, path, flags, _result_nr in extract_paths(afp):
                if not path.is_file():
                    continue
                path_str = path.as_posix()

                out_file.write(f"{path} | {line}\n")
                if not re.match(filter_pattern, path_str):
                    print(f"openat: {location} {flags}: {path}")
                    if path_str not in accessed_files:
                        accessed_files.add(path_str)
    finally:
        for file in sorted(accessed_files):
            print(file.replace(str(Path("~").expanduser()), "~"))


async def buffer_stream(stream: StreamReader, out_file: TextIO) -> None:
    """Records a given stream to a buffer line by line along with the source"""
    while line := (await stream.readline()).decode():
        out_file.write(line)


@contextmanager
def strace_output_path(path: Path | None = None) -> Iterator[Path]:
    """Wraps optional creation of named pipe and sanatizes @path argument"""
    result = path or Path("myfifo")
    result.unlink(missing_ok=True)
    try:
        if path is None:
            os.mkfifo(result, 0o600)
        yield result
    finally:
        if path is None:
            os.unlink(result)


async def main_invoke(cmd: Sequence[str], _args: Namespace) -> None:
    """Runs a program using strace"""
    access_trace_file_path = (
        Path("~").expanduser()
        / f"access-log-{cmd[0]}-{datetime.now().strftime('%Y.%m.%d-%H%M')}.log"
    )
    with open(access_trace_file_path, "w", encoding="utf-8") as outfile:
        print(access_trace_file_path)
        outfile.write(f"{' '.join(cmd)}\n")

        with strace_output_path(None) as strace_output_file_path:
            full_cmd = (
                "strace",
                "--trace=openat",
                "--follow-forks",
                "--columns=0",
                "-o",
                f"{strace_output_file_path}",
                *cmd,
            )
            process = await create_subprocess_exec(*full_cmd, stdout=PIPE, stderr=PIPE)
            assert process.stdout and process.stderr
            try:
                await gather(
                    buffer_stream(process.stdout, sys.stdout),
                    buffer_stream(process.stderr, sys.stderr),
                    process_strace_lines(strace_output_file_path, outfile),
                    process.wait(),
                )
            except (KeyboardInterrupt, CancelledError):
                pass
            finally:
                try:
                    process.terminate()
                except ProcessLookupError:
                    pass
            raise SystemExit(process.returncode)


def main() -> None:
    """Main entrypoint"""
    # args, command = parse_args()
    args: Namespace
    args, command = Namespace(), sys.argv[1:]

    run(main_invoke(command, args))


if __name__ == "__main__":
    main()
