# Plantly — Landing Page Design System & Section Specification

> **Status:** Design specification / implementation handoff, not a coded page  
> **Version:** 4.0 · November 7, 2026  
> **Scope:** Full-bleed hero, Our Mission (Pain → Promise → Person), Key Features grid, Benefits accordion, and AGRA-inspired footer  
> **Supersedes:** `PLANTLY_FIRST_SCREEN_DESIGN.md` for landing-page implementation decisions  
> **Surface mode:** Persuade (marketing), with authentic product-data previews  
> **Visual north star:** AGRA-inspired full-bleed agricultural hero composition, established Plantly branding and tractor, crisp white feature/benefit sections, and a charcoal multi-column footer.

## 1. Product and design intent

Plantly is a research-backed seasonal growing planner for small farms and home gardeners. It converts information about a plot's soil, crop history, goals, location, and budget into a reasoned growing plan, with cost and weather context. The landing page must feel calm and trustworthy, while the agricultural artwork feels distinctive and cinematic.

**Page progression:**

```text
[ FULL-BLEED HERO / FIRST VIEWPORT ]
    Three-zone navigation: left text links | centered Plantly SVG mark | right actions
    Huge centered 'Plantly' over expansive upper-sky negative space
    Headline, concise description, seven-day trial pill CTA
    Large white tractor / crop-field landscape positioned low in the frame
    Three qualified market/target metrics as subtle bottom-edge overlays
         ↓ normal page scroll (NO growing vine/progress bar)
[ OUR MISSION ]
    Typography-led Pain → Typical Approach → Plantly value bridge
    Home gardeners and small/mid-sized growers as the two audience groups
         ↓
[ KEY FEATURES ]
    Airy white editorial heading + three dark-green image/data cards
         ↓
[ BENEFITS ]
    Numbered accordion, item 01 open, 30/70 explanation + image carousel
         ↓
[ FOOTER ]
    Full-width charcoal panel: brand and email signup on left
    Social row and three link columns on right; bottom divider + legal links
```

**Excluded from this specification:** pricing page, authentication, dashboard, processing animation, unapproved testimonials, and any scroll-based growing plant indicator. It describes visual design, not evidence that future capabilities, newsletter subscriptions or a free trial are already implemented.

### Design references and asset truth

- **NEW definitive hero layout:** `IMG_4368.jpeg` — AGRA agricultural-photo hero: full-bleed image, restrained overlay navigation, centered upper-sky copy and CTA, dominant vehicle low in frame, small bottom-corner support elements. **This supersedes the previous inset-card Origin layout.**
- **Historical hero inspiration:** `IMG_4339.jpeg` / `IMG_4339(1).jpeg` — Origin ocean hero, atmosphere and image storytelling only; no longer the hero layout authority.
- **Approved Plantly symbol:** `premium_spherical_plant_emblem.png`; gold right leaf, integrated green spherical form. It is currently a PNG reference; a true production SVG must be vectorized and visually checked, **not simply renamed**.
- **Existing Plantly hero asset:** `golden_harvest_tractor_at_sunset.png`; the white-tractor artwork stays the current approved subject/background asset, but it may need a re-crop or a revised export to meet the NEW full-bleed, lower-center composition. The AGRA photo is a layout/style reference, not a substitute image to publish.
- **Mission content evidence:** the source PDF and investor conversation; designed as a calm white editorial bridge, rather than duplicating the photo-led Features section.
- **Key Features reference:** `IMG_4362.webp`; white section, centered heading, three tall dark-green photographic cards and inset data-preview glass panels.
- **Benefits reference:** `IMG_4365.webp`; numbered accordion, 30/70 expanded area, nature imagery, UI-overlay first card, visible horizontal carousel progress indicator.
- **NEW footer layout reference:** `IMG_4369.jpeg` — AGRA charcoal footer with brand/story and newsletter on left, social icons and grouped links on right, and a full-width legal bar.
- **Original product evidence:** `Soil-Smart Planner Team Demo.pdf` and `Past Conversation on Plantly investor’s perspective.txt`.

Recreate the **layout grammar, hierarchy, interactions, and visual materiality** of the references. Do not copy third-party logos, text, proprietary illustrations, or claimed measured results.

## 2. Updated color palette — authoritative UI tokens

The **green + charcoal palette remains the authority for UI surfaces**, with an added full-dark footer treatment and image-dependent hero text color. The original Forest/Mist/Harvest tones remain valid in the **approved logo and hero artwork**. Do not recolor the approved visual assets solely to force their pixels to match new UI tokens.

| Semantic token | Hex | Usage |
|---|---|---|
| `--color-brand` | `#1B3625` | Primary emerald/forest: CTAs, card overlays, heading accents, key outlines |
| `--color-brand-hover` | `#244B33` | Primary-button hover and active navigation treatments |
| `--color-brand-bright` | `#4E9F3D` | Active accordion details, small icons, section accents, active visual states |
| `--color-leaf-lime` | `#76B947` | Sparse micro-highlights on dark surfaces, progress accents, small graphic markers |
| `--color-ink` | `#111813` | Primary charcoal headings, high-contrast copy |
| `--color-ink-soft` | `#1E241F` | Dark secondary surfaces, dark cards and overlays |
| `--color-footer` | `#1B1D1B` | Full-width charcoal footer canvas; avoid pure black |
| `--color-footer-muted` | `#B7BDB8` | Footer secondary copy and low-emphasis links |
| `--color-surface` | `#FFFFFF` | Main feature/benefit section backgrounds, paper-like containers |
| `--color-surface-soft` | `#F9F9F9` | Secondary light background, inset surfaces |
| `--color-text-muted` | `#68726B` | Supporting text, captions, descriptions |
| `--color-border` | `#E5EAE6` | Quiet dividers, subtle panel edges and input borders |
| `--color-on-dark` | `#FFFFFF` | Text on deep green/charcoal surfaces |
| `--color-harvest-art` | `#D9AF5F` | Legacy artwork/logo accent only; **not** the new primary UI accent |
| `--color-mist-art` | `#DFE8D8` | Legacy highlight within approved art and optional pale illustration areas |

### CSS token seed

```css
:root {
  --color-brand: #1b3625;
  --color-brand-hover: #244b33;
  --color-brand-bright: #4e9f3d;
  --color-leaf-lime: #76b947;
  --color-ink: #111813;
  --color-ink-soft: #1e241f;
  --color-footer: #1b1d1b;
  --color-footer-muted: #b7bdb8;
  --color-surface: #ffffff;
  --color-surface-soft: #f9f9f9;
  --color-text-muted: #68726b;
  --color-border: #e5eae6;
  --color-on-dark: #ffffff;
  --color-harvest-art: #d9af5f;
  --color-mist-art: #dfe8d8;

  --radius-card: 20px;
  --radius-panel: 14px;
  --radius-control: 10px;
  --page-max-width: 1360px;
}
```

**Color discipline:** Emerald is the signature brand action color. Bright green is a *small accent*, not an entire section background or paragraph text on white. White and charcoal carry most content. Test all text contrast; do not use lime or bright green for small body copy on white. The reference's dark green photographic cards should remain visually dark enough for white copy and readable inset panels.

## 3. Shared visual language

### Typography

- **Default:** Modern sans-serif family with distinctive proportions (e.g. Geist/Outfit, subject to font selection and licensing). Use the same family across hero, sections, labels, and UI previews.
- **Hero brand word:** Very bold, huge live text, around `clamp(80px, 10vw, 160px)` on desktop, adjusted for the AGRA-style centered scene; visual weight should never cover the tractor.
- **Major section headings:** approximately `clamp(36px, 4vw, 56px)`, medium-to-semibold, tight tracking but comfortable line height.
- **Accordion row titles:** `clamp(28px, 3vw, 42px)`, bold/medium, high contrast.
- **Card titles:** `20–24px`; body descriptions `15–17px`; captions and UI previews `12–14px`.
- The reference uses a styled *Operations* word. If applying emphasis, prefer a controlled italic treatment within the chosen headline family; do not introduce a random extra font solely to mimic the screenshot.

### Spacing / geometry

- Max content width: `1360px`, center-aligned.
- Desktop gutters: `48–64px`; tablet `32px`; mobile `20–24px`.
- Vertical space between major below-fold sections: approximately `104–144px` desktop, `64–88px` mobile.
- Standard gaps: `8/12/16/24/32/48px` scale. Avoid arbitrary one-off spacings.
- Large image cards: `18–22px` radius; translucent inner panels `12–16px`; buttons `8–12px`.
- Shadows are restrained and used only to separate a raised UI widget from its photo. Use borders/contrast for most separation.

### Animation

- **No scroll-growing plant or scrolling progress vine.** Normal scroll between sections.
- Below-fold entrance animations, if desired: short opacity/translate reveal (`~300–500ms`), once; never delay content availability.
- Button and accordion motion: `150–250ms` typically; expandable content can use approximately `220–320ms` with reduced-motion support.
- Do not autoplay the benefits carousel.
- `prefers-reduced-motion: reduce` removes nonessential movement.

## 4. First screen — NEW AGRA-inspired visual authority

**Reference:** `IMG_4368.jpeg` is now the **decisive visual-layout reference** for the hero. It has a real agricultural landscape spanning the entire frame; the machinery fills the lower portion, while an unusually open, atmospheric sky holds the main messaging. Plantly retains its **own** approved navigation order, SVG emblem, product name, tractor artwork, offer wording, and qualifying market stats. Do not reproduce AGRA's name, machine, testimonial claims, or other proprietary copy.

### 4.1 Hero layout and visual hierarchy

- **Full-bleed, photo-led canvas** edge-to-edge across the browser width and at least `100dvh` tall on desktop (minimum use `min-height: 100dvh`). **Remove the earlier inset white-page card frame, oversized rounded corners, and outer drop shadow.**
- The image is the product's visual statement, not a small illustration beside the words. Landscape/tractor artwork fills the page; background image goes behind the top navigation, main copy, and bottom metadata.
- Visually organize the viewport into four vertical zones: **(1) navigation, (2) upper-centered headline/copy/CTA, (3) spacious scene with large tractor in the lower-center or lower-center-left, (4) floating bottom-corner metrics**. Keep actual negative space between them; avoid stacking copy directly over the vehicle.
- AGRA-like atmosphere: deep or teal-green tinted sky, soft natural illumination, restrained grain/texture, landscape horizon in the lower third, strong grounded vehicle. This should feel like an immersive agricultural hero rather than a SaaS dashboard, glass card collage, or busy infographic.
- **Subject continuity:** Use Plantly's white/cream tractor with dark-green detailing, working at the boundary of an already-plowed portion (track marks/furrows visible) and an unworked crop area. The tractor is visually prominent, not a small icon. The reference's combine/harvester is *not* the Plantly vehicle.

**Composition sketch — placement only (not a pixel-art target):**

```text
┌───────────────────────────────────────────────────────────────────────────┐
│ Our Mission  Key Features  Benefits       [PLANTLY MARK]   Start Planning │
│                                                            Pricing  Sign Up│
│                                                                           │
│                   [optional tiny credibility eyebrow]                     │
│                                PLANTLY                                    │
│               Stop Guessing Your Soil. Grow Smarter,                      │
│                              Spend Less.                                  │
│                   Concise research-backed explanation                    │
│                      [ Try Plantly Free for 7 Days → ]                    │
│                                                                           │
│                     (open sky / atmospheric field)                        │
│                                                                           │
│                    LARGE WHITE TRACTOR / FIELD                            │
│                                                                           │
│  [ $36B TAM ] [ $9.6B SAM ]                     [ 20% TARGET COST DROP ]  │
└───────────────────────────────────────────────────────────────────────────┘
```

### 4.2 Top navigation — Plantly's exact established structure

| Zone | Contents (exact order) | Appearance / behavior |
|---|---|---|
| **Left** | **Our Mission · Key Features · Benefits** | Small, widely spaced overlay links; use white text where the image has adequate contrast, otherwise a defined darker scrim or approved dark-text variant |
| **Center** | **Approved Plantly SVG mark only** | True horizontal center of the viewport; clickable link to `/`; no Plantly wordmark in navbar |
| **Right** | **Start Planning · Pricing · Sign Up** | Start Planning and Pricing as text links; Sign Up as a compact high-contrast pill (the screenshot's small upper-right light CTA is a useful pattern) |

- Implement header alignment with a real **three-track grid: `1fr auto 1fr`** and independent left/right flex groups; do not visually shift the emblem when the side groups differ in length.
- On desktop use a slim inset padding, roughly `32–64px` from side edges, and `24–34px` from top; do not add a huge opaque app-bar surface.
- Navbar can initially overlay the hero as transparent. If it becomes sticky on scroll, transition to a readable opaque dark/white bar *only* when needed and avoid imposing a second distracting animation.
- Use hover underlines/color or focus rings, not glows. All visible links require working destinations. `Key Features` targets `#features`; `Benefits` targets `#benefits`; `Our Mission` targets `#mission` (the new Mission section in Section 5).
- Mobile: keep SVG mark visually centered, and collapse navigation into an accessible menu; retain an easily discoverable Start Planning action. Do not cramp six labels into one row.

### 4.3 Hero image art direction and contrast

- Current asset: `golden_harvest_tractor_at_sunset.png`, optimized to `hero-tractor-field.webp` / AVIF where supported. The source image is sufficiently open above but positions the tractor lower-left; a **new crop, art-directed responsive variant, or composition adjustment** may be required to mimic AGRA's larger low-center machinery.
- Match `IMG_4368.jpeg`'s *immersion and photographic atmosphere*, not its specific harvester or branding. Prefer a photographic or finely painterly agricultural treatment over conspicuously flat UI illustration when preparing a future asset; do **not** silently replace the approved art without checking with the product owner.
- Use `object-fit: cover` for an `<img>`/`<picture>` background or CSS `background-size: cover`; preserve tractor cabin, wheels, plowed rows, unworked crop, and sky reading area across breakpoints. Consider separate mobile crop/artwork.
- **Text contrast is not optional.** The reference uses white type against a saturated blue-green sky; the existing Plantly image has a much lighter sky. Add a subtle **top-localized dark emerald/teal overlay** or art-direct a darker sky for white copy. If white remains illegible, deliberately switch copy to dark forest over the light sky. Never put low-contrast white copy directly on mint/cream.
- Make overlay gradients localized to text and navbar zones. Leave tractor and vegetation vivid and legible; no heavy all-over dark filter that hides the brand image.

### 4.4 Main copy — centered, high in the sky

Use Plantly's established content, but style and position it like the reference: **a compact, centered copy stack suspended in the upper half of the landscape**, above the machinery rather than sitting in a left-side panel.

1. **Optional eyebrow** — a thin outlined micro-pill, such as `RESEARCH-BACKED SEASON PLANNING`. It is descriptive, not a fake launch or verification badge; omit if it crowds the hierarchy.
2. **Product name** — `Plantly`, by far the largest visible type (desktop starting point `clamp(80px, 10vw, 160px)`). This is live HTML; no word baked into the background asset. Capitalization remains **Plantly**.
3. **Headline** — `Stop Guessing Your Soil. Grow Smarter, Spend Less.` centered and narrower than the product name; usually two lines, potentially three on narrow desktop. The reference's italic emphasis can inspire a *restrained* emphasis on a phrase, but is not mandatory.
4. **Subheadline** — `Custom, research-backed crop plans and input cost tracking tailored to your exact soil and weather.` Limit to about 55–65 characters per line on large screens so it doesn't become a full-width paragraph.
5. **Primary CTA** — `Try Plantly Free for 7 Days`, a **light/white pill** with a small emerald arrow-circle or arrow at right, matching the reference's contrast and compact proportions. This supersedes the old dark rectangular hero CTA style **for this hero only**; brand-green buttons remain correct elsewhere.

**Spacing / positioning:** Desktop hero-copy group begins around 15–21% of viewport height (below header), with tightly controlled gaps and enough space below the CTA for the tractor. This percentage is a *starting point*, not an instruction to force an overlap at short heights. A maximum copy width around `760–900px` is appropriate; the huge name can exceed that width if balanced. The tractor remains the second visual focal point, not a backdrop obscured by heading lines.

**Commercial caveat:** A seven-day free trial is specified as landing copy, not a confirmed active entitlement. Do not ship this CTA as a public offer without supporting trial signup, expiration, billing/auto-renewal terms (if any), and honest route behavior.

### 4.5 Bottom hero support elements — adapt AGRA's corner accents to Plantly metrics

The reference has compact translucent preview cards **bottom-left** and a supporting trust statement **bottom-right**, both integrated into the scene rather than covering it. Plantly has already chosen market/target statistics; use the **same corner-placement grammar**, but present Plantly's own three numbers:

```text
 Bottom left (small floating translucent tiles)          Bottom right (support block)
 ┌───────────────┐  ┌───────────────┐                    ┌────────────────────┐
 │     $36B      │  │     $9.6B     │                    │       20%          │
 │ TAM estimate* │  │ SAM proxy*    │                    │ Cost reduction     │
 └───────────────┘  └───────────────┘                    │ target*            │
                                                        └────────────────────┘
```

- Build these as **real text over small glass/translucent emerald surfaces** (not pre-rendered into the image); very restrained blur/border and excellent contrast. Do not force a large three-column bar across the tractor if it hides the hero image.
- The first two numbers may group at left, while the third sits at right to echo the reference. On large screens they should visually balance the horizon, leaving the tractor clear. On mobile, allow a tidy compact row or an accessible section directly below the crop instead of obstructing the machine.
- Footnote visible on page: `*Historical market proxies; 20% is an unverified savings target.` Do not make market-size claims look like actual customers, revenue or achieved impact. Use links or info-disclosure to cite source/methodology in production.
- The original deck derives an illustrative roughly **$36B TAM** from dated household garden spending and uses a **$9.6B lawn/garden consumables market** figure as a SAM *proxy*, not as audited software-market sizes. The investor conversation treats **15–20%** savings as a potential goal. Never label the 20% as an achieved cost drop.

### 4.6 Hero responsive + technical specifications

- **≥1280px:** edge-to-edge image; transparent three-track nav; centered upper copy; tractor large in lower center/left; floating metrics tucked into lower corners, away from tractor.
- **768–1279px:** trim copy size/gaps first; ensure tractor remains visible; reduce the metric overlay footprint and check against shorter tablet heights.
- **<768px:** art-direct tall crop; center title and copy without covering the tractor. Use a compact navigation control. If all three metrics would obscure the subject, move them immediately below the hero image on the same tonal surface and retain their footnote. The CTA remains in the first viewport where practical.
- **Mobile browser height:** avoid `height: 100vh` as the only rule. Use `min-height: 100dvh` with height allowed to grow naturally for accessibility and large type settings.
- **Performance:** deliver appropriately sized image sources (`srcset`/`sizes` if `<picture>`), mark the LCP hero image high priority, avoid heavy scroll listeners; the hero should still be intelligible if animation fails.
- **Motion:** no required animation. An extremely subtle atmospheric reveal is permissible, but no parallax or scroll vine is needed; honor reduced-motion settings.

## 5. Our Mission — Pain → Promise → Person

**Location:** Immediately after the full-bleed hero and before the Key Features grid.  
**Navigation target:** `#mission` from the hero's **Our Mission** link and footer.  
**Source authority:** *Soil-Smart Planner Team Demo.pdf* (especially pp. 2, 8–15), the Plantly investor-perspective discussion (market tiers, Pain vs. Gain, 3 P's), and the v3.0 visual system.  
**Surface mode:** Persuade, not Operate.  
**Objective:** Answer in one calm, scannable passage: **Who are we building for? Why does today's growing workflow fail them? What changes with Plantly?**

### 5.1 Narrative strategy and section role

**Three P's story order:**

1. **The Pain:** Recognize spending by habit, soil results that are hard to interpret, manual crop/plot planning, and surprises from weather and pests.
2. **The Promise:** Explain Plantly's intended bridge from soil/crop/location/budget inputs to transparent, research-linked planning, estimated costs, and useful next steps; emphasize *better decisions and protection of harvest potential*, not guaranteed outcomes.
3. **The Person:** Close with direct language for home gardeners and small-to-mid-scale growers, with initial use cases centered on backyard beds, market gardens, family farms, and small multi-plot operations (the investor conversation's first commercial segment is 1–9-acre growers).

Do not reproduce the investor memo as a wall of sales copy or lead with an AI/OSINT/RAG acronym stack. The mission's job is **why**, while the subsequent Key Features section shows **what** and the Benefits accordion shows **how it helps**. No animated scroll-growing vine, no accordion, no three dark photographic feature cards repeated here.

**Recommended one-line narrative:** *From costly guesswork to a growing plan you can understand.*

### 5.2 Exact recommended visitor-facing copy

**Eyebrow:** `OUR MISSION`

**H2 — primary editorial statement:**

> Good growing decisions shouldn't be reserved for big farms.

**Intro — the pain, in familiar language:**

> Whether you're tending a backyard garden or managing several acres, understanding your soil, choosing the right inputs, and planning around unpredictable weather shouldn't require expensive software or an agronomy degree.

**Mission — the promise; keep the product-in-development voice:**

> We're building Plantly to turn complicated agricultural data into practical, research-backed growing plans—helping growers make informed decisions, avoid unnecessary spending, and care for their soil without losing sight of their harvest.

**Small bridge heading immediately before the comparison:**

> From guesswork to a growing plan.

**Visitor-facing column labels:** `THE CHALLENGE` · `THE USUAL APPROACH` · `WITH PLANTLY`

**Audience close, after the comparison:**

> Built for the people who grow our food—and their own.

**Audience card/column A — HOME GARDENERS:**

> From a raised bed to a backyard garden, understand what your soil needs and make the most of your growing budget.

**Audience card/column B — SMALL & MID-SIZED GROWERS:**

> For market gardens and family farms managing multiple plots, make rotation, input, and timing choices with a clearer plan and more visible trade-offs.

**Quiet text link:** `Explore Plantly's tools` → `#features`, with a small inline arrow icon. This is a navigation link, **not** a second primary green trial CTA competing with the hero.

**Copy tone:** Specific, warm, competent. Avoid inflated claims such as "revolutionizing agriculture," "guaranteed higher yields," "eliminate pesticides," "save 20% today," or "live sensors". Speak as a builder offering planning support, not as a certified agronomist.

### 5.3 The central value bridge — three comparison rows

The investor's comparison becomes a **three-row editorial table without a heavy `<table>` look**. Each row preserves the causal sequence **Customer Pain → Legacy Solution → Plantly's Approach**. Rows are stacked vertically with subtle separators; the rightmost column gets the clearest visual emphasis, but not a filled green card.

| Row | The challenge (Pain) | The usual approach (Legacy) | With Plantly (Promise) |
|---|---|---|---|
| **01 · Input costs** | Fertilizers and pesticides can be expensive, and it's difficult to judge what is necessary. | Repeat last season's purchases or rely on generic shelf labels and sales advice. | Compare possible inputs against soil needs, existing compost/cover crops, plot size, and budget, with estimated costs when pricing data is available. |
| **02 · Soil complexity** | Soil pH, N-P-K, and crop history are hard to turn into clear actions. | Leave lab reports unread or interpret them manually across notes and spreadsheets. | Turn entered soil and growing history into understandable, source-linked nutrient and rotation recommendations, with assumptions visible. |
| **03 · Weather and pests** | Rainfall changes, planting windows, and recurring pests disrupt a season. | React after weather shifts or pest damage, often without a coordinated plan. | Bring available local weather context and research-supported rotation/prevention considerations into one seasonal plan. |

**Rendering guidelines:**

- Put the row index (`01`, `02`, `03`) in a narrow leading gutter; each row uses a bold short pain title (e.g. **Input costs**) and three distinct content groupings. Column headings appear once above rows on desktop.
- Give **With Plantly** a thin left emerald rule (`--color-brand`) or small green arrow glyph, never a saturated large fill. Default text remains charcoal; supporting text uses `--color-text-muted`.
- Use `1px solid var(--color-border)` separators and around `28–36px` vertical row padding. Avoid multiple nested cards, oversized shadows, green gradients, and fake dashboards.
- The visual should be scannable even if users read only the first clause in each column. Don't use paragraphs exceeding approximately 3–4 lines per column at 1440px.
- **Accessibility:** Prefer semantic `<ol>` with grouped text or a genuinely semantic `<table>` if the implementation keeps fixed column relationships. On mobile, reflow each row into three labeled text blocks instead of allowing horizontal table scrolling. Column labels must be visible or available to assistive technology in every layout.
- All examples express intended product capabilities; do not portray live price matching, validated weather alerts, or sensor readings as presently active without real integrations.

### 5.4 Visual layout — mission statement, bridge, audience

**Recommended composition at ≥1100px:**

1. **Editorial intro (top):** small uppercase `OUR MISSION` eyebrow in emerald; below it a **7/12-width oversized H2** on the left and a **5/12-width intro + mission copy** on the right. Keep the statement dominant and the supporting paragraph within ~60–65 characters per line.
2. **Comparison (middle):** a full-width horizontal hairline, a small `From guesswork to a growing plan` subheading, then three spacious horizontal rows divided by fine neutral rules. Unlike Key Features, this is typography-led, with almost no imagery.
3. **Audience close (bottom):** a single restrained soft-surface band or two unboxed columns separated by a vertical rule: `HOME GARDENERS` and `SMALL & MID-SIZED GROWERS`, each with one sentence. Close with the understated link to `#features`.

```text
 HERO / FULL-BLEED AGRICULTURAL IMAGE
─────────────────────────────────────────────────────────────────────────
                         WHITE / NEAR-WHITE MISSION

  OUR MISSION

  Good growing decisions             Whether you're tending a backyard...
  shouldn't be reserved              We're building Plantly to turn...
  for big farms.

  ───────────────────────────────────────────────────────────────────────
  From guesswork to a growing plan.

        THE CHALLENGE             THE USUAL APPROACH        WITH PLANTLY
  01    Input costs              Buying by habit          Compare options
  ───────────────────────────────────────────────────────────────────────
  02    Soil complexity          Unused reports           Clear sourced plan
  ───────────────────────────────────────────────────────────────────────
  03    Weather & pests          Reactive choices         Earlier planning
  ───────────────────────────────────────────────────────────────────────

  Built for the people who grow our food—and their own.
  HOME GARDENERS                 |   SMALL & MID-SIZED GROWERS
  ...                            |   ...

                                   Explore Plantly's tools  ↗

                         KEY FEATURES / GREEN IMAGE CARDS
```

**Material palette:** `--color-surface` (#FFF) is the principal canvas; an optional `--color-surface-soft` (#F9F9F9) band distinguishes the audience close. Main headings use `--color-ink` (#111813). Mission eyebrow and micro indicators use `--color-brand` (#1B3625); bright lime is allowed only as a **tiny** interactive/accent marker. Do not use Harvest gold as a new section button color; it belongs to approved hero/logo art.

**Typography and spacing:** H2 around `clamp(36px, 4.6vw, 64px)` with tight tracking, max 2–3 deliberate lines on desktop. Intro `18–20px` line-height ~1.5; mission text `16–18px`; comparison titles `20–24px`; comparison bodies `15–16px` with 1.5–1.65 line height. Use established max width `1360px`, page gutters `48–64px`, and `104–144px` section padding on desktop. No oversized centered CTA or testimonial block.

**Boundary with adjacent sections:** Let the cinematic hero end naturally. The mission enters with a calm white reset and a generous top margin, then flows into the white Key Features section with deliberate whitespace or one subtle separator; avoid a heavy dark transition that would compete with the dark feature cards and charcoal footer.

### 5.5 Responsive and interaction specification

- **Desktop ≥1100px:** 7/5 intro grid; comparison columns use roughly `24% / 32% / 44%` of the *content area*, subject to a compact index gutter; audience uses 2 equal columns.
- **Tablet 768–1099px:** intro becomes 6/6 or stacked, depending on legibility. Comparison can remain three columns with smaller type only while every row stays readable; otherwise labels stack within rows.
- **Mobile <768px:** eyebrow → H2 → intro/mission paragraph → comparison rows. Every comparison row stacks `THE CHALLENGE`, `THE USUAL APPROACH`, `WITH PLANTLY` vertically, visibly labeled. Audience groups stack in a single column. Preserve whitespace, never shrink descriptions below 14–15px, and never require side scrolling.
- **Motion:** optional one-time `opacity + translateY(8–12px)` entrance for the intro; use `300–450ms`, nonblocking. Comparison rows may appear together; never stagger content so far that visitors wait for reading. Respect `prefers-reduced-motion`.
- **No custom interaction is needed**: only the `Explore Plantly's tools` anchor is actionable. Do **not** create another accordion or carousel in Mission; the Benefits and Features sections already provide those patterns.
- **Link state:** visible keyboard focus, hover underline or arrow translate `2–4px`, correct `#features` target. Use native anchor behavior; avoid unnecessary JavaScript scroll hijacking.

### 5.6 Product proof, wording guardrails, and handoff

- The PDF's stated pilot measures are **hypotheses**: lower synthetic-input spending, fewer pesticide applications, yields staying close to baseline. The section may express these as goals, **not proven results**.
- The PDF explicitly says planning support is **not certified professional agronomic advice**; organic options are **not automatically cheaper**; fewer chemical inputs **can affect yields**. The mission's language must preserve these trade-offs.
- Research-backed recommendation rules and citations come from the original design; AI/RAG, weather API and price collection are **intended architecture** from the investor discussion, not proof of completed integrations.
- Initial target users are home gardeners and growers operating small plots and ~1–9-acre specialty/family farms in the investor discussion. "Mid-sized" is an audience aspiration, not evidence of existing enterprise-ready support.
- Do not repeat the hero's `$36B / $9.6B / 20%` market/target figures within the mission; those values already have a dedicated visual placement and are not customer testimonials.
- **Implementation outline:** `MissionSection` containing `MissionIntro`, `PainToValueBridge` (three static rows), `MissionAudience` and a `MissionExploreLink`. Keep the content data-driven only if doing so simplifies repeating rows; no client state is required.

**Mission acceptance criteria**

- [ ] Navigation `Our Mission` points to the real `id="mission"` section.
- [ ] Eyebrow, headline, supporting copy, three Pain → Legacy → Plantly rows, two audience messages, and `#features` link all appear.
- [ ] Copy mentions both home gardeners and small-to-mid-sized growers without implying a validated enterprise product.
- [ ] No guaranteed yield/savings, verified 20% reduction, false live data, invented testimonials, or unsafe agronomic prescriptions.
- [ ] Design respects v3.0 palette, typography, spacing, restrained motion, and a typography-first white section between hero and Key Features.
- [ ] Responsive at `320×700`, `390×844`, `768×1024`, `1440×900`, `1920×1080`, with no clipped comparisons and accessible section/link semantics.

---

## 6. Key Features section — “Smart Tools for Modern Farming Operations”

**Anchor:** `<section id="features">`  
**Reference:** `IMG_4362.webp`  
**Objective:** Demonstrate the three systems behind a useful growing plan, using tactile green visual storytelling plus restrained, believable UI-preview overlays.

### 6.1 Section heading

- White background, substantial top/bottom whitespace, no beige or purple gradient.
- Narrow centered eyebrow above title: `KEY FEATURES`, uppercase, small, emerald/bright-green detail.
- Large centered title across two lines:

  **Smart Tools for Modern**  
  **Farming Operations**

- Optionally use a tasteful italic emphasis on *Operations*; keep one visual hierarchy, with no second unrelated decorative font.

### 6.2 Three-card feature grid

Desktop: **three equal columns** (`repeat(3, minmax(0, 1fr))`), ~`24–30px` gap, ~`420–470px` card height. Each card uses a darkened agricultural photographic/textural background with a high-contrast overlay, crisp edge, subtle glass widget, and a short title/description above the widget. **Do not use gradient-only generic SaaS cards.**

| Card | Title | Description (proposed landing copy) | Embedded preview widget |
|---|---|---|---|
| 01 | **Field Intelligence** | Understand your soil, crop history, and plot-specific growing conditions. | Mini plot diagram or crop-health panel; soil pH, organic matter, last crop, confidence/missing-data indicator |
| 02 | **Monitoring & Observations** | Keep track of important changes and build a clearer record of each growing season. | Plot status / observation timeline and data points; if future sensor connections are shown, label them **concept** or **coming later** |
| 03 | **Weather Tracking** | Use local forecasts and relevant growing risks to plan work around changing conditions. | Mini forecast: temperature, precipitation, date, source, and last-updated timestamp |

The visual reference titles the middle card **Monitoring Sensor**. Use that name **only** if Plantly actually supports sensor data or the card is visibly labeled as a future concept. Until then, the source-supported feature is observations/soil records, not a claimed live hardware feed. Likewise, do not display a fake `LIVE` status for mockups.

### 6.3 Card anatomy

```text
┌─────────────────────────────────┐
│  Feature title                  │
│  Short two-line explanation     │
│                                 │
│ [dark green leaf / field photo] │
│                                 │
│  ┌───────────────────────────┐  │
│  │ translucent data widget   │  │
│  │ title / metric / plot      │  │
│  │ small labels + status     │  │
│  └───────────────────────────┘  │
└─────────────────────────────────┘
```

- Card base: deep emerald/charcoal photo tint and gradient scrim. White text on upper dark area.
- UI-widget panel: translucent dark-green/neutral overlay with `1px` light border, subtle highlights; restrained `backdrop-filter: blur(8px)` if supported, with a solid-color fallback.
- Use **realistic, clearly labeled sample data** if production data is unavailable. UI previews must not imply that a sensor is connected or forecast data is up to date unless it really is.
- Keep the widget's information design consistent across cards: label sizes, lines, spacing, status treatment, icons, and unit formatting.
- Hover: subtle contrast increase and at most `translateY(-3px)`; keyboard focus must be equally visible. Avoid 3D tilt, aggressive glow, or text movement that harms readability.
- Click: either anchors to a real feature detail / relevant product preview or does nothing interactive and should be a non-clickable card. No deceptive clickable styling without an action.

### 6.4 Responsive

- `≥1100px`: three equal cards, full visible grid.
- `768–1099px`: keep three only when widget labels remain readable; otherwise use two columns with the third on a second row, or responsive carousel **only if explicitly approved**. Prefer a grid.
- `<768px`: stack cards vertically at full available width, keep visual hierarchy and text sizes, reduce height if necessary. Do not shrink tiny dashboard widgets to illegibility; simplify their content.

## 7. Benefits section — numbered interactive accordion

**Anchor:** `<section id="benefits">`  
**Reference:** `IMG_4365.webp`  
**Objective:** Explain the practical outcome of Plantly through a considered, interactive editorial layout, not a repeated three-card feature grid.

### 7.1 Eyebrow and accordion list

Top-left small eyebrow label: **Our Green Innovation Products** (green `--color-brand` or `--color-brand-bright` as appropriate for contrast), with substantial white space above the accordion.

Three accordion items, in this order:

1. **01. Boost Harvest Output** — **expanded on initial load**, arrow `↑` at far right.
2. **02. Minimize Irrigation Requirements** — collapsed, arrow `↓`.
3. **03. Improve Soil Health** — collapsed, arrow `↓`.

Headings can stay as aspirational, benefit-oriented labels from the reference, but **body copy must not guarantee higher yields, lower irrigation volume, or objectively improved soil health without evidence**. The original team deck explicitly treats lower input spending, pesticide reductions, and yield stability as hypotheses for future grower testing.

### 7.2 Accordion interaction and row styling

- Large row-height heading with three zones: compact number (`01.`), large charcoal title, slim green directional arrow on right.
- White background; subtle `1px` neutral-gray dividers separating items.
- Accordion is **single-open**; item 01 is open by default. Clicking another header closes the prior item and expands the new one. Allow collapsing the active one as an optional accessible behavior (no forced animation loop).
- Whole row's title/button is click/keyboard accessible; arrow is a visual indicator, not a tiny isolated hit target.
- Use native `<button aria-expanded="true|false" aria-controls="...">`, stable IDs, real heading hierarchy, and appropriate focus treatment.
- Preserve scroll position reasonably as panels change; do not jump the visitor unexpectedly.

### 7.3 Expanded panel: asymmetrical two-column layout

Desktop expanded content beneath the row header:

| Left ~30% | Right ~70% |
|---|---|
| Short, useful description, top-aligned; optional one-line next-action link | Horizontal row of **three nature/photo cards** with soft corners; 1 UI-overlay card + 2 image-overlay cards; visible bottom progress/scroll indicator |

**Initial item copy suggestion** (measured, not guaranteed):

> Use your plot's soil results, previous crops, and seasonal goals to identify sensible nutrient and rotation decisions. Plantly helps you make these choices with clearer research context and budget trade-offs.

**Initial active-item carousel cards:**

1. **Optimized Growing Conditions** — close-up green foliage/photo backdrop; upper floating UI preview showing `Crop Health`, `Sensor Read`/`Soil Snapshot`, relevant sample soil or weather values. If sensors are not implemented, label it **Soil Snapshot** rather than falsely indicating live sensor readings. Bottom title and short two-line explanation on readable dark scrim.
2. **Reduced Resource Waste** — green leaves/water droplets photo, full-bleed; bottom-aligned title overlay. Supporting text optional, short.
3. **Smarter Harvest Timing** — close-up textured leaves/field imagery; bottom-aligned title overlay. Do not claim predictive harvest accuracy without an actual validated model.

For items 02 and 03, the same **layout component** is reused with content appropriate to irrigation planning and soil improvement (e.g. weather timing, water-use context, compost/cover crops, nutrient balance). **Do not repeat the exact same photos or dummy metrics in every accordion panel.**

### 7.4 Carousel mechanics

- Right panel intentionally feels horizontally browseable: at typical desktop widths display about **2.2–2.7 cards** while the remainder peeks into view, or display all three only if dimensions are genuinely generous.
- Cards around `260–300px` wide and `340–400px` tall desktop; gaps `14–18px`; rounded corners `18–20px`. Keep photographic crop meaningful.
- Use native horizontal overflow, `scroll-snap-type: x mandatory`, with keyboard-friendly previous/next controls if necessary; avoid custom draggable-only interaction.
- Progress indicator: thin horizontal track under card row, with a short darker thumb or filled portion reflecting **actual scroll position**. Do not fake movement by time or autoplay.
- Keep card text bottom-aligned with translucent dark-green gradient for readability. Avoid overlays that completely hide the photograph.
- On accordion switch, reset the new panel carousel to the beginning; preserve or reset previously seen offsets consistently.

### 7.5 Responsive

- `≥1100px`: 30/70 description + carousel. Align body to the right of the description with generous top spacing.
- `768–1099px`: approximately 35/65, or stack if panel/card readability is compromised.
- `<768px`: expanded content becomes **description above carousel**. One full card plus 10–20% of the next card should be visible as a browsing cue. Use touch scrolling with snap; keep arrows/scrollbar accessible and not dependent on hover.
- Accordion header typography scales down appropriately; number and arrow never wrap onto separate unintended lines.

## 8. Relationship between hero, mission, features, benefits, and footer

The five surfaces deliberately have **different roles**:

- **Hero = emotional identity:** full-bleed farming landscape, large foreground tractor, huge centered Plantly word, promise and action.
- **Our Mission = reasons to believe:** typography-led 3 P's story, three pain/legacy/value rows and a clear welcome to home gardeners and smaller growers.
- **Key Features = capabilities:** centered statement and three consistent, dark-green tool cards with inset believable UI.
- **Benefits = practical explanation:** airy white reading surface, large editorial accordion rows, asymmetric paragraphs and crop-photography carousel.
- **Footer = grounded closure:** decisive charcoal contrast, concise brand statement, easy navigation, newsletter input only if functional, and clear legal links.

The transition is a **simple light-canvas shift** from the image-led hero into the editorial Mission, followed by Key Features and Benefits, then a deliberate charcoal cutoff into the Footer; do not reintroduce the old scroll-growing vine. A decorative field-edge fade may be used if it does not compete with content, but there is no mandated visual scroll animation.

## 9. Footer — NEW AGRA-inspired design pattern

**Reference:** `IMG_4369.jpeg`  
**Role:** A strong, confident conclusion to the marketing page and a practical hub for navigation, brand context, legal information and (only if available) email updates.

### 9.1 Macro composition

- **Full-width near-black/charcoal section** with a slight warm-green cast (`--color-footer: #1B1D1B`). Do not use pure black, large gradient decorations, glass cards, or the illustrated tractor as a footer backdrop.
- White/soft gray copy. Content lives in an interior max-width container (`~1200–1360px`) with generous top/bottom padding (`~72–96px` desktop). The area is intentionally spacious, especially in the left half.
- Match the reference's asymmetric two-part design: **left brand-and-newsletter rail (~45–50%)** and **right social-and-links rail (~50–55%)**, followed by a subtle full-width divider and bottom legal row.

```text
┌───────────────────────────────────────────────────────────────────────────┐
│                                                                           │
│  [Plantly logo] PLANTLY               Follow Plantly                       │
│  Research-backed growing plans        [Instagram] [LinkedIn] [etc.]*       │
│  for healthier, smarter seasons.                                         │
│                                       Company    Platform    Resources    │
│                                       Our Mission Key Features Sample Plan│
│                                       Benefits    Plan Now     Research   │
│                                       Contact*    Pricing     Help*       │
│                                                                           │
│  Get growing insights by email                                            │
│  [ Enter email address...  ][ Subscribe → ]                                │
│                                                                           │
│  ─────────────────────────────────────────────────────────────────────── │
│  © {current year} Plantly               Terms of Service   Privacy Policy │
└───────────────────────────────────────────────────────────────────────────┘
```

`*` Only render social/contact/help links that actually exist. The link labels here are information-architecture proposals, not permission to ship dead routes or pretend accounts exist.

### 9.2 Left rail — identity, positioning, newsletter

- **Top:** approved Plantly emblem paired with the word `Plantly` (unlike the hero navigation, the footer **may** use a wordmark). Use a white or light monochrome SVG variant on dark; preserve mark's characteristic geometry. The existing full-color logo may be used only if contrast remains crisp.
- **Brand one-liner** (proposed, editable): `Research-backed growing plans to make smarter decisions from soil to harvest.` Keep it short and specific, not generic “transform the future” claims.
- **Lower-left subscription area:** small label `Get growing insights by email`; an inline charcoal rounded email field plus a light `Subscribe` pill, exactly the restrained visual pattern in the reference.
- Email must have a real `type="email"` input, visible label (screen-reader accessible), validation, submission feedback, and honest consent/anti-spam treatment. **If there is no newsletter backend, omit the form or present a clearly marked coming-soon state—never a fake working Subscribe button.** Avoid prechecked marketing opt-in.

### 9.3 Right rail — social and three navigation columns

- **Top row:** tiny label such as `Follow Plantly`, with muted/light social icons directly under it. Use only verified official profiles; avoid reproducing reference's icons by default when no Plantly accounts exist. Each icon-only link gets an accessible name and visible focus treatment.
- **Below:** three compact, vertically aligned link columns, with headings `Company`, `Platform`, `Resources`, in brighter white and links in lower-contrast neutral gray. Recommended grouping:

| Column | Proposed links | Behavior |
|---|---|---|
| **Company** | Our Mission (`#mission`) · Benefits · Contact | Link to actual section or route; hide Contact if no route/channel |
| **Platform** | Key Features · Start Planning · Pricing | Feature anchor, working onboarding flow, real pricing page |
| **Resources** | View Sample Plan · Research & Sources · Help Center | Show only destinations that actually exist; may be added over time |

- Use understated text links (around `14–16px`), comfortable `12–18px` vertical separation, subtly brighten/underline on hover; never use pills around every link.
- Reference includes many sample company solutions and API resources. **Do not copy them as Plantly features.** In particular, don't link to invented `Farm Automation`, `Yield Prediction`, `API Documentation`, or sensor tools not offered.

### 9.4 Lower legal bar

- Quiet horizontal rule spanning the **content container**, `1px` with low-opacity gray (`rgba(255,255,255,.12)`), after the main grid.
- Left: `© [current year] Plantly. All rights reserved.` Generate current year from the runtime/date mechanism, not hardcoded screenshot copyright.
- Right: `Terms of Service` and `Privacy Policy` (and `Cookie Preferences` only if actually applicable). Real routes required before public launch.
- The legal row is comfortably separated from main content; labels use subdued footer text color, hover/focus states stay visible.

### 9.5 Responsive layout and interaction

- **≥1100px:** two main columns; right rail has 3 equally spaced internal columns. Newsletter sits near the lower-left rather than directly beneath the brand tagline, creating the reference's deliberate negative space.
- **768–1099px:** reduce left/right split or stack brand/newsletter above links if labels compress; social area remains visible. No horizontally overflowing link columns.
- **<768px:** stacked sections: brand/tagline → newsletter (if real) → social → link groups in 1–2 columns → legal row. Form input/button may stack, each ≥44px tall. Ensure icon hit areas are at least 44×44px.
- Footer should be static and calm; simple hover/focus/validation feedback only. No heavy entrance animation.
- Text contrast must remain WCAG AA for all actionable and body content; muted secondary copy must not be so faint that it disappears on charcoal.

## 10. Responsive page behavior at a glance

| Viewport | Hero (AGRA layout) | Mission | Features | Benefits | Footer |
|---|---|---|---|---|---|
| Desktop `≥1280px` | Full-bleed landscape; 3-zone transparent nav; centered upper typography and CTA; large tractor low in frame; compact corner stats | 7/5 intro; three-row comparison; two audience groups | 3 cards side by side | 30/70 expanded panel; horizontal 2+ card window | 45/55 brand/newsletter + social/3 link columns, then legal row |
| Tablet `768–1279px` | Reduced typography/copy stack; preserve tractor and sky separation; shrink or reflow metric overlays | 6/6 or stacked intro; readable comparison | 2 or 3 cards by legibility | Narrower split or stacked panel | 2 columns if space allows, else staged stack |
| Mobile `<768px` | Tall image crop and compact menu; centered copy and CTA; metrics move under image if needed | Stacked labeled comparison rows and audience blocks | 1-column stacked cards | Text above touch carousel | Stacked brand, newsletter, social, link groups, legal |

Mandatory design-review sizes: `320×700`, `390×844`, `768×1024`, `1440×900`, `1920×1080`. In all cases, no text overlaps controls, no photo-based white text loses contrast, and no carousel content becomes unreachable by keyboard.

## 11. Data provenance, copy guardrails, and accessibility

1. **Metrics are not results.** `$36B` TAM and `$9.6B` SAM are historical market proxies; `20%` is an unverified target. Label accordingly.
2. **Sensor data is not established in the provided team deck.** Do not show `Sensor Status: LIVE` as a fact unless a real connection exists. For a marketing concept, visibly distinguish future integrations or sample UI.
3. **Specific agronomy data is contextual.** Units, soil pH, nutrient results, weather values, and risk flags in artwork are sample/demo labels unless grounded in actual data. No mock values presented as this user's real soil or location.
4. **No guarantee of yield or savings.** Avoid statements such as “increases crop yield by X%” or “reduces irrigation by X%” until backed by evidence. Product is planning support, not certified agronomic advice.
5. **Readable and keyboard usable.** WCAG AA-style contrast, visible keyboard focus, `alt` treatment for meaningful photos, decorative CSS image excluded from redundant narration, semantic heading order, real accordion buttons, and visible navigation in responsive layout.
6. **Performance.** Optimize background and photography to WebP/AVIF, size them appropriately, reserve dimensions, lazy-load below-fold photos, and avoid costly `backdrop-filter` across full cards. Prefer a small blurred inset widget with solid fallback.
7. **Motion and input.** Respect reduced-motion preferences; no autoplay carousels, no pointer-only controls, no fake loading states.
8. **Footer functionality.** Social links, newsletter subscription, help routes, and legal pages must work before being presented as active. Do not imply subscriptions succeed without actual persistence and feedback.

## 12. Implementation inventory

**Assets to prepare:**

```text
public/assets/
  plantly-mark.svg                 # To be vectorized from approved PNG; not supplied as SVG yet
  hero-tractor-field.webp          # Optimized from golden_harvest_tractor_at_sunset.png; recrop/recompose for AGRA layout if needed
  plantly-mark-light.svg           # Optional approved white/light logo variant for dark footer
  feature-field.webp               # License-approved agricultural photo / visual treatment
  feature-monitoring.webp
  feature-weather.webp
  benefit-growth.webp
  benefit-resource.webp
  benefit-harvest.webp
  ...additional unique images for accordion items 02 and 03
```

**Suggested React composition (illustrative, not mandated):**

```text
LandingPage
├── Hero
│   ├── FullBleedHeroArtwork
│   ├── HeroNav / CenteredBrandMark
│   ├── CenteredHeroCopy / TrialPillCTA
│   └── CornerMarketMetrics
├── MissionSection (#mission)
│   ├── MissionIntro
│   ├── PainToValueBridge (3 editorial rows)
│   ├── MissionAudience (home / small-mid growers)
│   └── MissionExploreLink (#features)
├── FeaturesSection (#features)
│   └── FeatureCard × 3
│       └── FeaturePreviewWidget
└── BenefitsSection (#benefits)
    └── BenefitAccordion
        └── BenefitPanel (active only)
            ├── BenefitDescription
            └── BenefitCarousel
                └── BenefitCard × 3
└── Footer
    ├── FooterIdentityAndNewsletter (form only when implemented)
    ├── SocialLinks (only official active profiles)
    ├── FooterLinkGroups (Company / Platform / Resources)
    └── FooterLegal
```

Mission adds no client state. Suggested UI state remains minimal: one accordion active-item ID (or `null`) and one carousel scroll position per active panel. No global state management necessary for the landing page. Do not use a full charting library to display the small illustrative widget visuals; use simple semantic HTML/CSS or SVG as appropriate.

## 13. Acceptance criteria

- [ ] Updated emerald/charcoal/white UI palette is used consistently; approved Harvest-gold logo/field artwork remains unchanged.
- [ ] Approved centered-only navbar logo, navigation link order, Plantly copy and white-tractor identity are preserved.
- [ ] Hero now follows `IMG_4368.jpeg`: full-bleed atmospheric agricultural image, no outer rounded-card frame, centered upper copy + pill CTA, large low tractor, bottom-corner support elements.
- [ ] Header and title remain readable over the image; responsive crop preserves tractor and worked/unworked field distinction.
- [ ] No scroll-based growth bar or vine is introduced.
- [ ] Hero displays a large white tractor, worked/unworked field, light 7-day CTA pill, and three appropriately qualified market/target stats without covering the vehicle.
- [ ] Mission sits between hero and Features, with `id="mission"`, large editorial statement, three explicit pain/legacy/Plantly comparisons, and home-gardener / smaller-farm audience messages.
- [ ] Mission copy treats savings/yields as objectives, not demonstrated results, and does not duplicate Features cards, Benefits accordion, or the hero stats.
- [ ] Key Features is centered on white and uses three dark-tinted cards: Field Intelligence, Monitoring/Observations, Weather Tracking.
- [ ] Each feature card includes a legible, subtle translucent data-preview panel; no fabricated live claims.
- [ ] Benefits is a numbered three-item accordion with **item 01 open initially** and 02/03 collapsed.
- [ ] Expanded benefits panel uses **~30% explanation / ~70% 3-card photo carousel**, plus a working scrollbar/progress indicator.
- [ ] Carousel supports mouse, touch, keyboard and reduced-motion preferences without autoplay.
- [ ] Footer follows `IMG_4369.jpeg`: near-black two-rail layout, Plantly brand + tagline and optional functioning newsletter left, socials and three link columns right, legal divider/row below.
- [ ] No fake social destinations, dead legal links, or fake newsletter-submit success.
- [ ] Layout is polished and readable at mobile, tablet, and desktop widths.
- [ ] Claims, labels and numbers do not imply verified returns, sensor feeds, or professional agronomic certification where none has been established.

---

**One-line creative direction:** A full-bleed, atmospheric Plantly farm hero with oversized centered lettering and a dominant low tractor flows into a calm editorial mission (Pain → Promise → Person), crisp emerald-accented features, an interactive benefits accordion, and a quiet charcoal footer—always grounded in believable product evidence.
