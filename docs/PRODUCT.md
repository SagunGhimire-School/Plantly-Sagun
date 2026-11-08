# Plantly — Product Definition & Functional Specification

<!-- impeccable:product-schema 1 -->

> **Version:** 2.0 — 2026-11-07  
> **Document owner:** Plantly product / founding team  
> **Status:** Consolidated product baseline; explicitly separate accepted behavior, conditional delivery, future scope and unresolved choices  
> **Product type:** Responsive web application for research-grounded, plot-specific seasonal growing plans and contextual AI assistance  
> **Companion documents:** `docs/ARCHITECTURE.md` (implementation authority), `docs/DESIGN.md` / `PLANTLY_MASTER_DESIGN_SYSTEM(1).md` (visual/interaction authority), `docs/CHATBOT_SPEC.md` (optional future detailed assistant behavior), `docs/SCIENTIFIC_RULE_REVIEW.md` (proposed review record)  
> **Purpose:** Define **what Plantly does, whom it serves, what users see and can do, what is deferred, and what truth/safety constraints apply**. This document deliberately does not choose frameworks, database tables, endpoints or deployment providers.  
> **Important:** A feature described as a product requirement is **not a claim that its implementation already exists**. A working teammate prototype is not a scientifically reviewed release.

## Platform

web

## Users

Home gardeners and small specialty/market/family growers first. Mid-sized growers remain a longer-term audience, not the scope of the first demo.

## Product Purpose

Turn a grower's plot information, season and crop goals, soil observations and lab results, crop history, reviewed agronomic evidence, and available weather and price context into an understandable, persistent, actionable season blueprint.

## Positioning

**Plantly is a seasonal planning product with an AI agronomy explainer—not a generic chatbot, unqualified fertilizer calculator, online retailer, sensor network, or certified agricultural consultancy.** The season plan is the core deliverable; the dashboard organizes it; chat explains and explores it.

## Operating Context

A user signs up, creates and revisits plots, associates them with a season, provides as much authentic context as they have, reviews gaps, requests a plan, and consults that saved version through the dashboard and contextual chatbot. Unavailable sources or measurements reduce the level of advice rather than invite invented precision.

## Product Principles

Action over dashboards; plot/season specificity; evidence before confidence; useful abstention; honest economics; understandable language; and user control of changes.

## Document status conventions

| Marker | Meaning |
|---|---|
| **[LOCKED]** | Explicitly agreed in Plantly decision rounds or subsequent confirmation. Governs product design and engineering unless formally changed. |
| **[CORE]** | Foundational product intent inherited from the original Soil-Smart Planner concept; must respect scientific and release gates. |
| **[MVP]** | Target behavior for the first complete hosted demonstration, subject to evidence and operational release gates. |
| **[CONDITIONAL]** | Shown or calculated only where compatible approved inputs, sources, coverage or external data are actually available. |
| **[PROPOSED]** | Reasonable product choice not explicitly approved; never silently assume locked. |
| **[LATER]** | Outside first demonstration; may appear as a future direction, not an implemented feature. |
| **[OPEN]** | Material decision or evidence not yet resolved. Do not invent its value. |

**Precedence:** (1) most recent explicit team decisions; (2) this product contract for product behavior; (3) original project material for foundational direction; (4) design system for visuals; (5) `ARCHITECTURE.md` for technical implementation. If documents conflict across responsibilities, flag for human resolution. Source content or teammate prototype code does not automatically approve a scientific rule. See §19 and §22.

---

## 1. Executive product definition

### 1.1 One-sentence promise

**Plantly helps a grower decide what to plant, what their available soil information means, what actions to consider this season, and what supported inputs might cost—while showing the evidence and limitations behind each recommendation.**

### 1.2 The user's problem

Growers may have fragmented plot records, soil reports they do not know how to interpret, repeated crop-family or pest issues, variable weather, limited budgets and products of uncertain value. Advice is often generic, while costs are difficult to compare. The grower needs one place to turn available facts into plot-specific decisions without pretending incomplete facts are complete.

### 1.3 Differentiation

| Traditional workaround | Plantly product outcome |
|---|---|
| Memory or spreadsheets of prior crops | Saved plot and growing-season history, with applicable rotation guidance |
| Dense soil-test reports or guesswork | Plain-language view of **actual supplied measurements**, method constraints, and supported interpretations |
| Generic crop/fertilizer advice | Conditional, reviewed-rule actions tied to specific crop, soil method, region and inputs |
| Searching multiple research links | Viewable reason, source and limitations for important recommendations |
| Retail shelf estimates | Comparable **observed or explicitly estimated** purchase options only when relevant quantities and prices exist |
| Asking a general chatbot to guess | Plan-aware assistant that reads the authorized saved plan and reviewed evidence |

The outcome is **better-informed decisions and potentially more efficient spending**. Plantly does **not** promise a specific savings percentage, higher yield, elimination of pesticides or disease, or perfect timing.

### 1.4 Product boundary

Plantly provides planning support. Soil laboratories, local extension advice, product labels and qualified agricultural professionals remain authoritative where appropriate. It does not control farm machinery, dose chemicals autonomously or purchase supplies without the user's action.

---

## 2. Users, goals and accessibility

### 2.1 Primary users

| User | Main job | What Plantly must optimize |
|---|---|---|
| **Home gardener [CORE]** | "Help me understand this bed and decide what to grow or buy." | Simple prompts, clear units, optional technical fields, modest plot sizes, honest unknowns |
| **Small specialty/market/family grower [CORE]** | "Plan multiple plots across seasons while understanding inputs and cost." | Plot history, season association, evidence, per-plot and season views, practical decisions |
| **Mid-sized grower [LATER aspiration]** | "Coordinate more acreage and growing constraints." | Data model should not preclude growth, but enterprise workflows are not a first-release promise |

Plantly does not initially target enterprise farm resource planning, equipment telemetry or regulated pesticide-compliance automation.

### 2.2 Jobs to be done

1. **Understand:** What does my actual soil information indicate, and what is missing?
2. **Choose:** Is my desired crop compatible with my plot's known history and the reviewed evidence?
3. **Plan:** What supported actions should I consider in this season, and in what sequence?
4. **Estimate:** Which viable inputs and quantities can be justified, and what might buying them cost?
5. **Explain:** Why was this recommendation made, and which source supports it?
6. **Explore:** What would happen if I changed my crop, plot assumptions or available resources?
7. **Return:** Can I revisit the exact plan I previously generated after leaving the site?

### 2.3 Accessibility commitments [LOCKED direction]

Core signup, onboarding, plan and chat interactions must be usable by keyboard, screen reader and touch. Explain terms such as pH, P/K test method, crop family and amendment rate without requiring the user to read a research paper. All meaningful statuses require text, not only color. Reduced-motion users receive a nonanimated processing alternative. A full workflow must function in a mobile browser; native mobile and offline-first apps are [LATER].

---

## 3. Product principles and information integrity

1. **The plan is the product.** The assistant and dashboard are interfaces to a saved, structured plan, not separate sources of competing advice.
2. **Make next actions visible.** Prioritize action, risk, missing information and relevant timing over decorative metrics.
3. **Tie claims to the right context.** Where possible, each recommendation identifies plot, season, crop, inputs, evidence and applicability.
4. **Show observations as observations.** User-entered pH is not a lab measurement; a forecast is not observed weather; a placeholder price is not a shop quote.
5. **Separate known, interpreted and unknown.** An empty field is not zero, and a missing soil value must not be replaced with a believable number.
6. **Use qualified calculations.** Quantities come from approved rules and compatible inputs, never the LLM's general memory.
7. **Prefer useful abstention to fictitious precision.** An unsupported application rate becomes a visible missing-data state.
8. **Distinguish cost from savings.** Estimated cost may be available without a valid historical baseline. Never substitute potential savings for measured savings.
9. **Ask before changing decisions.** Explanation, what-if analysis and saved-plan regeneration are distinct user actions.
10. **Be transparent about freshness.** Plans are preserved versions; weather and prices may age independently.

### 3.1 Forbidden product claims [LOCKED]

Never display fabricated soil-health scores, lab values, local humidity/temperature, planting probability, current prices, retailer links, yields, source citations, verified research status or cost savings. Do not show a hypothetical research-backed number for a real user's plot as if independently reviewed. Avoid unsupported blanket claims that organic products always cost less or are identical substitutes for synthetic products.

### 3.2 Source and result labels [MVP]

Product surfaces must use consistent labels when material:

- **Measured / lab-reported** — tied to an actual report or measurement and date; method identified where available.
- **User-reported** — entered by grower without independent laboratory verification.
- **Calculated from approved rule** — deterministic quantity or interpretation with rule/evidence references.
- **Research-supported** — claim matched to reviewed applicable evidence, not merely a similar search result.
- **Observed price / forecast / historical weather** — actual provider response with timestamp and scope.
- **Estimated** — supported calculation with explicitly named assumptions and exclusions.
- **Sample/demo** — synthetic fixtures; never a live result.
- **Unavailable / insufficient data / unsupported scope / outdated** — explicit absence or limitation.

Do not express an uncalibrated "AI confidence 93%" as agricultural certainty.

---

## 4. Confirmed MVP scope and phased delivery

The following is a **product release contract**. Features tagged `[CONDITIONAL]` are not automatically blocked from the MVP, but they must decline to provide unsupported values. The target is **one complete, real user journey**, not a visually impressive mockup.

### 4.1 First demonstrable release

| Capability | MVP behavior | Basis |
|---|---|---|
| Landing and pricing navigation | Public landing with truthful product positioning and pricing entry; no invented subscription terms | [LOCKED surfaces], offer rules [OPEN] |
| Public signup/login/logout | Account first, then persisted user workspace; demo identity is server-protected | [LOCKED] |
| Temporary-demo accounts | User is told the service is a demo with limited account recovery and retention | [LOCKED direction], duration [OPEN] |
| Guided onboarding | Step-based plot and season entry; resume from saved draft after refresh/login | [LOCKED] |
| Grower-wide season | User can associate one or more owned plots with a season | [LOCKED] |
| Plot/soil information | Create and revisit plots, crop history, soil observations and available lab results | [CORE/MVP] |
| Review and generate | User confirms input assumptions and explicitly starts generation | [LOCKED] |
| Scientific scope gate | Only approved crops/regions/methods/rules authorize evidence-dependent outputs | [LOCKED] |
| Mixed scientific plan | Limited reviewed rotation + soil interpretation, lab-backed lime quantity, and narrowly reviewed nutrient pathway | [LOCKED scope]; actual activation [CONDITIONAL] |
| Generation progress | Real phases and a growing-plant illustration; durable status across refresh | [LOCKED] |
| Saved blueprint | Versioned, per-plot, evidence-linked plan that remains accessible later | [LOCKED] |
| Dashboard | Selected plot/season, plan summary, actionable guidance, observed soil, gaps, costs and weather states | [LOCKED] |
| Contextual chatbot | Persistent chat tied to the selected saved plan version; source-backed explanation | [LOCKED] |
| What-if analysis | Compare assumptions without changing the persisted plan; no silent mutation | [MVP target], invariant [LOCKED] |
| Weather context | Fetch actual provider observations/forecast when configured; clearly labeled fallback when unavailable | [LOCKED behavior/CONDITIONAL data] |
| Product/pricing context | Surface viable inputs and available retailer/product information; price comparisons only with real compatible observations | [LOCKED behavior/CONDITIONAL data] |
| Basic responsive/a11y UX | Works on desktop and mobile, including error, partial and empty states | [LOCKED direction] |

### 4.2 Capabilities intentionally not required for the first complete release

| Capability | First-release decision |
|---|---|
| AI parsing of uploaded PDF or photo soil reports | **[LATER / OPEN promotion]**; manual entry is sufficient for core launch. Teammate prototype does not make this automatically approved. |
| SMS/email/push weather alerts and continuous monitoring | **[LATER]**; one-time contextual forecast display is enough initially. |
| Automated retailer scraping of arbitrary sites | **[LATER]** unless a lawful supported provider/feed is specifically chosen; no promise of universal seller coverage. |
| In-app checkout, fulfillment, payment processing | **[LATER / OPEN business model]**. External links may be shown when sourced. |
| Daily farming activity logs, purchase ledger, yield tracker, impact analytics | **[LATER]**; retain historical inputs and versioned plans now. |
| Team accounts, farm staff roles, enterprise analytics | **[LATER]**. One user owns the initial workspace. |
| Satellite data, IoT soil sensors, automatic field monitoring | **[LATER]**, not implied by estimated soil information. |
| Autonomous plant disease diagnosis, pesticide prescriptions | **[LATER / not currently authorized]**. Basic reviewed prevention/scouting guidance only. |
| Crop variety-level yield prediction, probabilistic planting-success scores | **[LATER/OPEN evidence]**. No score without validated model and inputs. |
| Dedicated weather, costs, research, analytics navigation pages | **Not MVP surfaces**; information is integrated into dashboard/plan and evidence details. |
| Guaranteed seven-day trial, paid tier enforcement or card checkout | **[OPEN]** until terms, entitlements and billing exist. |

### 4.3 Scientific launch blocker

Although the mixed scientific MVP is approved conceptually, **no specific crop/region/test-method/rule combination has yet been human approved for actual-user quantitative execution**. The teammate's catalog lists crop and research entries, but most are explicitly marked unverified. Publication/source verification and rule approval are release prerequisites, not optional documentation. Until completed, restrict real-user output and use clearly labeled synthetic demonstrations for any unsupported numerical story.

---

## 5. End-to-end user journey

```text
VISITOR
  → Landing / feature story / pricing information (truthful offer language)
  → Sign up or log in [public signup; login-first]
  → Guided onboarding draft: location → season → plots → soil/history → goals/inputs → review
  → Check completeness + scientific coverage
  → Explicit Generate Plan
  → Persistent job with truthful phases and growing-plant animation
  → Saved versioned plot-season blueprint
  → Dashboard: summary, next actions, measurements, rotation, costs/weather, citations
       ↳ Plot details and crop/soil history
       ↳ Full plan and "Why?" evidence
       ↳ Plan-aware chat and non-destructive what-if
       ↳ Edit inputs → outdated notice → deliberate regeneration
  → Return later to same plan/version and messages
```

### 5.1 Visitor and marketing [MVP]

Landing is responsible for explaining target user, pain, the plan-first outcome, representative capabilities and a credible primary action. Retain the approved landing design and a pricing entry. **The existing "Try Plantly free for 7 days" design text is not yet backed by operational trial rules**: do not claim an active seven-day entitlement, payment requirement or trial-to-paid billing behavior before the team defines it. The interim CTA wording is a **[PROPOSED]** design/product adjustment requiring alignment with `DESIGN.md`.

A read-only sample plan may be shown as **sample data** if it helps conversion; this remains [PROPOSED]. Do not pass off the synthetic fixture as a completed real customer plan.

### 5.2 Identity and return visits [LOCKED]

A visitor signs up/logs in before entering authenticated onboarding. Public signup is allowed for the temporary hosted demo. Core account tasks are signup, login, logout and session expiration. **Email verification and password recovery are explicitly deferred for the temporary demo**; don't design functional "Forgot password" or confirmation flows if they are not implemented. Disclose that demo data may be purged after a defined window, to be decided and published before launch. A user must not view another user's plot, plan or chat.

### 5.3 First-time onboarding [LOCKED]

Step-based setup with back/next controls and explanatory field help. Save valid partial drafts at meaningful step boundaries. Returning users resume their most recent active draft. Require an explicit review of provided facts, missing data and assumptions before generation. Allow correction without discarding previous steps. The UI never populates a new plot's soil values with plausible fabricated pH, phosphorus or potassium defaults.

### 5.4 Generation and transition [LOCKED]

The user explicitly selects **Generate plan** after reviewing current inputs. Display named processing phases only when they actually occur. A growing plant can animate as a metaphor, but percentage completion must not imply measurement where none exists. Refreshing or navigating away must not start a second generation inadvertently. On success show the persisted plan; on failure preserve draft, show reason at an appropriate level and offer safe retry.

### 5.5 Returning dashboard [LOCKED]

A user can open their most recent saved plot-season plan. The dashboard is not a new LLM call on each refresh. It displays what was stored and, where supported, a separately refreshed weather/price layer with independent timestamps. Changing relevant plot inputs marks existing plan versions outdated rather than silently replacing historical data.

### 5.6 Ongoing edits and chat [LOCKED / MVP target]

User edits crop selection, growing assumptions or measurements deliberately. A fresh plan needs explicit regeneration and creates a new version; older versions remain inspectable while within the demo retention window. Chat explains the selected saved version and can explore permitted what-if changes, but conversations do not directly change authoritative plot state.

---

## 6. Onboarding, inputs and missing-information policy

### 6.1 Guided setup stages

| Stage | User enters | Experience rule |
|---|---|---|
| 1. Growing location and season | General region/location, season name or dates | Ask only the precision required for coverage/weather; don't imply exact GPS is necessary for every rule |
| 2. Plot details | Plot name, area and selected area unit; additional plots as needed | Support meaningful small gardens; preserve canonical units internally without confusing user |
| 3. Soil observations | Available pH, P/K, organic matter, lab rate, test date, extraction method and units when known | Explicit "I don't know"; method may be required for certain interpretations |
| 4. Crop and issue history | Desired crops, previous crops, recurring pests/diseases, current planting status | Unknown history is not interpreted as no risk |
| 5. Resources and goals | Compost/materials available, irrigation limitations, budget, desired harvest, prior input use | Optional fields qualify comparisons; avoid blocking unrelated guidance |
| 6. Review | Entered facts, source labels, unsupported crop/region warnings, missing data | Distinguish what Plantly can and cannot calculate; allow edits |

The exact order and individual field grouping can be refined under `DESIGN.md` without changing required semantics. Detailed soil-report extraction from image/PDF is not required for the initial manually entered flow.

### 6.2 Input inventory and authority

| Domain | Data | Scope | Required for which capability |
|---|---|---|---|
| Growing region | Region/general location, optional location detail | Grower or plot | Required for local coverage/weather-sensitive recommendations |
| Season | Label/year, practical dates/time window | Grower-wide | Required for season-based planning |
| Plot | Name, positive area, area unit | Plot | Required for quantity scaling and per-plot plan |
| Crop goals | Planned/desired crop(s), optional varieties and harvest goals | Plot-season | Required for crop-specific planning; varieties optional |
| Crop history | Previous one or more seasons/crops; dates when known | Plot / previous seasons | Required for defensible rotation interpretation |
| Soil observations | pH, P/K, organic matter, others as available | Plot and observation date | Values shown when provided; particular interpretations require compatible method |
| Lab provenance | Lab, extraction method, report date, sampling depth, original unit | Soil test/measurement | Required whenever the chosen numeric rule depends on test methodology |
| Lab lime recommendation | Numeric application rate, basis/area/units, associated report | Soil test | Required for lab-backed lime quantity; no placeholder substitution |
| Input history | Prior fertilizer/products, quantity/unit/date, pesticide application count if known | Plot / prior season | Required for defensible baseline claims; otherwise optional |
| Available resources | Compost, manure, cover crop history, materials already owned | Grower/plot-season | Optional unless a reviewed rule requires specific properties |
| Pests/disease | Observed problem history and timing | Plot / season | Optional; enables only supported preventive interpretations |
| Water/constraints | Irrigation method, resource limitations, equipment | Plot/grower | Optional unless necessary for a given proposed action |
| Economics | Budget, currency, price paid, historical spend | Grower/plot-season | Budget comparison/savings require relevant facts; a plan need not require a budget |
| Outcomes [LATER] | Yield, actual applications, labor and expenditure | Plot/season | Required only when building impact analytics |

### 6.3 Missing-data rules [LOCKED]

- **No soil test:** show any legitimate user-reported observations and data gaps, but no lab-dependent nutrient classification or quantity.
- **Unknown extraction method:** don't apply thresholds developed for a different method simply because both results are displayed in ppm.
- **No lab lime rate:** do not compute a lime quantity from the teammate prototype's placeholder pH/texture table; invite entry of a suitable lab rate or local professional guidance.
- **Unknown crop history:** explain that rotation assessment is incomplete. Never assume the plot had no prior crops.
- **Unsupported crop or region:** permit the user to save the plot and view facts, but withhold the unsupported evidence-dependent plan/recommendation.
- **Unknown prices:** do not imply $0 cost or invent a merchant; present price as unavailable.
- **No comparable baseline:** do not display claimed savings (dollar or percentage).
- **Stale weather:** do not treat an old forecast as current; show retrieval time/validity and limitations.
- **Unresolved contradiction:** ask for clarification or narrow the plan rather than choosing whichever value yields more convenient advice.

### 6.4 General completeness gate [PROPOSED precise product rule]

The first plan-generation attempt should require a valid signed-in account, a named plot with positive area, grower season, a sufficiently specified growing region for supported coverage, and a supported crop or eligible goal. Additional inputs are conditionally required by the particular requested scientific action. If these minimum facts are missing, keep the user's draft and show a corrective checklist; do not generate a false complete plan. The exact minimum region granularity and crop catalog remain [OPEN] until evidence review.

---

## 7. Core domain concepts and product ownership

### 7.1 Grower, plot, season, plot-season [LOCKED]

A **grower account** owns independent **plots** (locations/areas where crops grow) and **seasons** (grower-wide planning periods). A plot may participate in multiple seasons, and a season may include multiple plots. Each **plot-season** has its own crop goals, constraints, actions and generated plan history. A grower-level overview may summarize several plot-seasons without losing which plot each observation or recommendation concerns.

A soil measurement belongs to a plot and retains its observation date and provenance, not automatically to the currently selected season. Crop history likewise follows the plot through seasons. A recommendation must identify which observed history actually informed it.

### 7.2 Saved plan versus current data [LOCKED]

A **plan version** is the immutable result of a successful generation attempt using a particular input snapshot and reviewed evidence. It is not a constantly evolving chat transcript. An edit to the plot does not rewrite that old version. The user can inspect the plan's creation time, material assumptions, known limits and whether it may now be outdated.

A newly generated plan replaces the *selection of the current plan* for that plot-season, not the old record. Old versions can be revisited while retained.

### 7.3 User choice and execution state [LOCKED principle; later tracking]

Separate **suggested action**, **user accepted/selected action**, and **actual completed action**. The first release may show recommendations and support regeneration without a full activity ledger. Do not label a suggestion "completed" merely because it appeared in a generated plan. Actual season logs and measured impacts are [LATER].

---

## 8. Scientific recommendation scope and review gate

### 8.1 Accepted mixed qualitative + quantitative MVP [LOCKED — ARC-047/ARC-048]

Plantly will implement a **small, scientifically reviewed mix** of crop-rotation guidance, soil interpretation, lab-backed lime quantity conversion and a *narrow* subset of fertilizer calculation scenarios. It will not enable all formulas found in the prototype. The team's research review chooses which rules actually become live.

| Recommendation class | User-visible outcome when approved + applicable | If not supported |
|---|---|---|
| Crop rotation | Flag relevant recent crop-family/problem conflict and offer an eligible alternative with reason | Show "rotation guidance unavailable/incomplete"; do not invent crop recommendation |
| Soil interpretation | Display measured pH/P/K and compatible reviewed classification/context | Show the original measurement and an explanation of method/data gaps, no invented classification |
| Lab-backed lime quantity | Scale the laboratory-reported rate to the confirmed plot area; present original rate and units | Request compatible lab rate; **no fallback placeholder rate** |
| Limited fertilizer quantity | Show only numbers derived from an individually approved nutrient rule with all required measurements and applicable crop/region/method | "Insufficient evidence/data" or "unsupported here"; no model-created quantity |
| Product requirement and cost | Convert eligible quantity into supported package/price comparison | Show known product facts or no comparable cost; don't imply shopping availability |
| Pest prevention/scouting | Reviewed, context-relevant low-risk prevention considerations and source | General data-gap language; no chemical treatment rate |
| Timing / planting suitability | Only supported guidance using documented conditions, relevant dates and evidence | Do not show probability of success or definitive planting date |

### 8.2 Rule status and governance [LOCKED]

Each rule version must have an explicit review state: `pending_review`, `approved`, or `disabled`. A human reviewer must verify the exact source or permitted authoritative excerpt, scientific applicability (crop, region, test method, soil/depth and assumptions), unit conversion, formula/interpretation, limitations and independent acceptance examples. **Only `approved` rules with all applicable prerequisites can authorize recommendations.** Importing a YAML row or running a unit test does not equal approval.

The first reviewed candidates are rotation rules, crop-specific soil targets, compatible soil-test interpretation, the user-provided lab-lime pathway, and a tiny nutrient rule subset. They remain **unapproved until reviewed**. `lime_table.yaml` from the prototype contains explicitly labeled placeholder rates and must not be used as a real-user fallback.

### 8.3 What the LLM may and may not do [LOCKED]

An LLM may help select among **already eligible** actions, summarize approved source passages, explain trade-offs and present accessible language. It must not invent a soil measurement, authorize an unreviewed formula, recalculate fertilizer needs from memory, claim unsupported crop applicability, invent scientific references or silently add a pesticide treatment.

The final blueprint and quoted quantities must be checked against approved rules and captured source references before appearing in the product. A polished explanation is not proof of correctness.

### 8.4 Geographic and agronomic scope [OPEN]

The teammate prototype has 21 catalog crops, 40 source records and 122 research notes in the inspected version. Those are **inventory counts, not approved coverage**. Published initial supported crop(s), geographic region(s), soil-test method(s) and reviewed-rule version(s) will be decided by reviewing the actual sources. Until then, any unsupported user profile can still be saved but cannot receive unsupported crop-specific prescriptive content.

### 8.5 Risk communication

When recommendations touch agricultural inputs, explain what measurement or rule allowed the quantity, why it applies, relevant application limitations and why the grower should consult their lab report, product instructions or extension provider where needed. Do not overpromise that an organic substitution is safe/effective without matching available nutrient analysis and constraints.

---

## 9. Research grounding and evidence experience

### 9.1 What users should see [CORE / LOCKED]

Each material recommendation should expose a human-readable *Why?* action, the relevant rule or reasoning category, user facts used, research publication/source link where available, and any uncertainty or missing data. The core product supports reviewed claims with traceable sources rather than treating a list of references as decoration.

A citation should identify an actual versioned source/passaged evidence, not a reference fabricated by Gemini. The review process must distinguish a source that **directly supports the recommendation under relevant conditions** from a source that merely discusses the same topic.

### 9.2 Curated research library [LOCKED direction]

The first knowledge library comes from actual team-curated sources: agricultural extension publications, relevant peer-reviewed materials, structured datasets and carefully checked notes. Papers/notes and numeric lookup tables play different roles: a retrieved passage can explain an approved action; a structured scientific rule determines whether a quantitative calculation is allowed. Both require appropriate provenance.

Source inclusion, legal permissions, publication accuracy, review status and crop/region/test-method coverage must be cataloged. A paper being inside the repository does not automatically mean it is eligible to support a live recommendation. The knowledge inventory template is a **template**, not an approved research database.

### 9.3 Evidence display states [MVP]

| Evidence state | UI behavior |
|---|---|
| Reviewed + applicable | Show the recommendation and link/reason |
| Available but not reviewed | May appear in explicitly labeled source/library metadata, **not** as authoritative support for a real-user prescription |
| Reviewed but not applicable | Withhold that rule for this crop/region/test method; explain limitation |
| No valid evidence | Omit/abstain on affected claim; tell user what is missing |
| Disagreement/uncertainty | Show a bounded warning and avoid unsupported certainty |
| Reference lookup temporarily down | Preserve previously saved plan and citations where stored; don't fabricate fresh evidence |

### 9.4 Why this matters to the dashboard

A dashboard card does not need a wall of papers. It needs a short reason and a clear path to inspect the evidence. The fuller plan detail may show source title, publisher, relevant finding or excerpt where permitted, date and applicability limits. No unsupported "research-backed" badge.

---

## 10. The generated product: persistent season blueprint

### 10.1 Required blueprint structure [LOCKED meaning]

The blueprint is structured, inspectable and saved. It should provide, as far as supported:

1. **Context summary:** grower season, plot, intended crops, goals, known location and data limitations.
2. **Rotation/crop guidance:** suggested or cautioned crop choices, conflicts, alternatives and reasoning.
3. **Soil interpretation:** observed values, method/date, supported classifications, absent/uncertain fields.
4. **Input strategy:** approved nutrient/lime quantities when eligible, usable resource comparisons and constraints.
5. **Schedule / next actions:** supported, season-relevant tasks and ordering; timing gaps if actual calendar guidance is not reviewed.
6. **Prevention/monitoring:** supported problem-history and scouting considerations.
7. **Cost view:** supported estimated purchase quantities and prices, with exclusions and availability states.
8. **Weather context:** provider-backed and time-bounded information if available.
9. **Evidence and limitations:** explanations, source links, reviewed rule references, missing or incompatible data.
10. **Version information:** generation time, input snapshot reference, staleness and relation to previous versions.

Not every section is guaranteed to contain a numeric answer for every user. A valid blueprint can contain a mixture of approved recommendations and clearly identified abstentions, provided it is never represented as an entirely complete recommendation when the core scientific scope is unsupported.

### 10.2 Meaningful recommendation detail [MVP]

| Field | Product meaning |
|---|---|
| Action | What the grower should consider |
| Plot / season / crop | Where the advice applies |
| Timing | When, or "not determined" if unsupported |
| Why | Short explanation based on relevant inputs and evidence |
| Input values used | Actual observations/historical records affecting the advice |
| Rule and evidence | Approved rule version + viewable reviewed reference |
| Quantity and units | Only where an approved numerical rule applies |
| Cost | Actual observed/estimated comparable price, with date and exclusions |
| Alternatives | Other eligible options and trade-offs, not invented substitutes |
| Limitation | Missing method, old measurement, unsupported geographic coverage, etc. |

### 10.3 Plan freshness and versions [LOCKED]

The saved scientific plan does not change because the latest weather forecast changes. New weather or pricing may display as a separate, clearly current-context layer. If the user changes crop/area/soil inputs that affected the saved generation snapshot, show **"This plan may be outdated"** and offer regeneration. Do not rewrite the previous explanation or silently change chat history to the new plan version.

### 10.4 No unqualified output [LOCKED]

If a scientific coverage gate fails for the user's primary crop/region, the product should preserve their inputs and show why an applicable plan cannot yet be produced. It may offer setup help and general, non-prescriptive education within reviewed scope, but it cannot issue disguised crop-specific instructions.

---

## 11. Dashboard — exact product content and state priorities

### 11.1 What the dashboard must answer [LOCKED]

A grower should be able to identify **(1) which plot/season they're seeing, (2) what action is next, (3) what the current plan says, (4) which soil facts and risks matter, (5) what reliable costs/weather are known, and (6) why the recommendation was made** without opening multiple unrelated pages.

Dashboard modules are **integrated product components**, not separate required weather, shopping or research destinations. The layout and colors remain governed by `DESIGN.md`.

### 11.2 Dashboard content contract

| Module/card | Display | Data conditions and exclusions | Priority |
|---|---|---|---|
| Plot & season selector | Selected plot, season label, relevant area | User-owned only; an invalid selection must not leak another user's data | High / [LOCKED] |
| Plan status | Not generated, generating, ready, partial, outdated, failed, creation time/version | Must reflect a real saved plan or job; no invented completion percentages | High / [LOCKED] |
| Next actions | A short list of evidence-backed actions with plot/crop/timing | Show reason and source; if timing is unsupported, avoid fictional date | High / [MVP] |
| Crop / rotation | Planned crop, relevant history, reviewed warning or eligible alternative | No crop-specific advice without coverage and relevant history | High / [LOCKED scope] |
| Soil observations | User/lab pH, nutrient and other supplied values; date/unit/method | **Unknown stays unknown**; no imaginary sensor measurements | High / [MVP] |
| Soil interpretation | Supported classification/limitations per compatible soil test | No generic "healthy soil 89%" badge or universally valid score | High / [CONDITIONAL] |
| Lab lime need | Approved lab rate, scaled plot quantity, reason | Only with confirmed lab rate and reviewed method; placeholder table disabled | Medium / [CONDITIONAL] |
| Fertilizer/input guidance | Approved quantities and feasible alternatives | Narrow reviewed rule set; withhold unapproved rates | Medium / [CONDITIONAL] |
| Price / shopping | Candidate items, quantities, unit/package price, seller/source, date, cost assumptions | Real listings or user-supplied price only; no invented retailer links | Medium / [CONDITIONAL] |
| Weather context | Relevant forecast/observations and action-sensitive caution | Source/time/location required; fall back to unavailable/stale | Medium / [CONDITIONAL] |
| Conditions summary | Temperature/humidity/rainfall over a **defined actual period**, if supplied by provider | No LLM-estimated climate numbers; don't conflate history and forecast | Optional / [CONDITIONAL] |
| Planting suitability | Explain whether reviewed constraints are met for a particular crop/time, if supported | No probability percentage or unsupported "perfect to plant" claims | Optional / [CONDITIONAL] |
| Budget / spend | Estimated plan purchases versus entered budget or known baseline | No implied savings without comparable baseline and full assumptions | Optional / [CONDITIONAL] |
| Evidence & limitations | Source links and "what's missing" notices | Always accessible for material guidance | High / [LOCKED] |
| Chat entry | "Ask Plantly" plus contextual prompts | Bound to selected saved plan version when present | High / [LOCKED] |

### 11.3 Dashboard before first submission [LOCKED]

An authenticated user who has no completed onboarding should see an intentional empty state with a prominent **Create your first plot / Continue setup** action. If the user has a plot but no plan, show known plot facts and an obvious **Review and generate plan** action, not fake recommendations. If a generation job is active, show its real phase and let the user return to it. If the crop/region is unsupported, show the coverage limitation and preserve the profile.

### 11.4 Dashboard after generation [LOCKED]

Show the saved blueprint organized around next actions, current plot/season, crop choice, soil facts, applicable rule-backed inputs and meaningful weather/cost context. Use compact summaries with links to full plan/recommendation details and verified citations. A plan's partial weather/pricing coverage should not make scientific recommendations appear unreviewed or vice versa; they are independent qualities.

### 11.5 Multi-plot behavior [LOCKED]

The selected plot and season determine what the dashboard displays. Switching plots changes the view to that plot's owned records and plan version. A grower-wide season overview may aggregate *comparable* totals and actions, but may not merge soils into a single invented "farm health" number. Cross-plot optimization is not guaranteed in the first reviewed scientific scope.

### 11.6 Interactions and navigation

The workspace offers integrated plot list/detail, plan detail, version history access, onboarding/editing and a contextual chat drawer. Desktop and mobile navigation patterns follow the design system. User preferences and lightweight presentation state must not alter authoritative plan data or skip permission checks.

---

## 12. Generation: feedback, success and failure

### 12.1 Truthful processing [LOCKED]

The growing-plant processing concept is an expressive progress presentation, not proof of scientific certainty. Show authentic statuses such as validating inputs, retrieving approved evidence, evaluating supported rules, gathering available weather/prices, preparing explanation, validating and saving. Only display a named operation as completed after backend confirmation. A percentage progress bar is optional only if backed by meaningful tracked progress.

### 12.2 Outcome states

| State | What the user sees | Next action |
|---|---|---|
| No draft | Empty setup state | Start plot/season setup |
| Draft incomplete | Saved field progress + missing items | Continue review |
| Validation conflict | Field-level reason | Correct inputs or reload latest draft |
| Unsupported scientific scope | Explain supported coverage gap | Save profile; choose an actually supported use case only if appropriate |
| Queued/running | Real job phase + visual feedback | Leave page safely, return to status |
| Successful plan | Saved version with supported sections | Open dashboard and full plan |
| Partial external context | Scientific plan with weather/price limitations | Continue without those fields; retry enrichment where supported |
| Core scientific failure | No misleading "completed" plan | Preserve inputs, show appropriate error/retry |
| Input changed after plan | Outdated marker on prior version | Review changes and deliberately regenerate |

A successful scientific plan may have conditional omissions; **that is not permission to fill the gaps with an LLM's guess**.

---

## 13. "Talk to Your Data" — dashboard chatbot

### 13.1 Purpose and positioning [LOCKED]

The assistant is a **contextual explainer of the user's saved plan**, with guarded exploration capabilities. It is not an unrestricted farming adviser or an autonomous planner that can quietly rewrite user decisions. On desktop it appears in a chat drawer; on small screens it can be a full-height sheet or equivalent accessible surface, as governed by the design system.

### 13.2 Context rules [LOCKED]

Chat is tied to the authenticated user, selected plot-season and **specific immutable plan version**. For a plan-specific answer it may use relevant saved measurements, crop history, plan actions, approved rule references, approved retrieved research and source-labeled provider context. It cannot trust arbitrary claimed ownership or an unrelated user profile supplied in the message. When a newer plan replaces the selected one, clearly distinguish the old conversation's version and offer a separate context for the new plan.

### 13.3 Supported user intents [MVP]

| User question | Desired answer / permitted action |
|---|---|
| "Why should I rotate this crop?" | Explain the saved rotation decision, actual history and reviewed source; acknowledge unknown history |
| "What does this pH/P/K mean?" | Explain the observed measurement and any compatible approved interpretation; don't invent an absent classification |
| "Why do I need lime?" | Quote the approved lab-backed recommendation if present, including rate/units; otherwise explain what's missing |
| "Can I use compost instead?" | Discuss eligible trade-offs only; quantitative substitution needs approved nutrient analysis and rules |
| "What will these inputs cost?" | Use existing supported plan quantities and actual price provenance; distinguish price age and exclusions |
| "What if I planted a different crop?" | Offer a **non-persistent comparison** using eligible reviewed rules and snapshot assumptions; disclose unsupported scenarios |
| "Will rain affect the next task?" | Refer to actual available forecast validity and selected action; no invented forecast or certainty |
| "What should I do if I have no soil test?" | Explain available limited help and which test/method would unlock additional supported interpretation |
| "Show your sources" | Link exact applicable approved evidence or state that evidence is missing |

### 13.4 Assistant response quality [LOCKED principles; detailed tone still PROPOSED]

Answers should begin with the direct answer, then tie it to the selected plot/plan, provide the short "why", cite reviewed material for significant agricultural claims, state conditions/limitations, and suggest a practical next step when useful. Prefer everyday language, short paragraphs and explicit units. Never use a citation purely because a retrieved passage shares keywords.

A future `CHATBOT_SPEC.md` may refine voice, follow-up prompts, model-tool schemas, evaluation datasets and refusal wording; the **behavioral boundaries here are already binding**.

### 13.5 What-if versus real changes [LOCKED invariant]

A what-if comparison works on a temporary copy of relevant assumptions. The assistant may show differences in crop choice, supported nutrients and **comparable** estimated cost where calculation is legitimate. It must not write edited crop/soil values to the user's saved plot or mutate the saved plan. Actual changes require a visible user-confirmed edit and new plan generation/version.

### 13.6 Conversation retention and error states [LOCKED direction]

Messages persist within the temporary-demo account lifecycle and stay associated with their plan version. Chat access requires a valid session and ownership; data retention after the demo is [OPEN duration]. If Gemini or research retrieval is unavailable, preserve the rest of the dashboard and display an honest chat retry/error state. Avoid model-generated raw HTML; links and explanations should be safe to render.

### 13.7 Chat limitations [LOCKED]

The assistant cannot fabricate nutrient rates, chemical/pesticide application instructions, real-time conditions, prices, measurement history or source citations. It must distinguish reviewed scientific outcomes from general educational explanation. A nonreviewed source may not be represented as authoritative merely because the assistant found it. Answer outside validated scope with the limitation, not a confident plan.

---

## 14. Weather, conditions and seasonal risk

### 14.1 Intended capability [LOCKED behavior, CONDITIONAL live data]

Plantly enriches the plan and dashboard with relevant weather **only from an identified, functioning provider or previously retained dated observation**. The user should understand the difference between the current weather, near-term forecasts and historical averages. Forecast is probabilistic and time-limited; it is not a guarantee of suitable planting conditions.

### 14.2 Valid weather dashboard signals

- Temperature, humidity, rainfall/precipitation and relevant conditions **only if genuinely supplied** for a described location and period.
- Averages such as "average temperature this week" only when computed from a defined observed or forecast interval, clearly labeled.
- Plan-relevant caution such as possible heavy rain near a scheduled input/planting action only where both event information and advice are supported.
- Weather source, retrieval time, forecast valid-through and stale/unavailable state.

There is no approved product requirement to generate a fabricated "average humidity" from the LLM or a precise planting-success probability. A suitability summary/modal requires independently approved inputs and agronomic interpretation and is [CONDITIONAL / not a required score card].

### 14.3 Beyond MVP [LATER]

Scheduled reevaluation, severe-weather monitoring, email/SMS/push notifications, user-configurable alerts, autonomous rescheduling and irrigation control. These need additional policies and are not implied by one-time forecast context.

---

## 15. Inputs, products, shopping links and truthful economics

### 15.1 User problem [CORE]

Growers need to know which scientifically viable inputs are required, how much might be needed, what they already have and how options compare economically. Plantly should be practical but must **not** turn merchant data into evidence of agronomic need.

### 15.2 Comparison workflow [LOCKED direction, CONDITIONAL output]

1. Start with an **approved** agronomic input need and supported quantity/units, or visibly state that a quantity is unavailable.
2. Account for verified user-owned stock or usable amendments only where the selected scientific rule permits the credit/substitution.
3. Match compatible products using actual composition/package information and applicable restrictions.
4. Use a supported provider feed/API or other lawful permitted source to obtain **real price observations**; retain retailer and observation time. Manual user price is [PROPOSED] as an additional fallback.
5. Normalize package units and quantity estimates, record currency and explicitly identify excluded shipping, tax, transport and labor costs where material.
6. Show source links when provided; let users investigate an actual seller. No automatic checkout in MVP.
7. Rank or compare only truly comparable options. Do not claim best local price without sufficient supplier coverage.

### 15.3 Cost versus savings [LOCKED]

| Label | Requirements |
|---|---|
| **Estimated input cost** | Supported quantity × appropriately normalized price or explicitly qualified user observation; list assumptions/exclusions |
| **Budget comparison** | User-entered budget and supported estimate in a comparable currency/period |
| **Potential savings** | Credible comparable baseline, scenario and assumptions; not merely difference between two unrelated shopping prices |
| **Actual savings** | Observed expenses and a defensible comparison methodology; not a first-demo impact claim |
| **No estimate available** | Display insufficient product/price/quantity data; **never display $0 as if nothing is needed** |

A price from a dated national agricultural survey is **not** automatically a local live retailer listing. The teammate prototype includes placeholder prices; these must not appear as live quotes.

### 15.4 Shopping experience [MVP conditional]

A dashboard/plan may contain a shopping or input card showing candidate material, eligible quantity, package size, available seller, timestamp and estimated subtotal or a clear unavailable status. Links must actually point to identified product or seller pages. Plantly is not itself a seller. Outbound checkout is external and entirely user-driven.

---

## 16. Historical season behavior, feedback and long-term measurement

### 16.1 Historical continuity [LOCKED baseline]

Maintain plot identity across seasons and preserve generated plan versions and their original assumptions. This supports future crop-rotation history and user trust. The demo does not require a complete task-completion ledger to use past crop data.

### 16.2 Activity logs and analytics [LATER]

Potential future product areas: planting events, fertilizer applications, pest scouting, product purchases, labor costs, harvest quantities, actual yield/area, organic-matter changes and plan-adoption metrics. These provide the basis for measuring outcomes; the existence of the source project's pilot goals is not evidence that benefits are already achieved.

### 16.3 Grower feedback [PROPOSED]

Allow users to flag incorrect data, challenge a recommendation or rate explanation, and note usefulness. Feedback must not automatically mark previously unreviewed source content as scientifically approved. Product improvements require deliberate review and tested changes.

---

## 17. Marketing, pricing and commercial truth

### 17.1 Product promise and brand [LOCKED direction]

Use the Plantly brand and the approved landing design language. Keep the voice calm, grounded, optimistic and practical. Marketing can illustrate desired outcomes, but must never present a demo fixture, placeholder rate, unverified citation or hypothetical savings as established field evidence.

### 17.2 Pricing and trial [OPEN]

The design includes Pricing navigation and a "Try Plantly free for 7 days" CTA. **This does not authorize actual seven-day entitlements, payment collection or subscription enforcement.** Billing plans, price points, trial start trigger, card requirement, limits, renewal, cancellation, taxes and disclosures are not yet approved. Until these exist, the product must not imply a functioning paywall or automatic charges. Updating approved marketing CTA copy needs product/design coordination.

The original project's illustrative $9.99/year price and total-addressable-market estimates remain **pitch assumptions**, not approved retail prices or market validation. Likewise proposed 15–20% savings targets are hypotheses, not measured Plantly results.

### 17.3 Public hosted demo [LOCKED]

The near-term public launch is a functional **temporary demonstration**, not full commercial availability. Public signup is permitted, but email verification and password recovery are deferred. Users must be told the demo nature and limitations before providing data. The team must decide and publish an actual cleanup/erasure window before enabling unrestricted signup. No real payment requirement is part of the approved initial demo.

---

## 18. Data privacy, control, accessibility and failure experiences

### 18.1 Product-level privacy promises [LOCKED]

Users see only their own plots, plans, chat and drafts. Minimize personal data and location precision to what the feature needs. Account and growing records belong to an identifiable authenticated user; protection and ownership are not merely frontend visibility rules. Temporary demo storage is disclosed, and the product must have a real cleanup/deletion policy before the public demo. Exact duration and retention exceptions remain [OPEN].

### 18.2 Failure-state table

| Event | User-visible product behavior |
|---|---|
| New user without plots | Friendly create-plot setup; no fake dashboard |
| Saved incomplete draft | Continue where left off; show outstanding fields |
| Unknown pH, P, K | Display "not provided"; do not insert sample defaults |
| Incompatible soil-test method | Show measured value without unsupported interpretation or rate |
| Unreviewed soil/fertilizer rule | Suppress prescriptive amount; explain needed evidence |
| Unsupported crop/region | Preserve plot data; provide explicit coverage limitation |
| No appropriate research passage | Omit/qualify affected recommendation, no fabricated citation |
| Missing real price | Product/cost marked unavailable; no fake merchant or $0 replacement |
| Weather unavailable/stale | State condition and time; preserve otherwise supported scientific plan |
| Slow generation | Truthful persisted phase; safe refresh/return |
| Failed generation | Preserve inputs and older plans; clear retry message |
| Changed input after plan | Show outdated marker and explicit regenerate action |
| New plan version | Distinguish its conversation from earlier plan context |
| AI chat error | Keep plan usable; retry chat without losing saved records |
| Session expiration | Clearly request login; no private-data leakage; saved work remains while account exists |
| Mobile/reduced motion | Equivalent content and statuses without animation dependence |

### 18.3 Usability and accessibility acceptance [MVP]

Users can complete the core flow on mobile without inaccessible wide-only tables; forms have meaningful labels and validation; status is never color-only; source links are keyboard reachable; chat is operable by keyboard and touch; animation can be reduced; the absence of a value is stated in text.

---

## 19. Release acceptance criteria and product success

### 19.1 Minimum honest end-to-end demo

The first complete demonstrated flow must support:

- [ ] A visitor can create a temporary account, sign in and return to their saved workspace.
- [ ] A grower can create a plot, choose a season and retain a draft across navigation/refresh.
- [ ] The app preserves authentic input provenance, supports unknown measurements and does not invent defaults.
- [ ] The team has approved **at least one clearly documented crop/region/method scenario and applicable rule set**, or the release clearly limits itself to source-reviewed non-prescriptive content until that exists.
- [ ] A plan can be requested and its actual job status recovered across refresh.
- [ ] A finished plan is saved, shown on the dashboard and remains the same version on reload.
- [ ] Crop rotation and soil interpretation appear only under reviewed applicability conditions.
- [ ] Lab-backed lime and the selected limited fertilizer quantity appear **only if** reviewed prerequisites are satisfied; unsupported quantities abstain.
- [ ] Every material scientific recommendation carries a meaningful reason/evidence trail and an honest limitation state.
- [ ] The dashboard displays actual soil measurements, action state and availability/freshness for weather and prices.
- [ ] The user can open a context-bound saved chatbot conversation, ask "why", and receive grounded responses or an explicit inability to support the claim.
- [ ] A hypothetical what-if action does not mutate current plan or user inputs.
- [ ] Editing relevant inputs marks prior plan outdated; regeneration creates another inspectable version.
- [ ] Another user cannot read the account's plots, plans or messages.
- [ ] Public-demo retention disclosure and actual deletion/cleanup process are approved and present.
- [ ] The team has tested genuine provider error states; sample data is labeled as such.

A UI mockup, successful unit test of unreviewed formula, or scripted Gemini answer **does not** satisfy an end-to-end functional acceptance criterion.

### 19.2 Product outcome measures (not asserted results)

| Outcome | Measure when evidence exists |
|---|---|
| First-use clarity | Setup completion and correction rate |
| First useful plan | Valid plans produced for in-scope user data |
| Scientific coverage | Reviewed rule/source coverage and abstention rate |
| Explainability | Percentage of material claims linked to applicable reviewed evidence |
| Trust | User-reported clarity, false-precision incidents, unsupported-answer rate |
| Returning value | Plan revisit and useful chat/question activity |
| Cost usefulness | Percentage of recommendations with sufficiently comparable price observations |
| Actual impact [LATER] | User-recorded expense, input rate, yield and other outcomes with defensible comparison |

Do not assign launch success percentages, achieved savings or conversion benchmarks absent actual pilot data or explicit approval.

---

## 20. Delivery sequence — product-facing milestones

The release sequence below describes product behavior, not mandated programming tickets. Actual module breakdown belongs in `ARCHITECTURE.md`.

| Stage | User-visible deliverable | Evidence of completion |
|---|---|---|
| **0. Truth and coverage** | Clear supported-scope and research approval matrix; honest marketing language | Reviewed scenario and explicit exclusions |
| **1. Account + onboarding** | Signup/login, persisted draft, owned plots and season | Return after logout/login without losing saved draft |
| **2. Scientific core** | Limited reviewed rotation/soil interpretation and lab-backed/narrow nutrient paths | Correct supported outputs and abstentions in independent test cases |
| **3. Generate + save** | Persistent generation progress and saved versioned blueprint | Refresh and revisit real plan unchanged |
| **4. Dashboard + chat** | Actions, measurement/limitation cards, citations and plan-aware chat | Relevant grounded answer and safe non-mutating comparison |
| **5. Live context** | Weather and eligible product/price information with source freshness | Real provider responses where configured; resilient unavailable states |
| **6. Demo hardening** | Privacy controls, public demo warning, clean failure UX and accessibility | End-to-end acceptance and chosen data lifecycle |

If the integration team cannot verify a provider or scientific rule by demo time, **reduce the claimed feature coverage**, not the truthfulness standard.

---

## 21. Open product decisions and explicit boundaries

The following are intentionally unresolved. No coding agent may supply values by guessing.

| ID | Open decision | Effect on product | Blocker level |
|---|---|---|---|
| PD-01 | Seven-day offer, pricing tiers and payment terms | Landing/pricing truth, entitlements and paywall | Blocks commercial trial claims, not authenticated demo |
| PD-02 | **Initial supported crop, region and soil-test method combinations** | Which real-user plans can be produced | Blocks scientific launch coverage |
| PD-03 | Exact reviewed source/rule approval list and named reviewer | Which qualitative/quantitative recommendations execute | Blocks affected scientific outputs |
| PD-04 | Minimum required data for each numeric fertilizer path | Eligibility and abstention wording | Blocks corresponding rate |
| PD-05 | Public-demo cleanup window and deletion/disclosure terms | Privacy and user expectations | Blocks public unqualified signup |
| PD-06 | Which weather provider, supported geographic area and freshness interval | Live weather cards and affected-task cautions | Blocks live weather claims |
| PD-07 | Which seller/product data sources, regions and listing freshness | Product/price cards and links | Blocks live price claims |
| PD-08 | Free/trial plot, plan-generation and chat usage limits | Entitlements and abuse constraints | Blocks published commercial limits |
| PD-09 | Exact supported chatbot conversational style, tools and evaluation criteria | Conversational consistency | Doesn't change core safety rules; detailed spec recommended |
| PD-10 | Whether AI-assisted report extraction joins first release | Onboarding effort/complexity | Not a core launch dependency |
| PD-11 | Whether user-entered manual price overrides ship | Cost comparison coverage | Not a core launch dependency |
| PD-12 | Whether there is a read-only sample plan on landing | Discovery and conversion | Not a core launch dependency |
| PD-13 | Evaluation/pilot methodology for cost/yield/input reduction claims | Future outcome measurement | Blocks quantified impact claims |
| PD-14 | Details of planting suitability indicators/condition summaries | Dashboard-specific weather/suitability messaging | Blocks unsupported probability/score |

### 21.1 Previously open questions now explicitly resolved

| Previous v1 question | v2 resolution |
|---|---|
| Signup before onboarding or guest draft? | **Login-first [LOCKED]**; user drafts persist after sign-in |
| Are plans/chat saved and for which context? | **Saved versioned plans and plan-version-bound conversations [LOCKED]** |
| Is the grower limited to one plot? | **Grower-wide seasons with plot-season associations [LOCKED]**; UX supports plot selection |
| Can AI create fertilizer rates using research snippets alone? | **No [LOCKED]**; approved rule and method gate required |
| What is the MVP scientific ambition? | **Mixed, narrow reviewed rotation + soil + lab lime + selected fertilizer [LOCKED]** |
| Do we show weather/pricing only if live? | **Use actual provider data where possible with truthful fallback [LOCKED]** |
| Can a chatbot suggestion change the saved plan? | **No silent mutation [LOCKED]**; hypothetical comparison only without confirmation |
| Is email recovery required at hackathon? | **Deferred for temporary public demo [LOCKED]**, with limitations disclosed |
| Are full activity/yield logs MVP? | **No [LATER]**; persistent plot/season/history and plan versions are MVP |
| Does the prototype's existing crop table establish supported crops? | **No [LOCKED gate]**; entries remain candidates until human review |

---

## 22. Product rules for design and engineering collaborators

### 22.1 Document authority

| Document | Owns | Must not silently decide |
|---|---|---|
| `PRODUCT.md` | Users, outcomes, feature scope, workflow, content semantics, product truth | Technology stack, SQL/API design or brand colors |
| `DESIGN.md` / master design system | Tokens, layouts, navigation appearance, typography, states and motion | Scientific rule approval or product entitlement terms |
| `ARCHITECTURE.md` | Modules, APIs, persistence, RAG pipeline, sessions, workers, provider/deployment contracts | New product promises, unreviewed agronomic formulas |
| `CHATBOT_SPEC.md` [future optional] | Exact chatbot style, tool-use conversational rules, evaluation prompts | Relax product safety gates or authorize numeric formulas |
| Scientific review records | Scientific applicability, source passages, approved rule versions | UI merchandising or billing terms |

### 22.2 Non-negotiable instructions for Codex/design agents

- Treat `[OPEN]` as a blocker for the affected feature or claim, not permission to create an assumption.
- Treat `[CONDITIONAL]` as a real data-dependent state, not a polished fallback populated with invented values.
- Do not replace the approved frontend/backend stack or reinterpret the multi-plot/season ownership semantics from this document.
- Do not port the teammate prototype's unreviewed placeholder lime table or fake soil defaults into the live product.
- Do not render generated HTML unsafely; keep chat answers and research snippets safe and accessible.
- Do not implement fake sources, costs, weather or progress percentages to satisfy a dashboard design.
- A scientific rule becomes executable only after actual human review and test evidence; no blanket auto-approval of YAML rows.
- Preserve meaningful empty/partial/error/stale states alongside successful views.
- Whenever requirements differ, document a proposed decision, affected features and product implications before writing incompatible code.

### 22.3 Feature handoff checklist

- [ ] Which user/job and release scope does this feature serve?
- [ ] What is the authenticated plot/season/plan context?
- [ ] What input is observed, reported, calculated, externally provided or unknown?
- [ ] Is scientific evidence reviewed and applicable to crop, region, soil test and units?
- [ ] What is the success, loading, empty, partial, stale and failure UI?
- [ ] Can the user understand the rationale, source and assumptions?
- [ ] Can a suggested change occur only with visible user intent?
- [ ] Are weather/pricing costs and freshness represented honestly?
- [ ] Can a user return and see their saved plan/conversation?
- [ ] Does mobile, keyboard and reduced-motion access work?
- [ ] Have product and architecture decisions been checked for conflicts?

---

## 23. Source and decision provenance

This document is a consolidation, not independent agronomic verification.

| Input | Contributed context | Important limitation |
|---|---|---|
| `Soil-Smart Planner Team Demo.pdf` | Grower needs, source-linked agronomy, multi-plot inputs, pilot measures and boundaries | Pitch and demonstration inputs do not establish approved live recommendations |
| `Past Conversation on Plantly investor’s perspective.txt` | Grower segmentation, weather/retailer expansion, practical dashboard/AI vision | Strategic ideas are not evidence of working integrations |
| `Plantly_Landing_Design_v4.md` and `PLANTLY_MASTER_DESIGN_SYSTEM(1).md` | Landing direction and shared product UI conventions | Do not confuse designed CTA copy with configured pricing/trials |
| `Plantly - PRODUCT(1)(1).md` | Original v1.0 product baseline and detailed feature intent | Contained open questions later resolved in architecture discussion |
| `PLANTLY_ARCHITECTURE.md` (v1.0) | Locked rounds 1–8 and ARC-047/048; specific implementation boundaries | Engineering decisions are referenced for alignment, not duplicated as product code |
| `PLANTLY_TEAMMATE_RAG_AUDIT(1).md` | Read-only review of deterministic engine, keyword-note retrieval, Claude tools, YAML catalog | Not an executed end-to-end verification or scientific review; source data remains unverified |
| Team decision rounds through 2026-11-07 | Explicit choices on login, persistence, dashboard, scientific narrow MVP and demo scope | Open operational/provider/scientific decisions intentionally remain open |

### 23.1 Changelog

| Version | Date | Change |
|---|---|---|
| 1.0 | 2026-11-07 | Initial product definition: gardener/grower scope, seasonal blueprints, RAG, prices/weather, dashboard/chat, evidence and open choices |
| **2.0** | **2026-11-07** | Reconciled latest locked architecture and science choices; made login-first + public temporary demo explicit; added grower-wide seasons, persistent plan/chat/version behavior, concrete dashboard before/after states, source/metric provenance, approved-rule gate, narrow mixed numerical scope, honest weather/pricing states, detailed chatbot user intents, revised MVP/later scope, resolved old open items and new release blockers |

---

**Product definition complete as a planning baseline. Scientific coverage, business terms and external-provider facts remain gated by the `[OPEN]` decisions above.**
