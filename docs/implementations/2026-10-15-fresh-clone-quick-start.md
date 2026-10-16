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
| `experiments/tiny_language_lab/README.md` | The same quick-start change for the bigram lab, the optional bigram commands, the transformer baseline commands and the GPU smoke test, with one sentence on bash paths instead of a second block. |
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

Run on 2026-10-15 on Windows 11 with Python `3.13.14` and torch
`2.12.1+cu126`, in a fresh clone of the pushed branch
(`git clone --branch fix/fresh-clone-quick-start --single-branch`), from the
repository root. The GPU was hidden with `CUDA_VISIBLE_DEVICES=-1`, so
`--device auto` resolved to `cpu` and the commands ran exactly as written.
The clone was at commit `f3e0420`; later commits change only this document.
A first PowerShell attempt set `$env:CUDA_VISIBLE_DEVICES = ""`, which
PowerShell treats as removing the variable, so its bigram runs used CUDA; the
generated corpus was deleted and every command was rerun with `-1`. All numbers
below come from the CPU reruns.

1. **The old bare command now says what to run.** In PowerShell,
   `python .\experiments\tiny_language_lab\cassandra_tiny_lm.py --method count --prompt "cassandra "`
   exits `1` and the traceback ends with:

   ```
   FileNotFoundError: Corpus file not found: <clone>\experiments\tiny_language_lab\corpus\tiny_seed.txt
   The default, corpus/tiny_seed.txt, is the original 1,129-character project-prose corpus and is not in the repository.
   Corpus files are generated locally and gitignored, so a fresh clone has none.
   From the repository root, write the structured corpus:
     python experiments/tiny_language_lab/make_synthetic_corpus.py --lines 320 --seed 20260616
   then rerun with --corpus experiments/tiny_language_lab/corpus/structured_seed.txt
   (each other corpus is written by its own make_*_corpus.py script).
   ```

   A missing non-default corpus (`cassandra_tiny_transformer.py --corpus
   .../nope.txt`) gives the same message without the `tiny_seed.txt` line.
2. **The README quick start runs in order (PowerShell block).** Every command
   exits `0`. `make_synthetic_corpus.py` prints `(25586 chars)`. The bigram
   reports, all `device` `cpu`, `vocab_size` `40`:

   | Command | `val_nll` | `val_bits_per_char` |
   | --- | ---: | ---: |
   | `--method count` | `2.020032` | `2.91429` |
   | `--method coordinate --steps 300` | `3.619758` | `5.222207` |
   | `--method gradient --steps 300` | `2.026884` | `2.924175` |

   The count result matches the `2.91429` recorded for the same corpus on
   2026-10-14 in `docs/implementations/2026-10-14-contributor-files.md`
   (Verification, item 4). Coordinate search starts from zero logits
   (`--init zeros`, the default), so 300 one-parameter steps leave it far
   above the count table; that is the method, not a fault.
3. **The bash block gives the same results.** After deleting the corpus, the
   four bash commands in Git Bash also exit `0` with the same three
   `val_bits_per_char` values; the count JSON is identical to the PowerShell
   run apart from `seconds` and the spelling of the corpus path.
4. **The four transformer demo commands in `README.md` run.** All exit `0` on
   `cpu`: `--steps 200` reaches `val_bits_per_char` `1.625152`;
   `--init count-bigram` `2.966417`; `--residual-base count-bigram
   --residual-l2 1.0` `2.862127`; `--train-scope adapters --adapter-rank 4`
   `2.918371` (`3,624` trainable of `108,328` parameters). The extra commands
   in `experiments/tiny_language_lab/README.md` (both optional bigram
   commands and `--train-scope head`) also exit `0`. The GPU smoke test
   (`--device cuda`) was not run here, because this check was CPU only.
5. **`git status` stays clean.** `git status --short` prints nothing after all
   of the above. `git status --short --ignored` lists only
   `experiments/tiny_language_lab/corpus/structured_seed.txt` and, from the
   optional `--out` command, `experiments/tiny_language_lab/last_logits.pt`,
   both ignored by `.gitignore`.
6. **The default is unchanged.** With a stand-in file copied to
   `corpus/tiny_seed.txt`, the bare `--method count` command runs, reports
   `"corpus": "...\\corpus\\tiny_seed.txt"`, and exits `0`; the check only
   acts when the file is missing. The stand-in was deleted afterwards.
7. **Style and parse checks.** A byte-wise scan of the five changed files for
   U+2013 and U+2014 finds `0` of each, and no added line in the diff carries
   either. The AST one-liner in `CONTRIBUTING.md` reports `44 files parse`.
8. **The #7 section.** It is 25 lines from its heading to the blank line before
   "Collaboration workflow". The model page answered the Hugging Face API on
   2026-10-15 as public (`private: false`) with the weights, `config.json`,
   `codec.json`, `inference_example.py` and `reproduce_text8_eval.py` in its
   file list. `flagship_eval_lib.py` defines `load_model_from_safetensors` and
   `sample_text` with the keyword arguments the snippet uses. The snippet
   itself was not run here, because it needs the released weights.

**Not done here:**

- `CONTRIBUTING.md` still has the "Known issue #3" paragraph, which is stale
  once this merges; it was left alone to avoid colliding with a concurrent
  change to that file and should be removed in a follow-up.
- `.github/ISSUE_TEMPLATE/bug_report.yml` names #3 as an example of an open
  issue; once #3 closes, that example should change.
- `CLAUDE.md` and `AGENTS.md` keep their commands without `--corpus` (see
  Design Decisions).
- Whether to publish the original `tiny_seed.txt` is open for the maintainers.

## Related Docs

- Issues #3 (missing default corpus) and #7 (link the released model)
- `experiments/tiny_language_lab/RESULTS.md` (the 2026-06-15 table and Stage 29,
  the `tiny_seed.txt` runs)
- `docs/release/stage61-flagship/MODEL_CARD.md` and `UPLOAD.md`
- `CONTRIBUTING.md` (the verified quick start, and the "Known issue #3"
  paragraph that this change makes stale)
- `docs/implementations/2026-10-14-contributor-files.md`
