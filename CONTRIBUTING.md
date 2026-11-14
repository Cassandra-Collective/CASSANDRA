# Contributing to CASSANDRA

Thank you for considering a contribution. This guide is written for people.
Most of the house rules below already exist in the repository, but they are
spelled out in files written for the owner's AI tools (`CLAUDE.md`,
`CODEX.md`, `GEMINI.md`, `AGENTS.md`, `INSTRUCTIONS.md`), and the one
automatic style check only runs inside those tools' sessions. This file
collects the rules in one place so you can follow them without reading the
role files first.

Taking part in this project means following the
[Cassandra Collective code of conduct](https://github.com/Cassandra-Collective/.github/blob/main/CODE_OF_CONDUCT.md).

## What this project is, and what it is not

CASSANDRA is a research workspace with two connected tracks:

1. `AGENT.md` · a prose working reference for accountable protective AI
   systems. It is writing, not code.
2. `experiments/tiny_language_lab/` · a laptop-scale lab that asks whether
   useful language-model behavior can be formed by *reducing* brute-force
   gradient training (analytic initialization, frozen priors, small
   trainable surfaces, verifier-guided data, retrieval) rather than by
   scaling it. Its research map is `docs/LOW_HARDWARE_LM_RESEARCH.md` and its
   staged evidence log is `experiments/tiny_language_lab/RESULTS.md`.

Most contributions land in the second track.

What it is not:

- **Not a claim that a laptop can build a frontier model.** In the README's
  words, it is a lab for testing smaller claims honestly, then keeping only
  the ones that survive.
- **Not a library.** The scripts are research code run from the repository
  root. There is no package to install and no stable API. The CPU helper test
  suite is documented in the [lab README](experiments/tiny_language_lab/README.md#cpu-helper-tests).
- **Not a place for results nobody can regenerate.** A number without the
  command, seeds and artifact behind it is not evidence here, however good
  it looks.

## Getting started

You need Python 3 and PyTorch. A CPU build of torch is enough for the quick
start and for many of the open issues; the owner's long comparison matrices
run on a CUDA laptop GPU. Some scripts import more (`numpy`, `matplotlib`,
`safetensors`, `onnx`, `onnxruntime`, `gradio`). There is no requirements file
yet; that is #8.

The quick start below uses forward-slash paths, which work unchanged in
PowerShell and in bash. Run it from the repository root:

```
git clone https://github.com/Cassandra-Collective/CASSANDRA.git
cd CASSANDRA
git config core.hooksPath .githooks

python experiments/tiny_language_lab/make_synthetic_corpus.py --lines 320 --seed 20260616
python experiments/tiny_language_lab/cassandra_tiny_lm.py --method count --corpus experiments/tiny_language_lab/corpus/structured_seed.txt
python experiments/tiny_language_lab/cassandra_tiny_transformer.py --device cpu --steps 20 --eval-interval 10 --max-new-tokens 80 --corpus experiments/tiny_language_lab/corpus/structured_seed.txt
```

What each step does:

1. `git config core.hooksPath .githooks` turns on the 50 MiB file guard
   described below. A fresh clone does not run it until you do this.
2. `make_synthetic_corpus.py` writes the deterministic structured corpus to
   `experiments/tiny_language_lab/corpus/structured_seed.txt` (`25,586`
   characters with these arguments). Generated corpora are gitignored, so the
   file never appears in `git status`.
3. The bigram lab forms one logit matrix directly from character counts, with
   no gradient training, and prints a JSON report that includes `val_nll`,
   `val_bits_per_char` and a sample.
4. The transformer smoke test trains for 20 steps on the CPU. With a CUDA
   build of torch, leave out `--device cpu`: the default `auto` picks the GPU
   when `torch.cuda.is_available()` is true.

**Known issue #3.** The first commands in `README.md`, and the smoke tests in
`CLAUDE.md` and `AGENTS.md`, run without `--corpus`. Both scripts then look for
`corpus/tiny_seed.txt`, which is not in the repository, and stop with a
`FileNotFoundError` on a fresh clone. Passing `--corpus` as above works around
it until #3 is fixed.

`cassandra_compare.py`, the multi-seed comparison runner, already defaults to
`structured_seed.txt` (the file made above), but it also defaults to
`--device cuda`. Pass `--device cpu` for small diagnostics only. Every entry
point prints its full flag surface with `--help`.

The sequence above was run on 2026-10-14 on Windows 11 with Python `3.13` and
torch `2.12.1` (a CUDA build, run on the CPU for the smoke test), in both
PowerShell and Git Bash.

## Where to find work

- [`good first issue`](https://github.com/Cassandra-Collective/CASSANDRA/labels/good%20first%20issue):
  small, well-scoped tasks with pointers to the exact files and lines.
- [`help wanted`](https://github.com/Cassandra-Collective/CASSANDRA/labels/help%20wanted):
  tasks the owner would especially like help with.
- [`research`](https://github.com/Cassandra-Collective/CASSANDRA/labels/research):
  replications, new probes and prior-art notes.
- The [Release lane · Stage 61 flagship](https://github.com/Cassandra-Collective/CASSANDRA/milestone/1)
  milestone: follow-through on the public release of the 200M flagship model.

The `area: docs`, `area: experiments` and `area: release` labels say which part
of the repository an issue touches.

Task issues share one shape: **Context**, **Task**, **Acceptance criteria**,
**Pointers**, **Not in scope**. The acceptance criteria are the definition of
done, and "Not in scope" is part of the contract: open a new issue for
adjacent work instead of widening a pull request. To take an issue, comment
on it so the owner can assign it to you and two people do not do the same
work.

## House rules

### Prose style

- **No em dashes and no en dashes**, anywhere in the repository's docs. Use
  the middle dot `·`, a comma, parentheses, or a restructured sentence. The
  ordinary hyphen `-` is fine.
- `AGENT.md` is the one exemption, as a legacy prose artifact. Twelve research
  notes still carry a dash; #6 tracks them.
- Numbers are backticked, cited to the file they come from, and never
  invented. A number is either measured or written as "to be measured".
- Absolute dates only (`2026-10-14`, never "next week").
- Claims are scoped tightly, and a strong result ends by naming what it does
  not prove.

The rule comes from `INSTRUCTIONS.md` section 2. Its automatic check,
`.claude/hooks/check_md_dashes.py`, only runs inside Claude Code sessions, and
there is no CI yet (#13), so run the check yourself. From the repository root,
in PowerShell or bash:

```
python -c "import pathlib; [print(p, i) for p in pathlib.Path('.').rglob('*.md') if p.name != 'AGENT.md' for i, l in enumerate(p.read_text(encoding='utf-8').splitlines(), 1) if '\u2014' in l or '\u2013' in l]"
```

It prints `file line` for every Markdown line with an em or en dash. On `main`
on 2026-10-14 it prints the twelve notes from #6; no file you changed should
appear.

### Determinism and seeds

- Comparison matrices use seeds `7 11 19` (the `cassandra_compare.py`
  default); single runs default to seed `7`. Corpus generators take fixed
  seeds too: `20260616` for the structured corpus and `20260617` for the
  long-context corpus. Keep them fixed so results replicate, and state the
  seeds of any new experiment.
- CPU and CUDA sampled runs are separate measurement families. The trainer
  draws training and evaluation windows from `torch.Generator(device=device)`,
  so the same seed picks different windows on each device. Say which device
  you used; #15 tracks a device-independent option.
- Closeout claims use the deterministic chunked evaluation;
  `--eval-mode sampled --eval-batches 16` is for monitoring during a run only
  (ADR 0014, summarized in `INSTRUCTIONS.md` section 1).

### Falsifiable hypotheses and ADRs

- **Hypotheses** live at `docs/hypotheses/NNN-slug.md`: three digits, one
  more than the highest existing number, a short lowercase hyphenated slug. A variant of an existing
  hypothesis takes a letter suffix (as `009b` does). Every hypothesis carries
  a **pass-or-fail line**, explicit CONFIRM and KILL thresholds, written
  before the run. A threshold may be recalibrated against the published
  record before the run, never after seeing the result.
- **ADRs** (architecture decision records) live at
  `docs/decisions/NNNN-slug.md`: four digits, one more than the highest
  existing number. An ADR is
  written only when measured evidence justifies committing to a method,
  retiring a branch, or rescoping an earlier decision, and every ADR carries
  a **"What would reopen or reverse this decision"** section. Files ending
  in `.codex-draft.md` are evidence drafts kept beside an accepted ADR; they
  do not take a number of their own.
- A resolved hypothesis is not rewritten. Its Status line changes to
  RESOLVED with a pointer to the deciding stage and ADR, and the original
  pre-registration stays frozen below it (see
  `docs/hypotheses/027-context-utilization-and-coherence.md`).
- The section templates are in `.claude/skills/new-hypothesis/SKILL.md` and
  `.claude/skills/new-adr/SKILL.md`. They are written as instructions for a
  tool, but the section lists apply to anyone. Recent examples:
  `docs/hypotheses/027-context-utilization-and-coherence.md` and
  `docs/decisions/0019-phase-6-coherence-is-a-window-limit-longer-context-arm.md`.
- Hypotheses and ADRs are roadmap decisions. To propose new research, open a
  research proposal issue first.

### Honest baselines and negative results

- Every stage must beat an honest baseline under the same corpus, step
  budget and metrics, and the hypothesis or stage record names that baseline.
  In the early lab it is the plain gradient-trained transformer, which the
  README calls the control model.
- A stage record carries the exact command shape, corpus and split, number of
  seeds, trainable parameter count, validation NLL and bits per character,
  any task metric, wall time, the baseline, and an interpretation that says
  what the result proves and what it does not (`CODEX.md`, "Evidence
  Standard").
- Plain validation NLL and task behavior can diverge: a model can lower
  next-character loss while a behavior probe stays at chance. Do not claim a
  method works because a sample looks nice.
- Negative and failed results are evidence and are never deleted. Supersede
  them with a suffixed filename or a dated note ("Superseded on 2026-10-14
  by ...") instead.

### Run outputs and the durable record

- `experiments/**/runs/` is gitignored. Run outputs (`runs/*.jsonl`,
  `runs/*.md`) stay on your machine; the durable record is a hand-written
  stage entry at the end of `experiments/tiny_language_lab/RESULTS.md`,
  headed `## Stage N` and a title, in the format of the latest entries. Every
  number in it comes from a run artifact. Whether to publish `runs/` for
  outside audit is an open question (#20).
- Gitignore-aware search tools (ripgrep, for example) skip `runs/`, so
  search it explicitly.
- Stage numbers and the README's "Next ladder" rung numbers are different
  sequences (Stage 62 is rung 73, for example). Cite both when you
  cross-reference.
- Never commit checkpoints (`*.pt` and `*.onnx` under `artifacts/` are
  ignored), generated corpus payloads (`corpus/*.txt` and `corpus/*.json` are
  ignored; the `*.meta.json` provenance files are tracked), or datasets.
  TinyStories and text8 are not redistributed here; see `NOTICE`.

### The 50 MiB file guard

`.githooks/pre-commit` refuses any commit that stages an added or modified file
larger than 50 MiB, with the message
`pre-commit: refusing staged file over 50 MiB: <path> (<n> MiB)`. Git only runs
it after you point your clone at the hooks folder:

```
git config core.hooksPath .githooks
```

Please do not bypass it with `--no-verify`. A large blob that reaches history
stays there until the history is rewritten.

### One implementation doc per meaningful change

Experiment results go into `RESULTS.md` as stage entries. Any other meaningful
change, to code, tooling, process or the structure of the docs, gets one
implementation doc at `docs/implementations/YYYY-MM-DD-slug.md`, with these
sections:

1. **Problem / Motivation** · why the change was needed.
2. **What Changed** · a table with one row per file and a one-sentence
   description.
3. **Implementation Approach** · how it was done.
4. **Mathematical / Statistical Details** · every formula or statistical
   test in plain words, or "None".
5. **Design Decisions** · the alternatives considered and why this one won.
6. **Verification** · concrete steps someone else can run.
7. **Related Docs**.

`docs/implementations/2026-06-24-claude-code-automation-setup.md` and
`docs/implementations/2026-10-14-org-move-links-and-header.md` show the
format. A typo fix does not need one.

### Code

- Python 3, four-space indentation, type hints where the surrounding code
  uses them.
- Keep `cassandra_compare.py` beside `cassandra_tiny_transformer.py`: the
  runner imports the trainer as a sibling module.
- To add a named comparison, add a branch in `config_args` in
  `cassandra_compare.py` and register the name in the `--configs` choices.
  Follow the existing names (for example `count_prior_lora_r2_copyw_floor`).
- Run a short smoke test before any long run.
- Before opening a PR, run `python -m pytest` from the repository root; see
  the [CPU helper test setup](experiments/tiny_language_lab/README.md#cpu-helper-tests).
- Check that every Python file still parses (from the repository root):

```
python -c "import ast, pathlib; files = sorted(pathlib.Path('.').rglob('*.py')); [ast.parse(p.read_text(encoding='utf-8'), str(p)) for p in files]; print(len(files), 'files parse')"
```

## How the role files divide the work

The owner runs the project with three AI collaborators, each with its own role
file and lane:

| File | Owns | Typically writes |
| --- | --- | --- |
| `CLAUDE.md` | Hypotheses, ADRs, roadmap and prioritization | `docs/hypotheses/`, `docs/decisions/`, phase reports |
| `CODEX.md` | Implementation, runs, verification, durable evidence | Code under `experiments/tiny_language_lab/`, `RESULTS.md` stage entries |
| `GEMINI.md` | Prior art and outside baselines | Notes under `research/`, source anchors in `docs/LOW_HARDWARE_LM_RESEARCH.md` |

Three more files sit beside them. `AGENTS.md` holds the general repository
guidelines (structure, commands, style, pull request expectations).
`INSTRUCTIONS.md` describes how the owner works and the bar for "done".
`AGENT.md`, without the S, is not a role file: it is the prose track described
at the top of this guide. Handoffs between the lanes travel as files in the
repository, for example `docs/phase6-codex-goal-prompt.md`, and `.claude/`
holds the hooks, skills and subagents used in the owner's Claude Code
sessions.

As a person you are not bound to one lane, but your contribution has to meet
the standard of the lane it lands in. A code change meets the `CODEX.md`
evidence standard. A hypothesis meets the `CLAUDE.md` one, including the
pass-or-fail line. A prior-art note meets the `GEMINI.md` one: source title
and link, date checked, what the source actually claims, what is directly
relevant and what is only an analogy, and how it should change the roadmap.
The role files and their lanes are the owner's to change; propose a change in
an issue first and expect review on wording.

## Pull request flow

1. **Issue first** for anything beyond a typo or a one-line fix, so the scope
   is agreed before you spend time. Pick the matching issue form; new
   research goes through the research proposal form. Comment on an existing
   issue to take it.
2. **Branch.** Fork the repository and branch from `main` with a short
   descriptive name, such as `docs/fix-stage58-lineage`.
3. **Change only what the issue asks for.** The issue's "Not in scope" list
   is binding.
4. **Commit messages** are concise and imperative or evidence-focused, for
   example `Record Stage 41 forced-choice probe`.
5. **Open a pull request** against `main`. The template asks for what changes,
   the issue it closes (`Closes #N`), the evidence (the exact commands you ran
   and the output that matters: metrics, artifact paths, OS, Python and torch
   versions, device), the docs and records you updated, and the style checks
   above. Add screenshots only for visual artifacts.
6. **Review.** The owner reviews and merges; merging is the owner's call.

## Licence

CASSANDRA is licensed under the Apache License 2.0 (`LICENSE`). Under its
section 5, unless you explicitly state otherwise, any contribution you
intentionally submit for inclusion is licensed under the same terms.

`NOTICE` holds the copyright line and the third-party lineage (the Muon
optimizer path, MIT licensed) and dataset provenance. If you adapt
third-party code, keep its licence notice, make sure the licence is compatible
with Apache-2.0, and add an entry to `NOTICE` in the same pull request. To
cite the project, use `CITATION.cff`.

## Conduct, security and support

- **Code of conduct:** the organisation-wide
  [code of conduct](https://github.com/Cassandra-Collective/.github/blob/main/CODE_OF_CONDUCT.md)
  applies to issues, pull requests and every other project space.
- **Security:** please do not open a public issue for a vulnerability. Report
  it privately at
  <https://github.com/Cassandra-Collective/CASSANDRA/security/advisories/new>;
  the [security policy](https://github.com/Cassandra-Collective/.github/blob/main/SECURITY.md)
  explains what happens next.
- **Questions and help:** ask open questions in
  [Discussions Q&A](https://github.com/Cassandra-Collective/CASSANDRA/discussions/categories/q-a),
  where anyone can answer and the answer that settles a question can be
  marked as accepted. When a question should be tracked as an issue, for
  example because its answer will need a change to the code or the docs, use
  the **Question** form on the new-issue page instead. The
  [support page](https://github.com/Cassandra-Collective/.github/blob/main/SUPPORT.md)
  explains what to expect.
