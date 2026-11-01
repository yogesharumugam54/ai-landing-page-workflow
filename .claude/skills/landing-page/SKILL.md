---
name: landing-page
description: Build a responsive single-file landing page from a filled-in brief, then verify it with the checker. Use when asked to create or redo a landing page from a brief and a design reference.
---

# Landing page workflow

## Inputs
- A brief in /brief (see brief.template.md)
- Optional design reference in /reference (layout only)

## Steps
1. Read the brief fully. List the required sections and content rules.
2. If a reference exists, describe its layout in 5 bullets (section order, grid, spacing, button style). Do not copy text, images, logos or colours.
3. Write the copy first: headline (within the word limit), subheadline, benefits, steps, FAQ, CTA. Match the brand voice. Avoid the banned words. No invented facts.
4. Build /output/index.html:
   - one file, inline CSS, no external fonts, scripts or images
   - viewport meta tag, title, meta description, one h1
   - every required section as `<section id="...">`
   - mobile first, readable at 360px width and up
   - accessible: semantic tags, alt text on images, visible focus states, good contrast
5. Run the checker. Fix every FAIL, then re-run until it passes.
6. Report: what was built, checker output, anything the human must confirm (claims, links, legal text).

## Quality bar
- Mobile first, no horizontal scroll
- CTA appears in the hero and at the bottom
- Copy is specific and plain, not hype
- Needs human review before publishing; for WordPress paste the page into a Custom HTML block or use it as a template
