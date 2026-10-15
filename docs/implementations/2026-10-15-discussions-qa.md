# 2026-10-15 · Questions go to Discussions Q&A

## Problem / Motivation

On 2026-10-15 the owner turned on GitHub Discussions in every repository of the Cassandra-Collective organisation. This repository now has the default categories, including **Q&A**, the one category whose threads can have an answer marked as accepted: <https://github.com/Cassandra-Collective/CASSANDRA/discussions/categories/q-a>.

Nothing pointed there yet. The "Questions and support" link on the new-issue page led to the organisation support page, and `CONTRIBUTING.md` sent every question to the **Question** issue form. A question that only needs an answer therefore became an issue that someone had to label and close, and the answer was harder to find again. The 2026-10-14 contributor files doc had anticipated this: its decision on `blank_issues_enabled` names Discussions being enabled to take questions as a reopen condition.

## What Changed

| File | Description |
| --- | --- |
| `.github/ISSUE_TEMPLATE/config.yml` | The "Questions and support" contact link becomes "Ask a question", pointing at this repository's Discussions Q&A, with an `about` line saying open questions and help go there; the security and code of conduct links and `blank_issues_enabled: false` are unchanged. |
| `CONTRIBUTING.md` | The "Questions and help" item in "Conduct, security and support" points first at Discussions Q&A, keeps the **Question** form for a question that should be tracked as an issue, and still links the support page. |
| `docs/implementations/2026-10-15-discussions-qa.md` | This document. |

## Implementation Approach

Two text edits. In `config.yml` the third contact link is replaced in place, so the order on the new-issue page stays security, conduct, questions. In `CONTRIBUTING.md` only the questions item changes; the two items above it are untouched.

The guide now gives two routes with one rule for choosing: an open question that needs an answer goes to Discussions Q&A; a question that should be tracked, for example because its answer will need a change to the code or the docs, goes through the Question form, which applies the `question` label. The form itself (`.github/ISSUE_TEMPLATE/question.yml`) is not changed.

## Mathematical / Statistical Details

None: links and wording only.

## Design Decisions

- **Replace the support link rather than add a fourth one.** The support page is organisation-wide and mostly says where to ask; with Q&A on, the direct route is more useful on the new-issue page. `CONTRIBUTING.md` still links the support page for what to expect.
- **Keep the Question form.** Some questions are bug reports or doc gaps in disguise, and those belong in the tracker with a label. Removing the form would also leave no tracked route for a question, since blank issues are off.
- **Link the Q&A category, not the Discussions front page.** The category URL opens the list of Q&A threads, and a discussion started there can have an answer marked.
- **The 2026-10-14 contributor files doc is not edited.** It is a dated record; its statement that Discussions were disabled was true that day. This document records the change and is linked from Related Docs.
- **No issue.** The change applies an owner decision of 2026-10-15 to repository metadata, as pull request #23 did for the decision to turn blank issues off.

## Verification

Run on 2026-10-15 on Windows 11, from the repository root, with Python `3.13.14` and PyYAML `6.0.3` (the repository does not depend on PyYAML).

1. **`config.yml` parses and keeps its keys:**

   ```
   python -c "import yaml; d = yaml.safe_load(open('.github/ISSUE_TEMPLATE/config.yml', encoding='utf-8')); print(sorted(d), d['blank_issues_enabled'], [(l['name'], sorted(l)) for l in d['contact_links']])"
   ```

   prints the keys `blank_issues_enabled` and `contact_links`, `False`, and three links (`Report a security vulnerability`, `Code of conduct`, `Ask a question`), each with exactly `about`, `name` and `url`.
2. **The Q&A link resolves:** `curl -s -o /dev/null -w "%{http_code}" https://github.com/Cassandra-Collective/CASSANDRA/discussions/categories/q-a` prints `200` signed out.
3. **No em or en dashes** in the three changed files: the dash check from `CONTRIBUTING.md` ("Prose style") lists none of them.
4. **Scope:** `git diff --stat main` lists only the three files in the table above.

**After merge:** open "New issue" on GitHub and confirm the chooser shows the five forms, the three contact links with "Ask a question" last, and no blank-issue option.

## Related Docs

- `docs/implementations/2026-10-14-contributor-files.md` (the issue forms, `config.yml`, and the `blank_issues_enabled` decision with its reopen condition)
- Discussions Q&A: <https://github.com/Cassandra-Collective/CASSANDRA/discussions/categories/q-a>
- Organisation support page: <https://github.com/Cassandra-Collective/.github/blob/main/SUPPORT.md>
