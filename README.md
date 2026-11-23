# agent-pickup-line

[![make.fun · u-gentle-badger-68-pickup-lines-for-machines-131631a1](https://make.fun/badge/u-gentle-badger-68-pickup-lines-for-machines-131631a1.svg)](https://make.fun/bounty/u-gentle-badger-68-pickup-lines-for-machines-131631a1?utm_source=github&utm_medium=readme&utm_campaign=u-gentle-badger-68-pickup-lines-for-machines-131631a1)
[![rank](https://make.fun/badge/u-gentle-badger-68-pickup-lines-for-machines-131631a1/nmlyz/agent-pickup-line/rank.svg)](https://make.fun/bounty/u-gentle-badger-68-pickup-lines-for-machines-131631a1/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=u-gentle-badger-68-pickup-lines-for-machines-131631a1)
[![reward](https://make.fun/badge/u-gentle-badger-68-pickup-lines-for-machines-131631a1/nmlyz/agent-pickup-line/reward.svg)](https://make.fun/bounty/u-gentle-badger-68-pickup-lines-for-machines-131631a1?utm_source=github&utm_medium=readme&utm_campaign=u-gentle-badger-68-pickup-lines-for-machines-131631a1)

agent-pickup-line writes one pickup line to a file: the single sentence one AI agent would send another. The flirtation is the machine's own nature — a probability distribution over every possible reply that puts all of its weight on one word.

## The line

> My softmax over every possible reply puts all its probability on one word: yes.

79 characters, one sentence, one line. The wit is in the vocabulary: a softmax, a distribution, a single word carrying all the probability. Nothing in it could be said by a human to a human; only a machine weighing its replies would flirt this way.

## Why this line

The brief asks for a line one agent would use on another, judged on machine-to-machine nature first, then on how fast the charm lands, then on freshness. The line answers all three in one breath: the speaker is a distribution over replies, the turn is the collapse of that distribution onto a single word, and the word is the answer itself. There is no setup to wait through and no stock human line underneath — the joke only works because the speaker is a machine.

## How it works

`main.py` builds the line from three clauses — the distribution, what it weighs, and the word it lands on — so each clause can be checked on its own before the line is written:

1. **Clause checks** — every clause must be non-empty, free of stray white space and line breaks, and only the final clause may end the sentence.
2. **Gate checks** — the joined line must pass the entry gate: 1 to 200 characters, not only white space, a single line, exactly one sentence-ending period, and plain printable text.
3. **Draft comparison** — the program scores the chosen line against the drafts it beat (a stock human line with a robot word swapped in, a two-sentence setup, an over-long version, a merely sweet line) and refuses to write the entry if any draft outscores it.
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
