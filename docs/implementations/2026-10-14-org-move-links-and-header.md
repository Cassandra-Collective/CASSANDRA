# 2026-10-14 · Links to the Cassandra-Collective organisation, and the org header

## Problem / Motivation

On 2026-10-14 this repository moved from the personal account `mertefesensoy` to the organisation `Cassandra-Collective` (first transferred as `CASANDRA-Lab`, then renamed). GitHub redirects the old URLs, but only until a repository is created at the old path; links in a model card and a citation entry should not depend on a redirect. The organisation also gained an identity the same day (the Forecast mark, in `Cassandra-Collective/.github`), and the owner asked for a small "part of the collective" header on each project README.

## What Changed

| File | Description |
| --- | --- |
| `README.md` | A one-line header above the title: the small Forecast mark (light and dark variants) and "Part of the Cassandra Collective", both linking to the organisation. |
| `docs/release/stage61-flagship/MODEL_CARD.md` | Four links to the code repository now point at `Cassandra-Collective/CASSANDRA`, including the BibTeX `url`. |
| `docs/release/stage61-flagship/inference_example.py` | The `git clone` URL in the docstring. |
| `experiments/tiny_language_lab/make_stage61_release.py` | The `code` URL that the release script writes into the release metadata. |
| `docs/phase4-flagship-midrun-report.md` | The repository URL in the note on GitHub's file-size limit. |
| `docs/implementations/2026-10-14-org-move-links-and-header.md` | This document. |

## Implementation Approach

One scripted replacement over every git-tracked text file: `github.com/mertefesensoy/(CASSANDRA|CASSANDRA-Chorus|Ephesus|Dervish)` becomes `github.com/Cassandra-Collective/<same name>`, then a re-grep confirms none remain. Hugging Face paths (`mertefesensoy/cassandra-200m-text8` and its demo Space) are not GitHub and did not move, so they are untouched, as is any other repository under the personal account.

The header loads the mark from the organisation's brand folder by absolute URL (`raw.githubusercontent.com/Cassandra-Collective/.github/main/brand/svg/cassandra-mark-small-on-*.svg`), so a later change to the mark updates every README at once. It uses the **small** mark, which the brand guide prescribes for 24 px and below; the image is 20 px. A `<picture>` element picks the light or dark variant from `prefers-color-scheme`.

## Mathematical / Statistical Details

None: links and markup only.

## Design Decisions

- **Absolute URL to the brand folder, not a copy of the SVG in this repository.** One source of truth for the mark; the cost is that the header depends on `Cassandra-Collective/.github` staying public.
- **Small mark at 20 px, `align="absmiddle"`, no `<sub>`.** The first version (full-height `<sub>` text and whitespace inside the link) rendered a stray underlined space and text below the icon's centre; the final markup centres the 20 px mark on the text line.
- **Dated reports updated too.** `phase4-flagship-midrun-report.md` names the repository in passing; the link was updated because its purpose is to point at the repository, not to record where it once lived.

## Verification

- `git grep -i -E "github\.com/mertefesensoy/(CASSANDRA|Ephesus|Dervish)"` returns nothing after the change; the replacement reported 7 links in 4 files (4 in the model card, 1 each in the other three).
- The README header was viewed on GitHub at commit `0ceffb8` in a signed-out browser: in light mode it loads `cassandra-mark-small-on-light.svg`, in dark mode `cassandra-mark-small-on-dark.svg`; the 20 px mark's vertical centre sits within 3 px of the text line's.

**Not done here:** the copy of the model card already published on Hugging Face (`mertefesensoy/cassandra-200m-text8`) still carries the old links until the next upload, and so does any release metadata already written by `make_stage61_release.py`.

## Related Docs

- Organisation brand guide: <https://github.com/Cassandra-Collective/.github/blob/main/brand/README.md>
