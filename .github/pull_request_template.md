<!--
Thanks for the pull request. CONTRIBUTING.md explains each item below.
Delete any section that does not apply, and say why if it is not obvious.
-->

## What changes

<!-- One short paragraph: what this pull request changes and why. -->

## Issue

Closes #

<!-- Anything beyond a typo needs an issue first. If this only partly addresses it, write "Part of #N" instead. -->

## Evidence

<!--
The exact commands you ran, from the repository root, and the output that
matters: metrics, artifact paths, JSON fields, test or check output. Give the
OS and shell, the Python and torch versions, and the device (cpu or cuda).
For an experiment, also give the seeds (house default 7 11 19), the baseline
it was compared against, and any known confounds. Screenshots only for
visual artifacts.
-->

```
command
output
```

## Docs and records updated

- [ ] An implementation doc at `docs/implementations/YYYY-MM-DD-slug.md` (any meaningful change that is not a stage record)
- [ ] For a run: a stage entry in `experiments/tiny_language_lab/RESULTS.md`, with every number taken from a run artifact
- [ ] For a run: the hypothesis or ADR it implements is linked, and its pass-or-fail line was written before the run
- [ ] The README or other docs that describe what changed
- [ ] Nothing to update (say why)

## Style and safety checks

- [ ] No em or en dashes in any doc I wrote or changed (the check in CONTRIBUTING.md, "Prose style", lists none of my files)
- [ ] No file over 50 MiB, and the guard is on in my clone (`git config core.hooksPath .githooks`)
- [ ] No checkpoints, generated corpora, datasets or `runs/` outputs committed
- [ ] Every changed Python file still parses (the AST check in CONTRIBUTING.md, "Code")
- [ ] Recorded results are untouched, or superseded with a dated note rather than rewritten

## Role files

<!--
Only if this pull request changes CLAUDE.md, CODEX.md, GEMINI.md, AGENTS.md or
INSTRUCTIONS.md: say what changes in which file and why. The roles and their
lanes are the owner's to change, so expect review on wording. Delete this
section otherwise.
-->
