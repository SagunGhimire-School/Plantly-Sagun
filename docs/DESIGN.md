# Plantly — Master Design System & UI Direction

> **Status:** Project-wide design instruction / reusable handoff  
> **Version:** 1.0 · November 7, 2026  
> **Use:** Paste into future design/implementation conversations, or place at the root of the project.  
> **Authority:** Extracted from `Plantly_Landing_Design_v4(1).md` (v4.0). Sections marked **[Extension]** are deliberate defaults proposed for product surfaces that the landing spec does **not** define; they are not previously approved designs.  
> **Relationship to landing spec:** This document governs shared design language. The original v4 landing specification remains authoritative for the **exact landing-page composition, copy, references, and interactions**. A future approved page-specific specification governs its page layout, provided it does not silently override the shared system.

---

## 0. Design mandate — read this before designing anything

**Plantly is a calm, research-minded, nature-rooted growing planner—not a generic AI SaaS dashboard.** It helps home gardeners and small growers translate soil, crop history, location, season goals, and budget into understandable, research-linked growing plans and cost trade-offs.

**Visual intention:** Premium agricultural editorialism meets precise, low-friction software. The brand feels grounded, trustworthy, spacious, natural, and competent. The interface should make complicated decisions feel understandable without pretending they are simple, certain, or guaranteed.

**Hierarchy of decisions**
1. **Truth and usability first:** accurate data, visible assumptions/sources, readability, keyboard/touch usability, and honest capability status.
2. **Shared invariants:** palette, type family, spacing rhythm, geometry, restrained interaction, and product voice in this file.
3. **Surface-specific composition:** different pages can use different layouts while retaining the same visual grammar.
4. **Local invention:** introduce a new pattern only to solve a real problem; reuse existing tokens/components before inventing one.

**Three surface modes**
- **PERSUADE — marketing:** large editorial typography, significant whitespace, cinematic agricultural imagery where meaningful, a clear story and one dominant CTA. Landing and pricing primarily use this mode.
- **OPERATE — product:** restrained white/near-white UI, tighter information density, clear forms, visible context and status, purposeful charts/tables, minimal decorative imagery. Onboarding and dashboard primarily use this mode. **[Extension]**
- **EXPLAIN — assistant/research:** legible conversational text, clear source/assumption links, structured answers and next actions; visually quiet and trustworthy, never a flashy AI-themed interface. Chat primarily uses this mode. **[Extension]**

**Core rule:** Keep the *same identity*, not the same layout. Do not paste the landing hero, glass/photo cards, or giant marketing typography onto operational screens.

---

## 1. Color — authoritative source tokens

Use these exact values. The UI identity is **deep emerald + charcoal + white**, with brighter greens reserved for small accents. Do not introduce another competing brand accent.

| Token | Hex | Apply to |
|---|---|---|
| `--color-brand` | `#1B3625` | Primary buttons, key links/active indicators, select heading accents, subtle strong borders |
| `--color-brand-hover` | `#244B33` | Primary-button hover, active/hover dark-green treatments |
| `--color-brand-bright` | `#4E9F3D` | Small selected details, accordion arrows, tiny icons, progress emphasis—not small green text on white |
| `--color-leaf-lime` | `#76B947` | Very sparse micro-accents, especially on dark surfaces—not a large background |
| `--color-ink` | `#111813` | Primary text, headings, key figures |
| `--color-ink-soft` | `#1E241F` | Deep neutral cards, dark overlays |
| `--color-footer` | `#1B1D1B` | Charcoal footer or an intentionally dark bounded section—not the default app shell |
| `--color-footer-muted` | `#B7BDB8` | Secondary text and links on charcoal |
| `--color-surface` | `#FFFFFF` | Primary pages, cards, panels and form surfaces |
| `--color-surface-soft` | `#F9F9F9` | Subtle section alternation, app background, grouped/inset panels |
| `--color-text-muted` | `#68726B` | Descriptions, labels of secondary importance, metadata |
| `--color-border` | `#E5EAE6` | Fine dividers, field outlines, card boundaries |
| `--color-on-dark` | `#FFFFFF` | Text on deep brand/charcoal surfaces |
| `--color-harvest-art` | `#D9AF5F` | Existing approved gold leaf/artwork **only**; not CTA/UI accent |
| `--color-mist-art` | `#DFE8D8` | Existing approved art or pale illustration areas |

**Usage distribution (directional, not a measured formula):** white/soft-white dominates operating screens; charcoal communicates information; dark emerald identifies actions/selected areas; bright green appears as a restrained detail. Reserve dark full-width surfaces for intentional brand moments, not every second component.

**Contrast:** white on `--color-brand` is very readable; bright green/lime is **not** a suitable color for ordinary small body text on white. Keep actionable text and content at WCAG AA contrast; never rely on color alone for meaning.

**[Extension] Non-brand feedback colors:** Use accessible, utilitarian states when needed—e.g. error text `#B42318`, warning text `#B45309` on white, with a textual label/icon. These are *functional* colors, not replacement brand colors. Verify pairwise contrast before selecting tinted backgrounds. Do not use brand green to indicate every success, error, and neutral state.

### Ready-to-use CSS seed

```css
:root {
  /* Approved v4 source colors */
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

  /* Approved v4 geometry */
  --radius-card: 20px;
  --radius-panel: 14px;
  --radius-control: 10px;
  --page-max-width: 1360px;

  /* [Extension] Shared implementation conveniences */
  --space-1: 8px;
  --space-2: 12px;
  --space-3: 16px;
  --space-4: 24px;
  --space-5: 32px;
  --space-6: 48px;
  --color-error: #b42318;
  --color-warning: #b45309;
  --motion-fast: 180ms;
  --motion-standard: 240ms;
  --motion-reveal: 400ms;
}
```

---

## 2. Typography — one consistent voice

**Source-authorized direction:** One modern, distinctive sans-serif across marketing and product. `Geist` or `Outfit` are candidates, **not a finalized brand-font choice**. Choose one after checking the actual approved UI and licensing; do not randomly mix fonts across pages. Use system sans fallback. Italic emphasis may appear in a major editorial headline, but only within the chosen family.

| Role | Size and weight | Line height / intent |
|---|---|---|
| **Landing hero `Plantly`** | `clamp(80px, 10vw, 160px)`, very bold | Exceptional marketing-only identity moment; live text, not baked into image |
| **Marketing major H2** | `clamp(36px, 4vw, 56px)`, 500–600 | Tight, confident, 1.08–1.2 line height |
| **Mission H2 exception** | `clamp(36px, 4.6vw, 64px)` | Editorial 2–3 lines, spacious surrounding layout |
| **Large accordion heading** | `clamp(28px, 3vw, 42px)`, medium/bold | Wide, accessible hit area |
| **Feature/card title** | `20–24px`, 600 | Clear and economical |
| **Body/description** | `15–17px`, 400 | Generally 1.5–1.65 line height |
| **Caption/mini UI** | `12–14px` | Metadata only; functional labels should generally stay ≥14px |
| **[Extension] Product page H1** | `clamp(30px, 3.1vw, 48px)`, 600 | More restrained than marketing; 1.12–1.2 |
| **[Extension] Product H2/section** | `24–32px`, 600 | Distinct section anchor |
| **[Extension] UI field/row label** | `14–16px`, 500–600 | Never depend on placeholder text alone |

**Rules:** Use `--color-ink` for principal text, muted text only for supportive information. Tight negative letter-spacing on **large** display headings is acceptable (roughly `-0.02em` to `-0.04em` as a starting point); don't crush ordinary text. Left-align reading-heavy operational content; center short marketing hero statements and specifically centered editorial features. Keep long reading text approximately `60–70ch` wide; avoid full-width paragraphs on desktop. Use tabular numerals for money, measurements, and charts. **[Extension]**

---

## 3. Layout, spacing, and geometry

**Source-established rules**
- Central max content width: **1360px**, horizontally centered.
- Horizontal gutters: desktop **48–64px**; tablet **32px**; mobile **20–24px**.
- Between major marketing sections: desktop **104–144px**; mobile **64–88px**.
- Standard spacing scale: **8 / 12 / 16 / 24 / 32 / 48px**. Prefer these over arbitrary one-off values.
- Photo/image cards: **18–22px** radius (canonical token: `20px`). Inset glass/data panels: **12–16px** (canonical `14px`). Controls: **8–12px** (canonical `10px`).
- Separation usually comes from **spacing, 1px borders, and tonal contrast**, not big shadows. Glass/blur is for small photographic preview overlays only, not a default application material.
- Avoid heavy gradients, stacked nested cards, decorative green backgrounds, and overwhelming ornamentation.

**[Extension] Operating layout defaults**
- App content uses the same `1360px` maximum but **denser vertical rhythm** than marketing: `24–48px` between functional sections, `16–24px` card/grid gaps, `20–32px` desktop panel padding and `16–20px` mobile padding.
- Use a **12-column responsive grid** when it helps dashboard alignment; do not force a grid on prose or simple forms.
- A guided input flow should usually have **one primary reading/form column** around `640–760px` max; optional help/context can sit beside it on wide screens, then move below on mobile. Avoid extremely long edge-to-edge fields.
- Use a consistent vertical stack: page label/breadcrumb (if useful) → heading → one concise explanation → primary interaction/content → secondary help. Keep headings aligned to the same left content edge.
- Empty space is deliberate. Don't fill it with generic illustrations, extra metrics, or cards purely for symmetry.

---

## 4. Components — reusable baseline **[Extension unless explicitly noted]**

| Pattern | Appearance | Behavior / meaning |
|---|---|---|
| **Primary button** | `--color-brand` fill, white text, `10px` radius, target height `44–48px` | One dominant action per section; hover `--color-brand-hover`; clear pending/disabled/focus states |
| **Secondary button** | White/soft surface, ink text, fine `--color-border` outline | Back, cancel, preview, compare; visually subordinate to primary |
| **Quiet/tertiary link** | Ink or brand text + underline/arrow where appropriate | Navigation, learn more, source details; not a second loud CTA |
| **Hero CTA exception (source)** | Light/white **pill** with restrained emerald arrow detail | On image-backed landing hero only; do not apply to every app action |
| **Text field/select** | White fill; neutral 1px border; `10px` radius; `48px` default height; label above; help/error beneath | Focus border/ring must be clearly visible; not color-only; never let placeholder serve as label |
| **Data input with unit** | Label, optional suffix/prefix (`acres`, `sq ft`, `%`, `pH`, etc.), helper text | Keep unit visible and consistent; show expected format/limits; preserve typed data on validation error |
| **Standard card** | White surface, quiet border, `14–20px` radius, little/no shadow | Group related facts, not a decoration container for every sentence |
| **Highlighted card** | Selective dark emerald surface, white copy | For one important summary/decision; not repeated in every row |
| **Chip/status** | Small, precise, low-contrast-neutral or context-appropriate border/fill | Say `Draft`, `Sample`, `Estimated`, `Needs review`, `Updated …`; avoid fabricated `LIVE` or `Verified` |
| **Accordion** | Source pattern: full-row button, fine separators, spacious typography | Single-open on landing Benefits; 150–250ms controls, 220–320ms content; keyboard/ARIA support |
| **Table/list** | Mostly white, fine horizontal dividers, subtle header | Prefer scanability and units; stack as labeled rows on narrow screens, no clipped columns |
| **Icons** | Simple, consistent stroke style and sizing | Functional cues; never replace labels when clarity matters |

**Interaction checklist:** Every active control has `default`, `hover`, `focus-visible`, `pressed/selected` where relevant, `disabled`, `loading`, and success/error feedback where relevant. Minimum touch targets approximately `44×44px`; tab order and visible keyboard focus are mandatory. No fake clickable cards or dead links.

**Form-specific guidance:** Group fields by the grower's mental model rather than the database schema. Explain why each datum matters. Support missing soil-test values honestly (`Not sure` / `I don't have a soil test`) when the planner can handle that; do not invent values. Indicate required versus optional fields. Prefer inline validation with actionable language and preservation of user input. Do not overwhelm with simultaneous unrelated fields.

---

## 5. Motion and microinteraction — quiet, purposeful

**Source values**
- Standard hover/button changes: **150–250ms**.
- Accordion expansion/collapse: **220–320ms**.
- Optional one-time reveal below the fold: **300–500ms** using small opacity + `translateY(8–12px)`; content must be readable without animation.
- Interactive photo-card hover: at most **`translateY(-3px)`**, no 3D tilt or glow.
- **No scroll-grown plant, progress vine, flashy parallax, or autoplay carousel.** Benefits image carousel is user-driven and can reflect real scroll position.
- Honor `prefers-reduced-motion: reduce` by removing nonessential movement and making transitions immediate or minimal.

**[Extension] Operating motion:** Prefer state transitions to theatrical entrances. Inline validation, expand-details, step changes, saving feedback and chat message appearance should be predictable and nonblocking. Avoid animated counters or fake streaming/progress that implies a system is doing work it isn't doing. Loading skeletons/spinners only when genuinely waiting for data; no fabricated completion.

---

## 6. Brand imagery and materiality

**Authorized brand assets and reference roles**
- For location go to `frontend\public\assets\images`
- Approved emblem reference: `planty_logo.svg` (gold right leaf + green spherical plant form).
- Approved white-tractor agricultural hero subject: `golden_harvest_tractor_at_sunset.png`, requiring responsive cropping/optimization if used.
- `IMG_4368.jpeg` (AGRA): **composition reference** for full-bleed immersive hero, not a replacement Plantly asset.
- `IMG_4362.webp`: photographic dark-green Key Features cards with small translucent data widgets.
- `IMG_4365.webp`: editorial Benefits accordion + nature-photo carousel.
- `IMG_4369.jpeg` (AGRA): restrained charcoal multi-rail footer reference.

**Guardrails:** Nature photography is real visual storytelling, not mandatory decoration. Use photographic texture and localized contrast scrims in marketing; avoid photography under dense dashboard tables, forms, or chat messages. No generic giant green gradients, random neon blobs, multiple frosted-glass panels, stock-looking AI brains, glowing orbs, or unapproved new logos. Preserve the brand emblem and gold artwork instead of recoloring them to match flat UI tokens.

---

## 7. Navigation and page family alignment

- **Landing (source authority):** transparent overlay navigation on the full-bleed hero; true **`1fr auto 1fr`** three-track grid; links left (`Our Mission`, `Key Features`, `Benefits`), **emblem-only** perfectly centered, actions right (`Start Planning`, `Pricing`, `Sign Up`). Mobile uses accessible collapsed navigation. Full exact implementation stays in landing v4.
- **[Extension] Marketing subpages (pricing, educational pages):** reuse brand/header vocabulary and restrained CTA hierarchy, but use a legible solid/neutral header when a full-bleed image is absent. Do not force image-overlay white navigation onto white pages.
- **[Extension] Auth/onboarding:** prioritize a clear step location, short task title, Save/Continue/Back actions, and a visible route home. Avoid marketing-navigation clutter during a focused form.
- **[Extension] Signed-in product:** use a consistent app shell that leaves content space for plots, plans, weather and budget; accessible navigation labels. A sidebar on wide screens or compact mobile navigation is acceptable, but do not clone the landing's centered-logo hero navbar into the dashboard.
- **Footer (source authority for marketing):** full-width `#1B1D1B` charcoal; brand and *functioning* newsletter left, social and grouped link columns right, quiet legal bar. Do not apply the full marketing footer to every operational screen by default.

---

## 8. Page templates to reuse in upcoming design conversations **[Extension]**

### A. Pricing page — PERSUADE, but decision-first

**Order:** slim navigation → short left- or center-aligned pricing headline → concise description / billing clarification → 2–3 plan cards **only if real tiers exist** → transparent comparison or included-features list → honest FAQ/terms → single primary CTA → marketing footer.

**Visual:** principally white or `#F9F9F9`; dark-ink headline; emerald primary action; neutral-bordered `14–20px` price cards with `24–32px` inner padding and `24px` gaps. One recommended plan may have a **thin emerald border or small label**, not a glowing/lime-filled box. Prices use tabular numerals and clear units (`/month`, `/year`, renewal details). Use whitespace to communicate confidence.

**Truth rules:** The landing's **7-day trial is proposed copy, not a verified active offer**. The deck's **$9.99/year** is an illustrative market assumption, **not an approved retail price**. Never fabricate tiers, active trials, discounts, payment terms, testimonials, or product entitlements. A pricing design can use explicitly labeled placeholders until business rules are confirmed.

### B. Plot / soil input flow — OPERATE

**Order:** compact context header → progress stated in real steps (if multi-step) → one focused group at a time → field-level explanation → persistent navigation (`Back`, `Continue`, optional `Save draft`) → review before generation.

**Suggested grouping (based on product evidence, not yet a finalized information architecture):** plot identity, area and location → current/previous crops and season goals → soil tests (pH, N/P/K, organic matter) → inputs/compost/cover crops and budget → irrigation, observed pests, historical yield and planting dates → review. Avoid forcing users to complete fields that the actual engine does not require.

**Visual:** single main form column `640–760px` where possible; optional contextual advice rail on desktop; one-column on mobile. Short labels above fields, 8px label gap, 12px helper/error gap, 16–24px between fields, 32px between groups. Units explicit; don't assume whether soil nutrient entries are ppm, lb/acre or lab-defined without asking. Use `Sample` tags for demonstrations. Provide honest empty/missing/invalid states.

### C. Dashboard / seasonal plan — OPERATE

**Order:** page/plot selector and season context → headline and current plan status → 2–4 **relevant** summary metrics → primary plan/recommendations → supporting soil, weather, estimated input costs and history → sources / assumptions / next actions.

**Visual:** soft-white app canvas with white bordered modules, 12-column grid on desktop when useful, 16–24px gaps, sparse emerald emphasis. A prominent dark-green summary card can be used **once**, if justified by hierarchy. Data density beats spectacle; charts are reserved for meaningful comparisons, not decoration. At mobile sizes, stack priority information and let detailed sections expand or navigate.

**Trust:** Clearly mark `Estimated`, `User-entered`, `Sample`, `Needs soil test`, `Forecast updated [time]`, or `Source` as appropriate. Show units and baseline; do not invent soil-health percentages, yield improvements, savings achieved, live weather, or sensor status. Expose *why* a recommendation exists and allow source inspection.

### D. Research / “Talk to your data” chatbot — EXPLAIN

**Order:** compact chat context (`Plot`, `Season`, available data) → readable conversation → prompt suggestions tied to real plan questions → composer with clear send state → cite/source/assumption details adjacent to each substantive answer.

**Visual:** predominantly white/soft-white, ink text, thin separators; use a modest emerald tint or border to identify assistant-associated actions, **not** full saturated message balloons everywhere. Assistant output should use structured text, short sections and reference links when supported; user messages can be visually distinguished without mimicking unrelated consumer messengers. Composer uses `10–14px` radius and obvious focus/send affordance. Avoid competing left rails, floating AI orbs, or perpetual typing animations.

**Trust:** Make clear whether a response is generated from user-provided plot data, available research, a retrieved source, or a general explanation. When a soil value, current price, real-time forecast, or source is not available, say so. Never show invented citations or claim an AI answer is certified agronomic advice. Provide a visible path to the underlying plan/data.

---

## 9. Responsive behavior

**Review at exactly these source-established sizes:** `320×700`, `390×844`, `768×1024`, `1440×900`, `1920×1080`.

- **Mobile `<768px`:** 20–24px gutters; one-column forms/cards; maintain ≥14–15px readable content; put essential actions within practical reach; no sideways body overflow. Photo/benefit carousels can show one card + a peek at the next and must remain keyboard accessible.
- **Tablet `768–1099px`:** 32px gutters; switch grids to two columns or stack when readability suffers, not just because a fixed breakpoint says so.
- **Desktop `≥1100px`:** preserve aligned column edges, 48–64px gutters, comfortable whitespace, and meaningful maximum reading widths. Three-column features are appropriate for marketing; app grids depend on information priority.
- **Hero-specific `≥1280px` and mobile:** keep white tractor prominent low in landscape, copy high in sky, bottom metrics unobtrusive; `min-height:100dvh`, not rigid `height:100vh`; art-direct mobile crops. This rule applies **only to the landing hero**.

Every viewport must maintain readable labels/units, uncut data/actions, clear contrast, touch/keyboard access, sensible heading order, and no elements occluding each other.

---

## 10. Product voice, evidence, and UX ethics

- Speak to **home gardeners and small growers**, not giant enterprise farms by default. Be warm, clear, practical, non-patronizing and specific.
- Present Plantly as **planning and decision support**, not certified professional agronomic advice. Local soil tests and extension services remain important.
- Do not guarantee higher yield, less irrigation, cost savings, fewer chemicals or healthier soil. Pilot outcomes are **hypotheses**, not verified impact.
- Never equate **organic** with automatically cheaper or better; make yield/cost/soil trade-offs visible.
- The historical `$36B` TAM and `$9.6B` SAM are **market proxies**, not Plantly revenues or verified current software-market sizing. The `20%` input-cost reduction is an **unverified target**. Don't put them on dashboard KPI cards as actual outcomes.
- Do not present proposed AI/RAG, price scraping, weather, monitoring, sensors, chat retrieval, newsletter, or free trial as **currently working** unless implementation is confirmed.
- Distinguish actual data from demo data. Expose source, scope, assumptions and timestamps where relevant. A beautiful but misleading dashboard violates the brand.

---

## 11. Acceptance tests for any new Plantly screen

1. **Recognizable:** same emerald/charcoal/white identity, single sans-serif, deliberate radii and spacing.
2. **Appropriate mode:** marketing persuades; product screens help users act; assistant helps users understand. No indiscriminate hero/glass treatment.
3. **Clear focal point:** obvious H1, primary task, primary CTA or next step. No competing green buttons.
4. **Consistent geometry:** `1360px` max width, approved gutters, common 8/12/16/24/32/48 scale; cards/controls reuse geometry.
5. **Quiet material:** white/soft-white, hairlines, little shadow, bright green only in small accents.
6. **Honest UX:** realistic statuses, provenance, no fabricated results/integrations/trial terms.
7. **Accessible:** tested contrast, 44px targets, visible focus, semantic labels, keyboard use and reduced-motion support.
8. **Responsive:** review 320, 390, 768, 1440 and 1920 widths; no clipping, unreadable miniature cards, or side scrolling.
9. **Useful motion:** short feedback; no autoplay, parallax gimmicks, scroll-growing vines or blocking entrances.
10. **Page fit:** specify exceptions explicitly; do not silently change global tokens to suit a single mockup.

### Instruction for future design / coding assistants

> Treat this file as the **project-wide visual/UX contract**. Preserve its exact color values, proportions, restrained motion, geometry, brand voice and honesty rules. First classify the requested page as **PERSUADE**, **OPERATE**, or **EXPLAIN**. Apply the corresponding page template, adapting structure to the actual product task. Reuse the shared primitives before inventing new visuals. Do not silently replace approved tokens or assets, import unrelated design-system aesthetics, add fake metrics, or imply proposed integrations are live. Where a page is not fully specified, treat **[Extension]** patterns here as starting defaults and clearly flag any proposed departure. For landing-specific details, consult `Plantly_Landing_Design_v4(1).md` instead of reconstructing them from memory. Produce an interface that is calm, precise, agricultural, premium and immediately usable.

---

**Design in one sentence:** *A cinematic, nature-rooted brand on the outside; a crisp, honest, research-first decision tool on the inside—unified by forest green, charcoal, white, structured whitespace and restrained motion.*



## Design skills — execution routing, not a new design authority

Visual requirements, approved tokens, page geometry, composition, and honest-data rules in this document remain authoritative. The landing page additionally follows `docs/LANDING_DESIGN.md`.

Repository-local Codex skills are discovered from `.agents/skills/<skill-name>/SKILL.md`. A reference to a skill is **not proof of installation**. Read the actual skill `name:` field and confirm its availability before invocation.

For meaningful new frontend work, consult **Taste** (typically `design-taste-frontend`) for composition and implementation only when installed. For a completed UI slice, consult **Impeccable** for targeted layout/accessibility/responsive critique when installed. Consult **Animate** only when an interaction genuinely needs motion; prefer reduced-motion-friendly CSS before adding dependencies. These tools may suggest improvements but cannot override this design system or invent missing image assets.

Use available Playwright MCP or Playwright Test for actual browser evidence at 320×700, 390×844, 768×1024, 1440×900 and 1920×1080. Do not assume a separate Plantly visual-review skill exists. Missing artwork is a visibly labeled `AWAITING USER ASSET` placeholder until the user supplies a real asset; do not generate fake final photography.

**Ponytail** is a separately installed engineering-simplicity plugin, not a design system or a guaranteed token/currency limiter. Follow its guidance only if installed and trusted; avoid unnecessary boilerplate, repeated large context loads, and unrelated skill invocations without weakening tests, accessibility, data provenance, or scientific approval.

Exact tool selection and installation policy: `docs/agent/SKILLS.md`. Agent-specific task routing: root `AGENTS.md` and `frontend/AGENTS.md`. Do not repeat detailed skill installation instructions throughout this visual specification.

Use these integrations only when installed and discoverable.

Never override approved colors, typography, layout,
responsive rules, scientific safety, or image requirements.

If images are missing, render visibly labeled
AWAITING USER ASSET placeholders.

Read docs/agent/SKILLS.md for detailed routing.
