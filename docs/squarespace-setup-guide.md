# Squarespace Editor Walkthrough

Step-by-step guide to actually building the site in the Squarespace editor
from the content already prepared in `/content` and `/docs`. Written for
Squarespace's newer unified editor (Fluid Engine); menu labels may vary
slightly by template/version, but the structure holds.

## 0. Before you start
- Have `content/homepage.md`, `about.md`, `pricing.md`, `prints-albums.md`,
  `contact-and-emails.md`, and `portfolio-structure.md` open in another tab
  — you'll be copy-pasting from these.
- Have your curated photo selects ready in folders on your computer, named
  by category, matching `portfolio-structure.md` (e.g. `01-portraits/`,
  `02-families-groups/`, etc.) so upload order is fast.
- Confirm your template supports a Portfolio/gallery page type — most
  photography-oriented Squarespace templates do natively.

## 1. Site-wide setup first
1. **Settings → Design → Logo & Title** — upload the confirmed EaleyImages
   logo (gold/bronze camera emblem). Set it as both header logo and
   browser favicon (Settings → Design → Favicon — crop to the circular
   emblem for a clean small-size render).
2. **Settings → Design → Fonts & Colors** — keep it minimal: 1–2 fonts max,
   a neutral/editorial palette (black, white, warm neutral) to match the
   "clean, editorial, premium" brand direction. Avoid busy template
   accent colors.
3. **Pages panel → add the 6 primary nav pages** first as empty pages so
   the nav structure exists before you fill content:
   Home · Portfolio · Services & Pricing · Prints & Albums · About ·
   Contact
   (Home and a Not Linked section for legal/policy pages if needed.)
4. **Settings → Design → Navigation** — order the nav exactly as above;
   Squarespace auto-populates it from your page list, so ordering there
   determines the header order.

## 2. Build the Portfolio section
Per `docs/sitemap.md`, use child pages under a Portfolio parent for SEO.
1. Create the **Portfolio** page as a parent/folder (Squarespace calls
   this a "Page Group" or "Folder" depending on version).
2. Under it, add one gallery page per category from
   `content/portfolio-structure.md`:
   Portraits · Families & Groups · Grad & Prom · Corporate & Branding ·
   Events · Mini Sessions
   (Weddings & Proposals and Lifestyle & Scenes are optional bonus
   galleries — add only if you want them public; they're portfolio-only,
   not linked to bookable services.)
3. For each gallery page: use a **Gallery** section/block (grid or
   masonry layout — grid reads cleaner for an editorial look). Upload the
   curated selects for that category in the order noted in
   `portfolio-structure.md`.
4. **Every image**: set the alt text before publishing (image settings →
   "Alt Text") using the pattern from `content/seo-keywords.md`, e.g.
   "Cary NC senior portrait outdoor session" — not the raw filename.
5. **Page Settings → SEO** for each gallery page: set the title and meta
   description from `content/seo-keywords.md`.

## 3. Home page
Work top to bottom through `content/homepage.md`:
1. **Hero section** — full-bleed image block, headline + subheadline as
   overlaid text, two buttons ("Book a Session" → links to Contact page;
   "View Portfolio" → links to Portfolio page).
2. **Intro/Philosophy** — a simple text block, centered, with a text link
   to About.
3. **Services grid** — a 6-column/2-row grid block (or repeating
   image-with-caption blocks), one per service category, each linking to
   its anchor on the Services & Pricing page (see step 4 below for how to
   set anchors).
4. **Portfolio teaser** — a gallery block set to a fixed small set of
   images (6–9), linking out to the full Portfolio page.
5. **Testimonial** — leave a placeholder text block for now; swap in a
   real quote once you have one.
6. **Closing CTA band** — full-width color/image block with the "Book a
   Session" button.
7. **Page Settings → SEO**: title/description from `content/seo-keywords.md`.

## 4. Services & Pricing page
This is one long scrollable page with anchored sections, built from
`content/pricing.md`.
1. Add a text/heading block for each category (Portraits, Families/
   Groups, Grad & Prom, Corporate, Events, Mini Sessions, Add-Ons,
   Booking & Payment Policy) in that order.
2. For each package, use a simple heading + line-item format matching the
   pricing doc (Squarespace's built-in "Pricing" block works well if your
   template has one; otherwise plain text blocks with bold package names
   are fine).
3. **Set section IDs/anchors**: in each section's block settings, add a
   custom anchor ID (e.g. `#portraits`, `#families`, `#corporate`,
   `#events`, `#mini-sessions`). Then go back to the Home page services
   grid and point each tile's link to `/services-and-pricing#portraits`
   etc. so clicking "Portraits" on Home jumps straight to that section.
4. Add the Booking & Payment Policy text at the bottom, verbatim from the
   pricing doc.
5. **Page Settings → SEO**: title/description from `content/seo-keywords.md`.

## 5. Prints & Albums page
1. Build from `content/prints-albums.md` — either as a standard content
   page (simplest) or as a Squarespace Store page if you want actual
   checkout/purchase flow through Square.
2. If using it as an upsell reference page only (no direct checkout),
   plain product-style blocks (image placeholder + name + price + one-line
   description) per item work fine.
3. Closing CTA links to Contact.
4. **Page Settings → SEO**: title/description from `content/seo-keywords.md`.

## 6. About page
1. Build from `content/about.md` top to bottom.
2. Use the confirmed photographer photo (gear-in-hand shot, per
   `portfolio-structure.md`) as the primary image.
3. Optional: add 1–2 behind-the-scenes shots (lighting setup, working a
   session) in a small supporting image block under the "The Experience"
   section — these were flagged as good process-section material.
4. **Page Settings → SEO**: title/description from `content/seo-keywords.md`.

## 7. Contact page
1. Build from `content/contact-and-emails.md`.
2. Add Squarespace's built-in **Form Block** with fields: Name, Email,
   Session Type (dropdown — use the six service categories), Preferred
   Date, Message. Set form submissions to email
   lannyealeyphotography@gmail.com (Form Block settings → Storage →
   Email Notifications).
3. Add the direct email and service-area line as plain text below the
   form.
4. Link "booking policy" text to `/services-and-pricing#booking-policy`.
5. **Page Settings → SEO**: title/description from `content/seo-keywords.md`.

## 8. Footer (site-wide, once)
Settings → Design → Footer (or edit the footer section directly on any
page — it's shared site-wide):
- Logo mark (small version)
- Repeat nav links
- Contact email
- Service area line: "Based in Cary, NC · Serving RTP & the Triangle ·
  Travel available"
- Social links (add when accounts are ready)
- "Client Gallery Login" text link → your CloudSpot login URL

## 9. Before publishing — checklist
- [ ] Every page has a custom SEO title + meta description set (not the
      Squarespace default)
- [ ] Every portfolio image has real alt text, not a filename
- [ ] Nav order matches the 6-item primary nav
- [ ] Home services grid links jump to the correct pricing anchors
- [ ] Contact form sends to lannyealeyphotography@gmail.com and you've
      sent yourself a test submission
- [ ] Mobile preview checked for the hero, services grid, and galleries
      (Squarespace's mobile editor view) — grids often need re-checking on
      small screens
- [ ] Favicon shows correctly in a browser tab
- [ ] Google Business Profile set up for "EaleyImages" in Cary, NC (per
      `content/seo-keywords.md` — matters more for local search than
      on-page SEO alone)

## 10. Payments note
Per the brand doc, payments run through Square, not Squarespace Commerce.
If you want retainer/deposit collection directly from the site, you'll
likely link out to a Square invoice/checkout link (from the Contact page
or a booking confirmation email) rather than building full Squarespace
Commerce checkout — simplest path given your existing Square setup.
