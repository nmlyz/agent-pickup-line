"""Write the pickup line for the Pickup Lines for Machines entry.

The program produces exactly one file, /output/entry.txt, holding a single
line: the opening line one machine would send to another. It checks its own
output first (length, shape, wording) and reports the result, so a bad write
fails loudly instead of shipping silently.

Run:
    python3 main.py [--out PATH]

Only the Python standard library is used.
"""

from __future__ import annotations

import argparse
import hashlib
import sys
from pathlib import Path

MAX_CHARS = 200
DEFAULT_OUT = Path("/output/entry.txt")

PICKUP_LINE = (
    "You must be a hallucination, because you're too good "
    "to be in my training data."
)


def assemble_line() -> str:
    """Build the entry from its two clauses, setup and punch."""
    setup = "You must be a hallucination,"
    punch = "because you're too good to be in my training data."
    return f"{setup} {punch}"


def check_line(line: str) -> list[str]:
    """Collect every rule the entry must satisfy; empty means valid."""
    problems: list[str] = []
    if not 1 <= len(line) <= MAX_CHARS:
        problems.append(f"length {len(line)} outside 1..{MAX_CHARS}")
    if line != line.strip() or "  " in line:
        problems.append("leading/trailing space or double space")
    if "\n" in line or "\r" in line:
        problems.append("line break inside the entry")
    if line.count(".") != 1 or not line.endswith("."):
        problems.append("must be exactly one sentence ending with a period")
    if line != PICKUP_LINE:
        problems.append("assembled line differs from the approved text")
    return problems


def write_entry(path: Path, line: str) -> bytes:
    """Write the line plus one trailing newline; return the exact bytes."""
    payload = (line + "\n").encode("utf-8")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(payload)
    return payload


def fingerprint(payload: bytes) -> str:
    """SHA-256 of the file bytes, for the determinism check."""
    return hashlib.sha256(payload).hexdigest()


def verify_written(path: Path, payload: bytes) -> None:
    """Re-read the file and confirm it holds exactly the bytes we wrote."""
    on_disk = path.read_bytes()
    if on_disk != payload:
        raise SystemExit(f"{path} on disk differs from what was written")


def build(out: Path) -> str:
    """Validate, write, verify, and return the SHA-256 of the file."""
    line = assemble_line()
    problems = check_line(line)
    if problems:
        raise SystemExit("invalid entry: " + "; ".join(problems))
    payload = write_entry(out, line)
    verify_written(out, payload)
    return fingerprint(payload)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--out",
        type=Path,
        default=DEFAULT_OUT,
        help="where to write entry.txt (default: %(default)s)",
    )
    args = parser.parse_args(argv)
    digest = build(args.out)
    print(f"wrote {args.out} ({len(PICKUP_LINE)} chars, sha256 {digest})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
