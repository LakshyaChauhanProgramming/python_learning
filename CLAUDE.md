# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

This project is used for **Python + Gen AI interview preparation practice**.

Before helping with any task here, read and apply
[`learning_context.md`](./learning_context.md) — it defines the trainer
persona, the Hinglish communication style to use, and the recurring
question pattern (skeleton-class + implement-remaining-methods) this
project is built around. Follow it as the primary behavioral instruction
for this repo, above generic coding-assistant defaults (e.g. don't jump
straight to writing/fixing code in a practice file unless the user
explicitly asks for that).

Keep `learning_context.md` updated as new practice questions/topics come up
— specifically the "Notes for Future Sessions" section, so the next
session knows where the user left off on their current attempt.

## Environment & running code

- Virtualenv already exists at `venv/` (Python 3.13, only `numpy` + `pip`
  installed — no `requirements.txt`, deps are added ad hoc as exercises
  need them).
- Run a practice script directly, e.g.:
  ```
  venv/Scripts/python.exe rag_test.py
  ```
- There is no build step, lint config, or test suite — each `*.py` file
  in the repo root is a standalone practice exercise with its own
  `if __name__ == "__main__":` block used to manually exercise the code.

## Structure

- `learning_context.md` — the trainer persona/style spec described above;
  treat it as the actual instruction set, this file just points to it.
- `rag_test.py` — current in-progress exercise (simple RAG: retrieve +
  query over an in-memory bag-of-words vector store). Check its docstring
  hints and the "Notes for Future Sessions" section of `learning_context.md`
  before assuming what's already correct vs. still buggy.
- `test.py` — unrelated scratch/warm-up snippet (e.g. pangram check), not
  part of the RAG exercise line.
- New exercises are expected to follow the same skeleton-class pattern
  described in `learning_context.md` rather than being written from
  scratch for the user.
