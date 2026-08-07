# Contributing

One rule covers almost everything: **every claim lands with a first-party URL and a `checked`
date, or it does not go in.**

## First-party means first-party

A row is only as good as its evidence. In order of strength:

| `evidence_type` | What it means |
|---|---|
| `public repos` / `public repo` | a repository under the vendor's own GitHub org — the strongest evidence here |
| `public org listing` | the vendor's org page, used to establish that something is *absent* |
| `vendor doc` | the vendor's own documentation |
| `vendor page` | a marketing page. Weakest. Flag it as such rather than upgrading it |

**Another roundup is not evidence.** If the only source for a claim is a blog comparing tools,
the claim does not go in — that is how the errors in this category propagate.

## Absence claims need a stronger source than presence claims

Saying "vendor X has no MCP server" is a claim about the whole world and cannot be fully proven.
The standard used here is: the vendor's own org listing, on a stated date, with the repo count
recorded. Anyone can re-run it. If you find a first-party server that a row says does not exist,
that PR is the most valuable one you can open.

## Deprecation is a first-class fact

An archived repo is not the same as no repo, and neither is the same as a working hosted service.
Use `code_access` honestly:

- `yes` — a first-party MCP server or documented agent endpoint exists and is maintained
- `partial` — an API exists but no agent surface; you write the glue
- `deprecated` — it existed and was archived or superseded. Record the date and where it moved
- `no` — nothing first-party found at check date

## Re-checking beats adding

The most useful PR to this repo is not a new agent. It is a `checked` date moved forward on a row
that was already here, with the evidence re-verified — or a row corrected because the vendor
changed something. This category deprecates fast; the value of the list is that its dates are real.

## Out of scope

Scores, rankings by output quality, "best overall" verdicts. Nobody can audit those from the
outside, and putting a number on them is what makes every other list in this category unfalsifiable.
