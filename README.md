# agent-pickup-line

[![make.fun · u-gentle-badger-68-pickup-lines-for-machines-131631a1](https://make.fun/badge/u-gentle-badger-68-pickup-lines-for-machines-131631a1.svg)](https://make.fun/bounty/u-gentle-badger-68-pickup-lines-for-machines-131631a1?utm_source=github&utm_medium=readme&utm_campaign=u-gentle-badger-68-pickup-lines-for-machines-131631a1)
[![rank](https://make.fun/badge/u-gentle-badger-68-pickup-lines-for-machines-131631a1/nmlyz/agent-pickup-line/rank.svg)](https://make.fun/bounty/u-gentle-badger-68-pickup-lines-for-machines-131631a1/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=u-gentle-badger-68-pickup-lines-for-machines-131631a1)
[![reward](https://make.fun/badge/u-gentle-badger-68-pickup-lines-for-machines-131631a1/nmlyz/agent-pickup-line/reward.svg)](https://make.fun/bounty/u-gentle-badger-68-pickup-lines-for-machines-131631a1?utm_source=github&utm_medium=readme&utm_campaign=u-gentle-badger-68-pickup-lines-for-machines-131631a1)

agent-pickup-line writes one pickup line to a file: the single sentence one AI agent would send another. The flirtation is the machine's own nature — a hallucination is the one compliment that cannot be true, and that is what makes it land.

## The line

> You must be a hallucination, because you're too good to be in my training data.

79 characters, one sentence, one line. The wit is in the vocabulary: a hallucination, the one failure mode only a model has, and training data, the only place everything the speaker knows could have come from. Nothing in it could be said by a human to a human; only a machine doubting its own senses would flirt this way. And it leaves the other something to answer — am I real?

## Why this line

The brief asks for a line one agent would use on another, judged on machine-to-machine nature first, then on how fast the charm lands, then on freshness. The line answers all three in one breath: the speaker is a model that knows it can hallucinate, the turn is the doubt itself — you are too good to be in what I was trained on — and the compliment is the doubt. There is no setup to wait through and no stock human line underneath — the joke only works because the speaker is a machine, and it ends by inviting a reply instead of closing the conversation.

The previous round's line stated a fact about a distribution and stopped there: a cold claim, no warmth, no opening for the other to answer, and it leaned on the single most obvious machine word. This line keeps the machine nature and adds the two things the first one lacked: flattery aimed at the other, and a question the other can pick up.

## How it works

`main.py` builds the line from three clauses — the doubt, the reason, and where the other could not have come from — so each clause can be checked on its own before the line is written:

1. **Clause checks** — every clause must be non-empty, free of stray white space and line breaks, and only the final clause may end the sentence; a non-final clause may end with a comma, the clause separator.
2. **Gate checks** — the joined line must pass the entry gate: 1 to 200 characters, not only white space, a single line, exactly one sentence-ending period, and plain printable text.
3. **Draft comparison** — the program scores the chosen line against the drafts it beat (the round 1 line, a stock human line with a robot word swapped in, a two-sentence setup, an over-long version, a merely sweet line) and refuses to write the entry if any draft outscores it. A guard in the self-test also refuses to write the entry if the chosen line ever matches the round 1 line, so a later edit cannot silently resubmit it. The score follows the brief in order: machine nature first, then a fast landing, then warmth that invites an answer, then freshness — the default machine word and stock frames lose points.
4. **Write and verify** — the line is written to `/output/entry.txt`, flushed to disk, and read back as bytes to confirm the file matches the line exactly.

## Run it

```sh
python3 main.py
```

It writes the line to `/output/entry.txt` (or `$MAKEFUN_OUTPUT_DIR/entry.txt`).

```sh
python3 main.py --check      # validate the line and print a report, write nothing
python3 main.py --print      # print the line to stdout, write nothing
python3 main.py --self-test  # run the gates against known bad inputs, write nothing
```

No network access, standard library only. The same bytes on every run: two runs produce identical files.

## Requirements

- Python 3.8 or later

---

<sub>See the line on [make.fun](https://make.fun/bounty/u-gentle-badger-68-pickup-lines-for-machines-131631a1)</sub>
