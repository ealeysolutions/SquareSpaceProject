# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

This is a **content package**, not a software project — there is no code, no
build system, no tests, and no dependencies to install. It contains the copy
and planning docs for the EaleyImages Squarespace website (editorial
photography business, Lanny Ealey, based in Cary, NC / RTP / Triangle area).
Everything here is Markdown intended to be read by a human and pasted into
the Squarespace editor.

## Structure and source-of-truth flow

- `docs/content-package-source.md` — **source of truth** for brand facts,
  confirmed pricing, and product details, as provided directly by the
  client. If pricing or service details change, **update this file first**,
  then propagate the change to the corresponding page(s) in `/content`.
- `docs/sitemap.md` — navigation and page-by-page structure plan for the
  Squarespace site.
- `docs/squarespace-setup-guide.md` — step-by-step walkthrough for building
  the site in the Squarespace editor from this content.
- `content/*.md` — page-ready, copy-paste-into-Squarespace content, one file
  per page/section (`homepage.md`, `about.md`, `portfolio-structure.md`,
  `pricing.md`, `prints-albums.md`, `seo-keywords.md`,
  `contact-and-emails.md`).

When asked to change pricing, services, or brand facts, always edit
`docs/content-package-source.md` first, then update the matching sections in
`/content` so the two stay in sync — `content-package-source.md` is
authoritative if they ever disagree.

## Content conventions

- `[ Bracketed text ]` marks a button/CTA.
- *Italic notes* mark where an image goes (images themselves are not stored
  in this repo — see Open Items below).
- Page files in `/content` are written as final, ready-to-paste copy —
  preserve that direct/publishable tone rather than writing in note form.

## Known open items (from README)

- Portfolio images must be uploaded directly to Squarespace; they are not
  persisted to this repo.
- Weddings is intentionally out of scope/omitted — not part of the current
  confirmed pricing sheet.
- Testimonials are placeholders pending real client quotes.
