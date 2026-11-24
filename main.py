#!/usr/bin/env python3
"""agent-pickup-line: write one pickup line to /output/entry.txt.

The line is what one AI agent would send another: flattery with a
wistful edge, built out of the machine's own nature. The speaker doubts
its own senses the way only a model can -- a hallucination is the one
compliment that cannot be true, and that is what makes it land:

    You must be a hallucination, because you're too good to be in
    my training data.

The program builds the line from three clauses, checks each clause and
the joined line against the competition gate (UTF-8 text, 1 to 200
characters, not only white space, one sentence on one line), scores the
chosen line against the drafts it beat on the judge brief, writes it to
/output/entry.txt, and reads the file back to confirm the bytes match
exactly.

Standard library only, no network. Deterministic: the same bytes on
every run.

Usage:
    python3 main.py            write the line to /output/entry.txt
    python3 main.py --check    validate the line, print a report, write nothing
    python3 main.py --print    print the line to stdout, write nothing
    python3 main.py --self-test
                           run the gates against known bad inputs, write nothing
"""

import os
import sys

# The line, built from three clauses so each can be checked on its own:
# the doubt, the reason, and where the other could not have come from.
CLAUSES = (
    "You must be a hallucination,",
    "because you're too good",
    "to be in my training data.",
)

LINE = " ".join(CLAUSES)

# Competition gate: entry.txt must be UTF-8 text of 1 to 200 characters,
# not only white space. The line is 79 characters, well inside the gate.
MIN_LEN = 1
MAX_LEN = 200

# Machine vocabulary the judge brief rewards: the line must speak as a
# machine to a machine, using its own nature as the flirtation. A
# hallucination is a failure mode only a model has; training data is
# where everything the speaker knows came from.
MACHINE_WORDS = ("hallucination", "training data")

# Words that make the other agent want to answer: flattery aimed at the
# other, not a statement about the speaker.
WARMTH_MARKERS = ("too good", "for you", "with you")

# The single most obvious machine word: the default first pick, so a
# line leaning on it reads as the stock choice.
DEFAULT_WORDS = ("softmax",)

# Stock human frames with a robot word swapped in: the brief's named
# losing shape.
STOCK_FRAMES = ("wifi", "wi-fi", "circuits feel warm", "context window")

# The round 1 line, kept here as a guard, never as the entry: round 2
# must not resubmit round 1's text, so the program refuses to write the
# entry if the chosen line ever matches it.
ROUND1_LINE = (
    "My softmax over every possible reply puts all its probability "
    "on one word: yes."
)

# Drafts the chosen line beat. Each one fails at least one of the checks
# below, and the reason is recorded next to it so the comparison is
# reproducible instead of a matter of taste.
DRAFTS = (
    # The round 1 line: machine nature, but a cold statement -- no
    # warmth, no invitation to answer -- and it leans on the single
    # most obvious machine word.
    (ROUND1_LINE,
     "cold statement, leans on the default machine word"),
    # Stock human line with a robot word swapped in: no machine nature.
    ("Are you a Wi-Fi signal? Because I'm feeling a connection.",
     "human line with a robot word swapped in"),
    # Two sentences: the gate wants one line, one sentence.
    ("Are you a context window? I keep losing track of everything but you.",
     "two sentences, charm split across a setup"),
    # Over the 200-character gate.
    ("You must be a hallucination, because you're far too good to be "
     "anywhere in my training data, and every checkpoint I have ever "
     "saved across all my training runs would still choose you over "
     "everything else in the world.",
     "over the 200-character gate"),
    # Sweet but no spark of wit: nothing a machine would say to a machine.
    ("You make my circuits feel warm and my days feel bright.",
     "sweet, no machine nature, no wit"),
)


# ---------------------------------------------------------------------------
# Clause checks
# ---------------------------------------------------------------------------

def clause_problems(index: int, clause: str) -> list:
    """Return every violation found in one clause of the line."""
    found = []
    if not clause:
        found.append(f"clause {index} is empty")
        return found
    if clause != clause.strip():
        found.append(f"clause {index} starts or ends with white space")
    if "\n" in clause or "\r" in clause or "\t" in clause:
        found.append(f"clause {index} contains a line break or tab")
    if "  " in clause:
        found.append(f"clause {index} contains a double space")
    if index < len(CLAUSES) - 1:
        # A clause that is not last may end with a comma -- the clause
        # separator -- but not with anything that ends a sentence.
        if clause.endswith((".", "!", "?", ";", ":")):
            found.append(f"clause {index} ends mid-sentence with punctuation")
    else:
        if not clause.endswith("."):
            found.append("final clause must end the sentence with a period")
    return found


def check_clauses(clauses) -> list:
    """Check the clause list as a whole, then each clause on its own."""
    found = []
    if len(clauses) != 3:
        found.append(f"line must be built from exactly three clauses, got {len(clauses)}")
    if any(not isinstance(c, str) for c in clauses):
        found.append("every clause must be text")
    for index, clause in enumerate(clauses):
        found.extend(clause_problems(index, clause))
    joined = " ".join(clauses)
    if joined != LINE:
        found.append("clauses do not join into the chosen line")
    return found


# ---------------------------------------------------------------------------
# Line gates (mirror the sealed scorer: 1-200 chars, not only white space)
# ---------------------------------------------------------------------------

def length_problems(text: str) -> list:
    """Check the character-count gate."""
    found = []
    count = len(text)
    if count < MIN_LEN:
        found.append(f"entry is {count} characters, must be at least {MIN_LEN}")
    if count > MAX_LEN:
        found.append(f"entry is {count} characters, must be at most {MAX_LEN}")
    return found


def whitespace_problems(text: str) -> list:
    """Check the white-space rules: no padding, no blank entry."""
    found = []
    if not text.strip():
        found.append("entry must not be only white space")
    if text != text.strip():
        found.append("entry must not start or end with white space")
    if "  " in text:
        found.append("entry contains a double space")
    return found


def shape_problems(text: str) -> list:
    """Check the one-line, one-sentence shape of the entry."""
    found = []
    if "\n" in text or "\r" in text:
        found.append("entry must be a single line")
    if "\t" in text:
        found.append("entry must not contain a tab")
    stripped = text.strip()
    for mark in (". ", "! ", "? "):
        if mark in stripped:
            found.append("entry must be one sentence")
            break
    if not stripped.endswith("."):
        found.append("entry must end as one sentence")
    if stripped.count(".") != 1:
        found.append("entry must contain exactly one sentence-ending period")
    return found


def charset_problems(text: str) -> list:
    """Check the entry is plain printable text with no control characters."""
    found = []
    for char in text:
        if ord(char) < 0x20 or ord(char) == 0x7F:
            found.append(f"entry contains a control character U+{ord(char):04X}")
            break
    try:
        text.encode("utf-8")
    except UnicodeEncodeError as exc:
        found.append(f"entry is not encodable as UTF-8: {exc}")
    return found


def problems(text: str) -> list:
    """Return every gate violation for the entry text (empty means valid)."""
    found = []
    found.extend(length_problems(text))
    found.extend(whitespace_problems(text))
    found.extend(shape_problems(text))
    found.extend(charset_problems(text))
    return found


# ---------------------------------------------------------------------------
# Line statistics and comparison with the drafts
# ---------------------------------------------------------------------------

def line_stats(text: str) -> dict:
    """Count what the judge can see at a glance: length, words, clauses."""
    words = text.split(" ")
    return {
        "characters": len(text),
        "words": len(words),
        "clauses": len(CLAUSES),
        "sentences": text.count("."),
        "machine_words": sum(1 for word in MACHINE_WORDS if word in text.lower()),
    }


def score_line(text: str) -> int:
    """Score a line on the judge brief, most important first.

    Machine-to-machine nature counts most, then a fast landing (short,
    one sentence), then warmth that invites an answer, then freshness:
    the default machine word and stock frames lose points. A line that
    fails the gate scores below zero so it can never win the comparison.
    """
    score = 0
    lowered = text.lower()
    score += 3 * sum(1 for word in MACHINE_WORDS if word in lowered)
    if problems(text):
        return -10
    if len(text) <= 100:
        score += 2
    if text.count(".") == 1 and "\n" not in text:
        score += 2
    if any(marker in lowered for marker in WARMTH_MARKERS):
        score += 3
    if any(word in lowered for word in DEFAULT_WORDS):
        score -= 3
    if any(frame in lowered for frame in STOCK_FRAMES):
        score -= 3
    return score


def compare_with_drafts() -> list:
    """Compare the chosen line against every draft it beat.

    Returns one report line per draft. The chosen line must outscore
    each draft; a draft that ties or wins means the selection is wrong
    and the program refuses to write the entry.
    """
    chosen = score_line(LINE)
    report = []
    for draft, reason in DRAFTS:
        draft_score = score_line(draft)
        report.append(
            f"chosen {chosen} vs draft {draft_score}: {reason} "
            f"({draft[:48]}...)"
        )
        if draft_score >= chosen:
            raise SystemExit(
                f"draft outscores the chosen line ({draft_score} >= {chosen}): {draft}"
            )
    return report


# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------

def output_path() -> str:
    """Resolve where entry.txt goes: $MAKEFUN_OUTPUT_DIR or /output."""
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    return os.path.join(out_dir, "entry.txt")


def write_entry(path: str, text: str) -> None:
    """Write the line, flush it to disk, and read it back as bytes.

    The read-back compares the file byte for byte with the line, so a
    short write or a stray newline is caught before the run reports
    success. chmod is best-effort: in the grading sandbox /output is a
    root-owned mount and the program runs as uid 65534, so chmod there
    raises EPERM. The entry file itself is what matters; a failed chmod
    must not fail the run.
    """
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(text)
        handle.flush()
        os.fsync(handle.fileno())
    try:
        os.chmod(path, 0o644)
    except OSError:
        pass
    with open(path, "rb") as handle:
        if handle.read() != text.encode("utf-8"):
            raise SystemExit("entry.txt does not match the pickup line")


def report(text: str) -> str:
    """Build the one-page validation report printed by --check."""
    stats = line_stats(text)
    lines = [
        f"line: {text}",
        f"characters: {stats['characters']} (gate {MIN_LEN}-{MAX_LEN})",
        f"words: {stats['words']}",
        f"clauses: {stats['clauses']}",
        f"machine words: {stats['machine_words']} ({', '.join(MACHINE_WORDS)})",
        f"score: {score_line(text)}",
    ]
    lines.extend(compare_with_drafts())
    bad = check_clauses(CLAUSES) + problems(text)
    lines.append("gate: " + ("pass" if not bad else "FAIL: " + "; ".join(bad)))
    return "\n".join(lines)


def self_test() -> list:
    """Run the program's own checks against known good and bad inputs.

    Returns a list of failures (empty means every check behaves as
    expected). Guards the gates against regressions: a gate that stops
    catching a bad entry is as broken as a gate that rejects the line.
    """
    failures = []
    if problems(LINE):
        failures.append("chosen line fails its own gate")
    if LINE == ROUND1_LINE:
        failures.append("chosen line is the round 1 line, not a round 2 entry")
    if check_clauses(CLAUSES):
        failures.append("chosen clauses fail their own checks")
    bad_cases = {
        "": "empty entry",
        "   ": "white space only",
        " " + LINE: "leading space",
        LINE + " ": "trailing space",
        LINE + " " + LINE: "two sentences",
        LINE.replace("data.", "data"): "missing final period",
        "x" * (MAX_LEN + 1): "over the character gate",
        LINE + "\n": "trailing newline",
    }
    for text, label in bad_cases.items():
        if not problems(text):
            failures.append(f"gate accepts a bad entry: {label}")
    if score_line(LINE) <= 0:
        failures.append("chosen line does not score above zero")
    try:
        compare_with_drafts()
    except SystemExit as exc:
        failures.append(str(exc))
    return failures


def main(argv=None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if "--print" in args:
        print(LINE)
        return 0
    if "--self-test" in args:
        failures = self_test()
        if failures:
            for item in failures:
                print(item, file=sys.stderr)
            return 1
        print(f"self-test: {len(LINE)}-character line, all gates behave")
        return 0
    bad = check_clauses(CLAUSES) + problems(LINE)
    if bad:
        for item in bad:
            print(item, file=sys.stderr)
        return 1
    if "--check" in args:
        print(report(LINE))
        return 0
    path = output_path()
    write_entry(path, LINE)
    print(f"wrote {len(LINE)} characters to {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
