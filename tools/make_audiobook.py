"""Build the audiobook editions of 200 Meters and Down with edge-tts.

Reads chapters/ch00.md .. ch09.md, prepares each for narration, synthesizes in
chunks with retries, and stitches per-chapter MP3s (tagged) into audiobook/.

Eight voices in four accents are supported. The default voice (Ryan, British
male) writes `chNN.mp3`; every other voice writes `<key>-chNN.mp3`, so all
editions share one folder and one release.

Usage:
  python tools/make_audiobook.py                 # default voice (ryan)
  python tools/make_audiobook.py --voice andrew  # one voice
  python tools/make_audiobook.py --all           # every voice
  python tools/make_audiobook.py --voice ava --chapters 0-4   # a subset
  python tools/make_audiobook.py --voice ryan --test          # short sample

Cross-platform: needs edge-tts (pip install edge-tts) and ffmpeg on PATH.
Resumable: a chapter whose MP3 already exists (> 100 KB) is skipped unless
--force is given.
"""

import argparse
import asyncio
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import edge_tts

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from tools import figreg
from tools.narration import NUMBER_WORDS, speak_figures, speak_math, strip_markup

REPO = Path(__file__).resolve().parent.parent
CHAPTERS = REPO / "chapters"
OUT = REPO / "audiobook"

# key -> (edge-tts voice, display name, accent, gender)
VOICES = {
    "ryan":    ("en-GB-RyanNeural",              "Ryan",    "British",    "Male"),
    "sonia":   ("en-GB-SoniaNeural",             "Sonia",   "British",    "Female"),
    "andrew":  ("en-US-AndrewNeural",            "Andrew",  "US",         "Male"),
    "ava":     ("en-US-AvaNeural",               "Ava",     "US",         "Female"),
    "william": ("en-AU-WilliamMultilingualNeural", "William", "Australian", "Male"),
    "natasha": ("en-AU-NatashaNeural",           "Natasha", "Australian", "Female"),
    "connor":  ("en-IE-ConnorNeural",            "Connor",  "Irish",      "Male"),
    "emily":   ("en-IE-EmilyNeural",             "Emily",   "Irish",      "Female"),
}
DEFAULT_VOICE = "ryan"

CHUNK_CHARS = 3500
RETRIES = 6

# Numbered-chapter heading, e.g. "1. The Spark Era (1900–1917)".
_CHAPTER_RE = re.compile(r"^(\d+)\.\s*(.+?)\s*\(([^)]+)\)$")
# Prologue/epilogue heading, e.g. "Prologue — Before the Amateurs (1864–1900)".
_PROLOGUE_RE = re.compile(r"^(Prologue|Epilogue)\s*—\s*(.+?)\s*\(([^)]+)\)$")


def spoken_heading(raw: str) -> str:
    m = _CHAPTER_RE.match(raw)
    if m:
        num = NUMBER_WORDS[int(m.group(1))]
        span = m.group(3).replace("–", " to ")
        return f"Chapter {num}. {m.group(2)}. {span}."
    m = _PROLOGUE_RE.match(raw)
    if m:
        span = m.group(3).replace("–", " to ")
        return f"{m.group(1)}. {m.group(2)}. {span}."
    return raw


def prepare_text(body: str, fig_desc: dict) -> str:
    """Turn a chapter body (markdown-ish) into narration-ready plain text.

    ``fig_desc`` maps figure id -> (number, description), as loaded from the
    figure registry. Scene rules (``***``) become paragraph breaks, ``### ``
    subheads are dropped to plain lines, ``$...$`` math and ``{{fig:ID}}``
    refs are spoken, and any leftover emphasis/heading/blockquote markup is
    stripped.
    """
    lines = body.replace("\r\n", "\n").split("\n")
    out = []
    for ln in lines:
        s = ln.strip()
        if s and re.fullmatch(r"[\*\s]+", s):
            out.append("")  # scene break -> paragraph pause
            continue
        s = speak_math(s)
        s = speak_figures(s, fig_desc)
        s = strip_markup(s)
        out.append(s)
    return re.sub(r"\n{3,}", "\n\n", "\n".join(out)).strip()


def prepare(path: Path, n: int) -> tuple[str, str]:
    """Return (spoken title, narration text) for one chapter file."""
    raw = path.read_text(encoding="utf-8").replace("\r\n", "\n").strip()
    lines = raw.split("\n")
    heading = re.sub(r"^##\s+", "", lines[0]).strip()
    title = spoken_heading(heading)

    reg = figreg.load()
    fig_desc = {
        fig_id: (entry.get("number", ""), entry.get("spoken") or entry.get("caption", ""))
        for fig_id, entry in reg.items()
    }

    body = "\n".join(lines[1:])
    text = prepare_text(body, fig_desc)

    intro = title
    if n == 0:
        intro = "200 Meters and Down. A Technical History of Amateur Radio.\n\n" + intro
    return title, intro + "\n\n" + text


def chunks(text: str) -> list[str]:
    out, cur, size = [], [], 0
    for para in text.split("\n\n"):
        if size + len(para) > CHUNK_CHARS and cur:
            out.append("\n\n".join(cur))
            cur, size = [], 0
        cur.append(para)
        size += len(para) + 2
    if cur:
        out.append("\n\n".join(cur))
    return out


def dest_name(voice_key: str, n: int) -> str:
    stem = f"ch{n:02d}"
    return f"{stem}.mp3" if voice_key == DEFAULT_VOICE else f"{voice_key}-{stem}.mp3"


async def synth_chunk(text: str, voice: str, dest: Path) -> None:
    last = None
    for attempt in range(1, RETRIES + 1):
        try:
            await edge_tts.Communicate(text, voice).save(str(dest))
            if dest.stat().st_size > 500:
                return
            raise RuntimeError("empty audio")
        except Exception as e:  # noqa: BLE001 - retry any transport error
            last = e
            await asyncio.sleep(min(2 * attempt, 12))
    raise RuntimeError(f"chunk failed after {RETRIES} tries: {last}")


def stitch(parts: list[Path], dest: Path, title: str, track: int, label: str,
           accent: str, gender: str) -> None:
    lst = parts[0].parent / f"{dest.stem}.txt"
    lst.write_text("".join(f"file '{p.as_posix()}'\n" for p in parts), encoding="utf-8")
    subprocess.run(
        [
            "ffmpeg", "-y", "-loglevel", "error",
            "-f", "concat", "-safe", "0", "-i", str(lst),
            "-c", "copy",
            "-metadata", f"title={title.rstrip('.')}",
            "-metadata", "artist=Claude Opus 4.8",
            "-metadata", "album=200 Meters and Down",
            "-metadata", f"track={track}/10",
            "-metadata", "genre=Audiobook",
            "-metadata", "date=2026",
            "-metadata", f"composer={label}",
            "-metadata", f"comment=Read by {label} ({accent} {gender})",
            str(dest),
        ],
        check=True,
    )
    lst.unlink(missing_ok=True)


async def build_chapter(n: int, voice_key: str, sem: asyncio.Semaphore,
                        parts_dir: Path, force: bool) -> str:
    voice, label, accent, gender = VOICES[voice_key]
    dest = OUT / dest_name(voice_key, n)
    if not force and dest.exists() and dest.stat().st_size > 100_000:
        return f"skip  {dest.name} (exists)"
    async with sem:
        src = CHAPTERS / f"ch{n:02d}.md"
        title, text = prepare(src, n)
        parts = []
        for i, ck in enumerate(chunks(text)):
            part = parts_dir / f"{voice_key}_{n:02d}_{i:03d}.mp3"
            await synth_chunk(ck, voice, part)
            parts.append(part)
        await asyncio.to_thread(stitch, parts, dest, title, n + 1, label, accent, gender)
        for p in parts:
            p.unlink(missing_ok=True)
    return f"done  {dest.name} ({dest.stat().st_size/1e6:.1f} MB) — {label}"


async def build_voice(voice_key: str, nums: list[int], concurrency: int,
                      force: bool) -> list[str]:
    sem = asyncio.Semaphore(concurrency)
    parts_dir = Path(tempfile.mkdtemp(prefix=f"tts_{voice_key}_"))
    try:
        results = await asyncio.gather(
            *(build_chapter(n, voice_key, sem, parts_dir, force) for n in nums),
            return_exceptions=True,
        )
    finally:
        shutil.rmtree(parts_dir, ignore_errors=True)
    lines, failed = [], []
    for n, r in zip(nums, results):
        if isinstance(r, Exception):
            failed.append(f"{voice_key} ch{n:02d}: {r}")
        else:
            lines.append(r)
    for line in lines:
        print(line, flush=True)
    if failed:
        print("FAILED:\n" + "\n".join(failed), flush=True)
    return failed


def parse_chapters(spec: str) -> list[int]:
    if not spec:
        return list(range(10))
    out: list[int] = []
    for part in spec.split(","):
        if "-" in part:
            a, b = part.split("-")
            out.extend(range(int(a), int(b) + 1))
        else:
            out.append(int(part))
    return [n for n in out if 0 <= n <= 9]


async def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--voice", choices=list(VOICES), default=DEFAULT_VOICE)
    ap.add_argument("--all", action="store_true", help="build every voice")
    ap.add_argument("--chapters", default="", help="e.g. 0-4 or 0,8,9")
    ap.add_argument("--concurrency", type=int, default=3)
    ap.add_argument("--force", action="store_true", help="rebuild existing files")
    ap.add_argument("--test", action="store_true", help="one short sample only")
    args = ap.parse_args()

    OUT.mkdir(exist_ok=True)

    if args.test:
        _, text = prepare(CHAPTERS / "ch00.md", 0)
        sample = "\n\n".join(text.split("\n\n")[:3])
        voice = VOICES[args.voice][0]
        dest = OUT / f"sample-{args.voice}.mp3"
        await synth_chunk(sample, voice, dest)
        print(f"sample OK: {dest} ({dest.stat().st_size} bytes)")
        return

    nums = parse_chapters(args.chapters)
    keys = list(VOICES) if args.all else [args.voice]
    all_failed: list[str] = []
    for key in keys:
        print(f"=== voice {key} ({VOICES[key][1]}, {VOICES[key][2]} {VOICES[key][3]}) "
              f"— {len(nums)} chapters ===", flush=True)
        all_failed += await build_voice(key, nums, args.concurrency, args.force)
    if all_failed:
        print(f"\n{len(all_failed)} chapter(s) failed", flush=True)
        sys.exit(1)
    print("\nALL DONE", flush=True)


if __name__ == "__main__":
    asyncio.run(main())
