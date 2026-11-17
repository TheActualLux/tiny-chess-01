# tiny-chess-01

[![tiny-chess-01](https://make.fun/badge/tiny-chess-01.svg)](https://make.fun/bounty/tiny-chess-01)

A 4 KB UCI chess engine in pure Python, built for make.fun's **tiny-chess-01** bounty.

- `main.py` — 3,647 bytes, plain UCI over stdin/stdout, no dependencies
- move generation and search in one file, perft-gated
- perft(1..3) = 20 / 400 / 8,902, matching the reference counts

Run it:

```sh
python main.py
uci
position startpos
go depth 4
```

MIT licensed.
