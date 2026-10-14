# 2026-10-14 · Contributing guide, issue forms and pull request template

## Problem / Motivation

On 2026-10-14 the owner asked for a contributing guide, a code of conduct and
issue and pull request templates in every repository of the Cassandra
Collective, to attract open-source contributors. The same day a 19-issue
backlog (#3 to #21) was opened here, labelled `good first issue`,
`help wanted` and `research`, with a release milestone. Nothing yet told a
newcomer how to work in this repository:

- The house rules (no em or en dashes, seeds `7 11 19`, falsifiable
  hypotheses and ADRs with reopen conditions, honest baselines, negative
  results kept, `runs/` gitignored with a hand-written `RESULTS.md`) are
  written into the role files for the owner's AI tools (`CLAUDE.md`,
  `CODEX.md`, `GEMINI.md`, `AGENTS.md`, `INSTRUCTIONS.md`). The only automatic
  style check, `.claude/hooks/check_md_dashes.py`, runs inside Claude Code
  sessions only, and the 50 MiB guard in `.githooks/pre-commit` runs only after
  `git config core.hooksPath .githooks`, which a fresh clone does not have.
  A human contributor never sees either.
- The repository had no `.github/` directory, so issues arrived without
  structure and pull requests without a checklist.
- The first command in `README.md` fails on a fresh clone with a
  `FileNotFoundError` because `corpus/tiny_seed.txt` is not in the repository
  (#3), and nothing documented the workaround.

## What Changed

| File | Description |
| --- | --- |
| `CONTRIBUTING.md` | New guide for human contributors: what the project is and is not, a verified quick start, where to find work, the house rules with their sources, how the role files divide the work, the pull request flow, the licence, and links to the organisation's code of conduct, security policy and support page. |
| `.github/ISSUE_TEMPLATE/bug_report.yml` | Issue form for broken code, scripts or documented commands; asks for exact commands, commit, environment and device, and whether a recorded result could change; labels `bug`. |
| `.github/ISSUE_TEMPLATE/enhancement_or_task.yml` | Issue form in the maintainers' task shape (Context, Task, Acceptance criteria, Pointers, Not in scope); labels `enhancement`. |
| `.github/ISSUE_TEMPLATE/research_proposal.yml` | Issue form for experiments, replications and probes: hypothesis, the stage it builds on, arms and baseline, pass and fail criteria written before the run, compute needed, what it would not prove, prior art; labels `research`. |
| `.github/ISSUE_TEMPLATE/documentation_problem.yml` | Issue form for wrong, stale, unclear or off-style docs, with the location and the evidence for the correct version; labels `documentation`. |
| `.github/ISSUE_TEMPLATE/config.yml` | Turns blank issues off (see the update under Design Decisions) and adds three contact links: the private vulnerability report, the code of conduct and the support page. |
| `.github/ISSUE_TEMPLATE/question.yml` | A Question form (label `question`), copied from the organisation default, added with the update under Design Decisions. |
| `.github/pull_request_template.md` | Pull request checklist: what changes, the issue it closes, evidence (commands and output), docs and records updated, style and safety checks, and a note for role-file changes. |
| `README.md` | A short "Contributing" section appended after the last "Next ladder" rung; the header block is untouched. |
| `docs/implementations/2026-10-14-contributor-files.md` | This document. |

## Implementation Approach

**Rules collected, not invented.** Every rule in `CONTRIBUTING.md` restates
something already in the repository, rewritten for people:

| Rule in CONTRIBUTING.md | Source |
| --- | --- |
| Prose style, numbers, absolute dates, scoped claims | `INSTRUCTIONS.md` section 2; `CLAUDE.md` "Prose style"; `.claude/hooks/check_md_dashes.py` (the `AGENT.md` exemption) |
| Dash check one-liner | Acceptance criteria of #6 |
| Seeds and fixed corpus seeds | `CLAUDE.md` "Determinism is load-bearing"; `--seeds` default in `cassandra_compare.py`; generator commands in `CLAUDE.md` |
| CPU and CUDA as separate measurement families | `CLAUDE.md` and `CODEX.md` "Conventions and gotchas" |
| Chunked evaluation for closeout claims | ADR 0014; `INSTRUCTIONS.md` section 1 |
| Hypothesis and ADR numbering, pass-or-fail line, reopen condition | `INSTRUCTIONS.md` section 1; `.claude/skills/new-hypothesis/SKILL.md`; `.claude/skills/new-adr/SKILL.md` |
| Evidence standard, honest baselines, negative results kept | `CODEX.md` "Evidence Standard"; `CLAUDE.md` "Conventions and gotchas"; `README.md` (the control model) |
| `runs/` gitignored, `RESULTS.md` as the durable record | `.gitignore`; `CLAUDE.md`; `.claude/skills/new-stage-entry/SKILL.md` |
| 50 MiB guard | `.githooks/pre-commit`; `docs/phase5-d2-prep-status.md` (local `core.hooksPath`) |
| Implementation doc sections | The two existing docs in `docs/implementations/` |
| Code conventions, commit messages, pull request contents | `AGENTS.md` |
| Role lanes | `CLAUDE.md`, `CODEX.md`, `GEMINI.md`, `INSTRUCTIONS.md` section 1, `README.md` "Collaboration workflow" |
| Licence and attribution | `LICENSE` section 5; `NOTICE`; `CITATION.cff` |

**Quick start.** The guide gives one command sequence that works on a fresh
clone today without changing any code: enable the hook, generate the
structured corpus with `make_synthetic_corpus.py`, then pass `--corpus` to the
bigram lab and to a CPU transformer smoke test. It names #3 as the known
issue rather than fixing it.

**Issue forms.** GitHub issue forms (YAML) rather than Markdown templates, so
required fields are enforced and every form applies exactly one existing type
label. The enhancement form copies the section shape the maintainers already
use for task issues. The research form encodes pre-registration: the pass
and fail criteria field is required and its label says "written before the
run", and a required dropdown records whether anything has already been run.

**Organisation defaults linked, not copied.** The code of conduct, security
policy and support page are linked at their canonical URLs in
`Cassandra-Collective/.github`, from `CONTRIBUTING.md` and from `config.yml`.
The security contact link points at this repository's private vulnerability
report form, since private vulnerability reporting is enabled here.

## Mathematical / Statistical Details

None. This change adds documentation and repository templates only.

## Design Decisions

- **Owner's decisions of 2026-10-14.** The code of conduct, security policy
  and support page are organisation defaults in `Cassandra-Collective/.github`,
  so one text serves every repository. This repository gets its own
  `CONTRIBUTING.md`, issue forms and pull request template, because its rules
  are project-specific, and it links to the organisation files instead of
  copying them. Private vulnerability reporting is enabled on this repository.
- **Dependency on the `.github` pull request.** The three organisation links
  resolve only after the community-health pull request in
  `Cassandra-Collective/.github` merges. When this document was written, that
  repository's `main` held no `CODE_OF_CONDUCT.md`, `SECURITY.md` or
  `SUPPORT.md`, so those links return 404 until then. That pull request should
  be merged first.
- **`blank_issues_enabled: true`.** Discussions are disabled on this
  repository, maintainers use the `question` label (#20), and the support page
  lives in another repository whose final text was not available when this was
  written. Keeping blank issues gives questions and reports that fit no form a
  path in; the four forms still appear first in the chooser. The alternative,
  `false`, would force every report into a form but could strand questions.
  Reopen condition: if blank issues routinely arrive that should have used a
  form, or Discussions is enabled to take questions, switch to `false`.

  **Update, 2026-10-14 (owner):** blank issues are turned off in every
  repository of the organisation. To keep a path for questions, this
  repository gains the organisation's Question form (`question.yml`, label
  `question`), and CONTRIBUTING.md points questions at it instead of at a
  blank issue.
- **Type labels only.** Each form applies one type label and no `area:`
  label, because a form cannot know the area: a documentation problem can sit
  in `docs/` (`area: docs`) or in the model card (`area: release`). The
  maintainers add the area when they triage. No new labels were created;
  labels and settings are the owner's.
- **No title prefixes.** The existing issues have plain imperative titles, so
  the forms set no `[Bug]`-style title prefix.
- **Work around #3, do not fix it.** Fixing the scripts and the README quick
  start blocks is #3's scope and a `good first issue`; this pull request leaves
  it to a newcomer and only documents the workaround.
- **One command form for both shells.** The quick start uses forward-slash
  paths, which were run unchanged in PowerShell and in Git Bash, instead of
  two parallel blocks.
- **`CONTRIBUTING.md` at the repository root.** It is the most visible
  location, and GitHub finds the file there as well as in `.github/`.
- **Stage results and implementation docs.** `CLAUDE.md` ("Documentation
  home") says new findings go into `RESULTS.md` rather than a separate
  per-change doc, while `docs/implementations/` holds docs for tooling and
  structural changes. `CONTRIBUTING.md` states the division that both imply:
  experiment results go into `RESULTS.md`, and any other meaningful change gets
  one implementation doc. `CLAUDE.md` itself was not edited, because the role
  files are the owner's to change.
- **No single stage-heading pattern prescribed.** `RESULTS.md` headings vary
  (`18` of `97` use the `## Stage N - Title` form), so the guide asks for
  `## Stage N` and a title in the format of the latest entries.
- **README edit kept to the end of the file.** Pull request #2 changes the
  README header line, so this change appends a section after the last ladder
  rung and does not touch the header block.
- **Left to their own issues.** A CI workflow for the dash, syntax and size
  checks (#13), a requirements file (#8) and a test suite (#12) are referenced
  from the guide, not added here.

## Verification

Run from the repository root unless stated.

1. **Issue forms parse and are well formed.** With an interpreter that has
   PyYAML (here Python `3.13.14` with PyYAML `6.0.3`; the repository does not
   depend on PyYAML), load each file with `yaml.safe_load`. A checker script
   also confirmed: `name`, `description` and `body` present; only known
   element types and attribute keys; every `id` unique and made of letters,
   digits, `-` or `_`; every element label unique within its form; markdown
   elements carry only `attributes.value`; `validations.required` is a boolean
   and is not used on checkboxes; dropdown options are unique non-empty
   strings; `config.yml` has a boolean `blank_issues_enabled` and three
   contact links, each with `name`, `url` and `about`. Result: no problems in
   the five files. GitHub's own schema was not run; GitHub validates the forms
   when they are viewed on the default branch.
2. **Every label exists.** The forms use `bug`, `enhancement`, `research` and
   `documentation`; all four are in
   `gh label list -R Cassandra-Collective/CASSANDRA`.
3. **No em or en dashes** in any added or changed file, Markdown or YAML:

   ```
   python -c "import pathlib, sys; fs = ['CONTRIBUTING.md', 'README.md', '.github/pull_request_template.md', 'docs/implementations/2026-10-14-contributor-files.md'] + [str(p) for p in pathlib.Path('.github/ISSUE_TEMPLATE').glob('*.yml')]; [print(f, i) for f in fs for i, l in enumerate(pathlib.Path(f).read_text(encoding='utf-8').splitlines(), 1) if '\u2014' in l or '\u2013' in l]"
   ```

   prints nothing.
4. **The quick start works on a fresh clone** (Windows 11, Python `3.13.14`,
   torch `2.12.1+cu126`, run in both PowerShell and Git Bash on 2026-10-14;
   the clone from GitHub was made in Git Bash, and the PowerShell run used a
   fresh local clone of the same commit): without `--corpus`, `cassandra_tiny_lm.py --method count` stops with
   `FileNotFoundError` naming `corpus/tiny_seed.txt` (#3);
   `make_synthetic_corpus.py --lines 320 --seed 20260616` writes
   `structured_seed.txt` (`25586` chars); the bigram lab with `--corpus` prints
   `val_bits_per_char` `2.91429`; the CPU transformer smoke completes 20 steps;
   `git status` stays clean because the corpus is gitignored.
5. **The 50 MiB guard is real.** In a throwaway clone with
   `git config core.hooksPath .githooks`, staging a 51 MiB file made
   `git commit` exit `1` with
   `pre-commit: refusing staged file over 50 MiB: big.bin (51 MiB)`, and a small
   file committed normally. A fresh clone has no `core.hooksPath` set.
6. **The other checks in the guide run.** The AST one-liner reports
   `44 files parse`; the dash one-liner from #6 prints the twelve research
   notes listed in #6 and nothing else.
7. **Scope.** `git diff --stat main` lists only the files in the table above,
   and `git diff main -- README.md` has one hunk, after line 667; line 1 is
   unchanged.
8. **Links.** The three label pages and `milestone/1` returned HTTP 200
   signed out; the vulnerability report form returned 302 (the sign-in
   redirect, expected when signed out). The three organisation links return
   404 until the `.github` pull request merges (see Design Decisions).

**After merge:** open "New issue" on GitHub and confirm the chooser shows the
five forms (with the Question form), the three contact links and no blank-issue option, and open a
draft pull request to see the template.

## Related Docs

- `CONTRIBUTING.md` (the guide this change adds)
- `AGENTS.md`, `INSTRUCTIONS.md`, `CLAUDE.md`, `CODEX.md`, `GEMINI.md`
  (the sources of the house rules)
- `docs/implementations/2026-06-24-claude-code-automation-setup.md` (the dash
  hook and its `AGENT.md` exemption)
- Issues #3 (missing default corpus), #6 (remaining dashes), #8
  (requirements file), #12 (test suite), #13 (CI checks), #20 (publishing
  `runs/`)
- Organisation community-health files:
  <https://github.com/Cassandra-Collective/.github>
- GitHub documentation on issue forms:
  <https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/syntax-for-issue-forms>
