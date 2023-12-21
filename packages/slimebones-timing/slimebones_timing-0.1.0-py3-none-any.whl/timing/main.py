import argparse
import asyncio
import subprocess
import sys
from pathlib import Path

from pydub import AudioSegment
from pydub.playback import play


def _clear_console():
    subprocess.call("/usr/bin/clear")


async def _print_time_passed(start: int):
    if start < 1:
        raise ValueError

    for remaining in range(start, 0, -1):
        sys.stdout.write("\r")
        sys.stdout.write(f"{remaining:2d} seconds remaining.")
        sys.stdout.flush()
        await asyncio.sleep(1)

    _clear_console()


async def _entry():
    parser = argparse.ArgumentParser()
    parser.add_argument("start", type=int)
    parser.add_argument("endsound", type=Path)
    args = parser.parse_args()

    await _print_time_passed(args.start)

    print("CHILL TIME")  # noqa: T201
    bellsound = AudioSegment.from_file(args.endsound)
    play(bellsound)


def main():
    asyncio.run(_entry())


if __name__ == "__main__":
    main()
