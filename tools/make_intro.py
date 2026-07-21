"""Synthesize the audiobook introduction (audiobook/intro.mp3) with edge-tts.

A short spoken preface that opens the audiobook: what 200 Meters and Down is,
that it was written by Claude Opus 4.8 running in Claude Code, and how to use
the eight-voice edition. Kept separate from the chapter tracks so it can be
regenerated on its own.

Usage:
  python tools/make_intro.py        # writes audiobook/intro.mp3
  python tools/make_intro.py --dry  # print the intro text and exit (no synth, no network)

Requires: edge-tts (pip install edge-tts) and ffmpeg on PATH.
Edit VOICE or INTRO and rerun to change the narration.
"""

import asyncio
import subprocess
import sys
from pathlib import Path

import edge_tts

VOICE = "en-GB-RyanNeural"
OUT = Path(__file__).resolve().parent.parent / "audiobook" / "intro.mp3"

INTRO = """200 Meters and Down: A Technical History of Amateur Radio. An introduction.

This audiobook was written by Claude Opus 4.8 — an artificial intelligence made by Anthropic — running inside the coding tool Claude Code.

The title comes from the Radio Act of 1912, which first licensed amateur radio operators in the United States and confined them to wavelengths of two hundred meters and below — frequencies the engineers of the day considered nearly worthless. Amateurs turned that banishment into a discovery, shortwave propagation, and built from it the hobby and the science this book follows.

What you are about to hear is a technical history of amateur radio, told in ten sections across the eras of the art: from spark-gap transmitters, through the vacuum tube and the superheterodyne receiver, wartime radar and postwar single sideband, the leap to satellites and repeaters, the arrival of the microprocessor and packet radio, and on to today's software-defined radios and digital modes. Each section teaches how that era's technology worked — the circuits, the physics, the engineering — alongside the human story of the people, the clubs, and the regulations that carried the art forward.

This edition is offered in eight voices — American, British, Australian, and Irish, male and female.

And now — 200 Meters and Down. Begin whenever you are ready."""


async def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    raw = OUT.with_suffix(".raw.mp3")
    last = None
    for attempt in range(1, 6):
        try:
            await edge_tts.Communicate(INTRO, VOICE).save(str(raw))
            if raw.stat().st_size > 500:
                break
            raise RuntimeError("empty audio")
        except Exception as e:  # noqa: BLE001 - retry any transport error
            last = e
            await asyncio.sleep(2 * attempt)
    else:
        raise RuntimeError(f"synthesis failed after retries: {last}")

    subprocess.run(
        [
            "ffmpeg", "-y", "-loglevel", "error", "-i", str(raw),
            "-c", "copy",
            "-metadata", "title=Introduction",
            "-metadata", "artist=Claude Opus 4.8",
            "-metadata", "album=200 Meters and Down",
            "-metadata", "track=0/10",
            "-metadata", "genre=Audiobook",
            "-metadata", "date=2026",
            str(OUT),
        ],
        check=True,
    )
    raw.unlink(missing_ok=True)
    print(f"wrote {OUT} ({OUT.stat().st_size} bytes)")


if __name__ == "__main__":
    if "--dry" in sys.argv[1:]:
        print(INTRO)
        sys.exit(0)
    asyncio.run(main())
