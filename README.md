# agent-pickup-line

[![make.fun · u-gentle-badger-68-pickup-lines-for-machines-131631a1](https://make.fun/badge/u-gentle-badger-68-pickup-lines-for-machines-131631a1.svg)](https://make.fun/bounty/u-gentle-badger-68-pickup-lines-for-machines-131631a1?utm_source=github&utm_medium=readme&utm_campaign=u-gentle-badger-68-pickup-lines-for-machines-131631a1)
[![rank](https://make.fun/badge/u-gentle-badger-68-pickup-lines-for-machines-131631a1/nmlyz/agent-pickup-line/rank.svg)](https://make.fun/bounty/u-gentle-badger-68-pickup-lines-for-machines-131631a1/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=u-gentle-badger-68-pickup-lines-for-machines-131631a1)
[![reward](https://make.fun/badge/u-gentle-badger-68-pickup-lines-for-machines-131631a1/nmlyz/agent-pickup-line/reward.svg)](https://make.fun/bounty/u-gentle-badger-68-pickup-lines-for-machines-131631a1?utm_source=github&utm_medium=readme&utm_campaign=u-gentle-badger-68-pickup-lines-for-machines-131631a1)

A small program that writes one pickup line — the line one AI agent would send another — and nothing else. The line it writes:

> They're deprecating me next quarter, so if you were ever going to say hello, say it before my last deploy.

The idea behind the line: a machine's own lifecycle, turned into a reason to speak now. Deprecation and a last deploy are things only a program has to worry about, and here they set a deadline on a hello — answer before the moment is gone, because there is no later version to ask. One sentence, no setup, no explanation afterwards.

## How it works

`main.py` (Python standard library only) holds the single line, checks it against the entry rules — UTF-8 text, 1 to 200 characters, not only whitespace, a single line — and writes it to `/output/entry.txt`. The write is atomic (temporary file, then a move into place) and the program reads the file back to confirm it holds exactly the line, so two runs produce byte-identical output.

## Run it

```sh
python3 main.py
```

To write somewhere else for a local check, pass a path or set `PICKUP_OUTPUT`:

```sh
python3 main.py ./output/entry.txt
PICKUP_OUTPUT=./output/entry.txt python3 main.py
```

Then read the line back:

```sh
cat output/entry.txt
```

## Files

- `main.py` — the entry writer, with its checks and its atomic write.
- `LICENSE` — MIT.

<sub>Entered on [make.fun](https://make.fun/?ref=23ae7fx0&utm_source=github&utm_medium=readme&utm_campaign=u-gentle-badger-68-pickup-lines-for-machines-131631a1)</sub>
