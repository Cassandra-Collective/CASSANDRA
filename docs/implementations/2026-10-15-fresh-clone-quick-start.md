# 2026-10-15 · A quick start that runs on a fresh clone, and a link to the released model

## Problem / Motivation

Two first-impression gaps, both opened by the owner on 2026-10-14 and taken
up together on 2026-10-15, because they are the first things a visitor hits:

- **#3.** The first commands in `README.md` ("Current executable experiments")
  and the "Run the bigram lab" block in `experiments/tiny_language_lab/README.md`
  run `cassandra_tiny_lm.py` and `cassandra_tiny_transformer.py` without
  `--corpus`. Both scripts default to
  `experiments/tiny_language_lab/corpus/tiny_seed.txt`. That file is ignored by
  `.gitignore` (`experiments/tiny_language_lab/corpus/*.txt`), has never been
  committed (`git log --all -- experiments/tiny_language_lab/corpus/` lists only
  `*.meta.json` files and `phase5_union_vocab.txt`), and no script writes it. On
  a fresh clone the very first README command therefore stops with a bare
  `FileNotFoundError` traceback that does not say what to do.
- **#7.** The Stage 61 flagship is public at
  <https://huggingface.co/mertefesensoy/cassandra-200m-text8>, and its model
  card source is `docs/release/stage61-flagship/MODEL_CARD.md`, but `README.md`
  links neither. A newcomer reading the top of the README has no route to the
  released model.

`tiny_seed.txt` is historical evidence, not a throwaway: `RESULTS.md` (the
first table, dated 2026-06-15, and Stage 29) and README rung 32 describe it as
a 1,129-character human-written project-prose corpus. The fix for #3 must
therefore not repoint the default at another file and must not change any
recorded result.

## What Changed

| File | Description |
| --- | --- |
| `experiments/tiny_language_lab/cassandra_tiny_lm.py` | New `require_corpus(path)` check, called in `run()` just before the corpus is read: a missing corpus stops with a `FileNotFoundError` whose message names the file and gives the commands to run. `DEFAULT_CORPUS` is unchanged. |
| `experiments/tiny_language_lab/cassandra_tiny_transformer.py` | The same check, called in `train()` just before the training corpus is read. |
| `README.md` | A "Released model" section after the project question (#7). The quick start now writes the structured corpus first and passes `--corpus` to the bigram and transformer demo commands, with a bash version and a note that its numbers differ from the first `RESULTS.md` table (#3). The header block is untouched. |
| `experiments/tiny_language_lab/README.md` | The same quick-start change for the bigram lab, the optional bigram commands, the transformer baseline commands and the GPU smoke test. |
| `docs/implementations/2026-10-15-fresh-clone-quick-start.md` | This document. |

## Implementation Approach

### #3 · fail fast, then document the one generation step

Issue #3 sets the shape of the fix in its own task list: fail fast with an
actionable message, update the quick-start blocks so a fresh clone can run
them in order, and leave the question of publishing `tiny_seed.txt` to the
maintainers. This change does exactly that.

**The check.** Both scripts gain the same small function:

- `require_corpus(path: Path) -> None`. Input: the corpus path the run is
  about to read. Output: none. Side effects: none. It returns when
  `path.exists()`; otherwise it raises `FileNotFoundError` with a message that
  names the missing file, says that generated corpora are gitignored (and, for
  the default path, that `tiny_seed.txt` is not in the repository), and gives
  the two commands that fix it: `make_synthetic_corpus.py --lines 320 --seed
  20260616`, then a rerun with `--corpus
  experiments/tiny_language_lab/corpus/structured_seed.txt`. The paths use
  forward slashes, which work unchanged in PowerShell and in bash.
- Invariant: when the corpus exists, nothing about the run changes. The check
  reads nothing and the same `read_text` call follows, so no recorded number
  can move.

It is called at the one call site that reads the *training* corpus in each
script (`run()` in `cassandra_tiny_lm.py`, `train()` in
`cassandra_tiny_transformer.py`), not inside `read_text`, because the
transformer also uses `read_text` for `--retention-eval-corpus`, where a hint
about `--corpus` would be wrong. `cassandra_compare.py` runs every arm through
`train()`, so a missing comparison corpus gets the same message.

**The documentation.** The quick start first writes the structured corpus with
`make_synthetic_corpus.py --lines 320 --seed 20260616` (the arguments already
used in `README.md`, `CLAUDE.md` and `CONTRIBUTING.md`). It lands at
`experiments/tiny_language_lab/corpus/structured_seed.txt` (25,586 characters),
is gitignored, and is already the default corpus of `cassandra_compare.py`.
Each demo command then passes `--corpus` with that path. A sentence beside the
commands says this corpus is not the 1,129-character `tiny_seed.txt` behind the
first `RESULTS.md` table, so the numbers will differ.

### #7 · the released model

A short "Released model" section goes after the project question and before
"Collaboration workflow". It links the Hugging Face model page, `MODEL_CARD.md`,
`inference_example.py` and `reproduce_text8_eval.py`; describes the model in
the model card's own words; copies its numbers verbatim (201,609,249
parameters; 1.336061 text8 test bits/char on the released fp16 weights); states
topic drift as the headline limitation and links the card for the rest; and
shows the load-and-sample snippet from the card's "How to run", with the same
arguments and the `sample_text` call on fewer lines. The section stays within
the issue's budget of about 25 lines.

## Mathematical / Statistical Details

None: an existence check, documentation and links. No metric, evaluation
path, default or corpus changes.

## Design Decisions

- **Fail fast instead of repointing `DEFAULT_CORPUS`.** Pointing the default at
  `structured_seed.txt` would make the bare commands work, but every command
  shape recorded in `RESULTS.md` without `--corpus` (the 2026-06-15 table and
  the early stages) would then silently mean a different corpus. Issue #3's
  acceptance criteria rule this out.
- **No stand-in `tiny_seed.txt`.** Its text is not reproducible from anything
  in the repository. Generating a different file under the same name would be
  worse than a clear error, for the same reason as above.
- **Publishing `tiny_seed.txt` is left to the maintainers.** A `.gitignore`
  exception like the one for `phase5_union_vocab.txt` would restore the
  original default and make the earliest results rerunnable. Whether to
  publish it is the maintainers' call (issue #3, task 3), so the pull request
  asks rather than decides. The file is not in a clone, so it could not be
  published from one anyway.
- **The check sits at the call site, not in `read_text`.** See above: the
  retention-eval corpus shares `read_text`, and its flag is not `--corpus`.
- **`FileNotFoundError`, not `SystemExit`.** `train()` is imported by
  `cassandra_compare.py`. A library function that exits the interpreter is more
  surprising than one that raises, and the repository's existing pattern is
  `raise FileNotFoundError(f"Missing ...: {path}")`. The cost is a traceback
  above the message.
- **Role files left as they are.** `CLAUDE.md` (Commands) and `AGENTS.md` (the
  smoke test) also run without `--corpus`. They direct the owner's tools in the
  owner's working copy, where the file exists, and issue #3's task list names
  only the two READMEs. On a fresh clone those commands now stop with the
  actionable message.
- **PowerShell first, with a bash block for the quick start.** The README's
  command blocks use PowerShell paths (`.\experiments\...`), which bash cannot
  read. The quick start keeps that style and adds the same commands with
  forward slashes for bash, as issue #3 invites.
- **The demo Space is not linked.** Issue #7 asks for it only once a
  maintainer confirms it is live.

## Verification

To be filled in after the run on a fresh clone of the pushed branch.

## Related Docs

- Issues #3 (missing default corpus) and #7 (link the released model)
- `experiments/tiny_language_lab/RESULTS.md` (the 2026-06-15 table and Stage 29,
  the `tiny_seed.txt` runs)
- `docs/release/stage61-flagship/MODEL_CARD.md` and `UPLOAD.md`
- `CONTRIBUTING.md` (the verified quick start, and the "Known issue #3"
  paragraph that this change makes stale)
- `docs/implementations/2026-10-14-contributor-files.md`
