# AI Landing Page Workflow (Claude Code)

A repeatable workflow for turning a **brief + design reference** into a **responsive, single-file landing page**, then verifying it with an automated checker. Built so a team can reuse it for every new page without starting from scratch.

> The sample brand, "Northwind Coffee", is fictional. The page in `output/` is a sample generated from `brief/example-brief.md`.

## How it works

```
brief (what to say) + reference (layout only)
        |
        v
Claude Code + skill (.claude/skills/landing-page)
        |
        v
output/index.html  --->  checks/check_page.py  --->  PASS / FAIL list
        |
        v
human review  --->  paste into WordPress (Custom HTML block) or use as a template
```

1. Copy `brief/brief.template.md`, fill it in (brand voice, goal, sections, rules, banned words).
2. Optionally add a layout reference screenshot to `reference/` (layout only, never copy text, logos or brand colours).
3. Open the repo in Claude Code and ask: *"Build the landing page from brief/my-brief.md using the landing-page skill."*
4. The skill writes `output/index.html` and runs the checker, fixing any FAIL.
5. A human reviews claims, links and legal text before publishing.

## Automated quality checks

```
python checks/check_page.py output/index.html brief/example-brief.md
```

Standard library only, no installs. It checks: mobile viewport tag, title and meta description, one h1 within the headline word limit, every required section, alt text on images, empty links, placeholder text, banned words from the brief, CTA repeated, and no external requests. Exit code is 1 if any check fails, so it can run in CI.

## Files

| Path | Purpose |
|---|---|
| `CLAUDE.md` | Project rules Claude Code follows every time |
| `.claude/skills/landing-page/SKILL.md` | The reusable build workflow |
| `brief/brief.template.md` | Blank brief to copy |
| `brief/example-brief.md` | Filled example |
| `checks/check_page.py` | Quality checker |
| `output/index.html` | Sample generated page |

## WordPress

The page is one self-contained HTML file (inline CSS, no external requests). Paste it into a Custom HTML block, or use it as the basis for a theme template.

## Limits

- This is a workflow and a sample, not a production design system.
- The checker catches structural and rule problems, not taste. Always review the result.
- The brief says "no invented statistics or testimonials"; the human must still confirm every claim.

## License

MIT
