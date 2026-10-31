# Metaphor Infographic Generator

A reusable spec for producing "explain-a-complex-topic-as-a-visual-metaphor" posts like *The Inference Grid: Six Serving Archetypes*. Paste this file (or the **Master Prompt** in section 4) into an LLM/image model, fill in the `{{variables}}`, and you get a one-page illustrated explainer, a carousel, or a kids' book spread.

---

## 1. The Formula (what makes these posts work)

1. **One familiar metaphor world** carries the whole topic (electric grid, city, kitchen, airport, school, ocean…).
2. **Exactly 4 panels**, numbered, connected by big arrows so the eye follows a path.
3. **Each concept gets a physical object** from the metaphor world (meter, generator, timer, battery…) with a short tagline + one-line "when to use".
4. **A comparison matrix** proves the concepts differ on a few axes (and what stays constant).
5. **One punchline rule** at the end, a single memorable sentence.
6. **A friendly guide character** points at the options and asks the reader to choose.
7. Hand-drawn marker style, pastel panels, handwritten-feel headline, creator credit in the footer.

---

## 2. Inputs (fill these in)

| Variable | Meaning | Example |
|---|---|---|
| `{{TOPIC}}` | Subject to explain | LLM inference serving options |
| `{{AUDIENCE}}` | Who reads it | Engineering leads / kids age 8-10 / execs |
| `{{N_ITEMS}}` | Number of options/archetypes (4-8, 6 is ideal) | 6 |
| `{{METAPHOR_WORLD}}` | Familiar domain to map onto | Electric power grid |
| `{{AXES}}` | 2 tradeoff dimensions for the "Start Here" map | Latency budget x Runtime location |
| `{{CONSTANT}}` | What does NOT change across options | Identical model weights |
| `{{COMPARE_COLUMNS}}` | 3-4 matrix columns | Weights, Standard rate, Off-peak discount |
| `{{PUNCHLINE}}` | The one rule to remember | Spend is an allocation problem, not a modeling problem |
| `{{CREDIT}}` | Footer handle/site | @yourhandle \| yoursite.dev |
| `{{FORMAT}}` | Poster / carousel / book spread | Single 4:5 poster |

---

## 3. Build Workflow (do these in order)

### Step 1: Find the insight
Ask: *"What do people get wrong about {{TOPIC}}?"* The answer becomes the punchline. (Inference grid: people optimize the model when they should optimize where/how it is served.)

### Step 2: List the options
Write `{{N_ITEMS}}` distinct options. Each must differ on at least one axis. Name each with a plain term plus a metaphor term, e.g. `1. Real-Time Mains (Standard Rate)`.

### Step 3: Choose the two axes
Pick two real tradeoffs. Place every option on the 2-D map (Panel 1). A big X/cross of arrows over the axes shows the tension.

### Step 4: Map each option to a metaphor object
Use the bank in section 6. Rule: the object's real-world behavior must mirror the option's behavior (generator = guaranteed availability; off-peak timer = delay-tolerant cheap batch).

### Step 5: Write each item card (max 25 words)
```
N. METAPHOR NAME
(Real term / pricing tag)
What it does. Best for X. Tradeoff Y.
```

### Step 6: Build the matrix
Rows = options, columns = `{{COMPARE_COLUMNS}}`. Include one column that is the same for every row (the `{{CONSTANT}}`) with green checks, so the differences elsewhere stand out. Highlight 1-2 "sweet spot" rows in yellow/green.

### Step 7: Write the punchline
Bold, under 15 words, plus a one-line sub-rule ("Align X with Y").

### Step 8: Add the guide character
Friendly person in bright clothing, center of Panel 2, speech bubble: *"Choose your {{path}} based on {{axis A}} & {{axis B}}!"*

---

## 4. Master Prompt (copy/paste into an LLM or image model)

```
Create a hand-drawn, marker-illustration style infographic poster titled
"{{TITLE}}: {{N_ITEMS}} {{TOPIC_NOUN}} Archetypes".

Audience: {{AUDIENCE}}. Format: {{FORMAT}}, portrait 4:5.
Use the metaphor world: {{METAPHOR_WORLD}}.

LAYOUT (four numbered panels joined by thick blue curved arrows):

PANEL 1 - "START HERE" (cream/yellow, top-left, small):
  Illustration of the metaphor's source/origin ({{SOURCE_OBJECT}}), labeled
  "{{SOURCE_LABEL}}". Below it, a 2-axis chart with a crossed double-arrow X.
  Y-axis: {{AXIS_Y}}. X-axis: {{AXIS_X}}.

PANEL 2 - the {{N_ITEMS}} options (light blue, large, wobbly rounded border
  with offset shadow, top-right). Arrange options in a ring around a smiling
  guide character (red jacket, yellow top, yellow sneakers) with the speech
  bubble "Choose your path based on {{AXIS_Y_SHORT}} & {{AXIS_X_SHORT}}!".
  Each option = one illustrated object + number + bold name + (subtitle) +
  1-2 line description:
{{OPTION_LIST}}

PANEL 3 - "COMPARISON MATRIX" (salmon/pink, bottom-left): table with rows =
  options and columns = {{COMPARE_COLUMNS}}. Green checkmarks in the constant
  column ("{{CONSTANT}}"). Highlight rows {{HIGHLIGHT_ROWS}} with yellow/green
  marker strokes.

PANEL 4 - "KEY ENGINEERING RULE" (mint green, bottom-right): large bold text:
  "{{PUNCHLINE}}" with a smaller line "{{SUBLINE}}".

STYLE: black ink outlines, flat pastel fills, hatch-pattern panel borders,
  hand-lettered condensed sans headings, handwritten-feel body, thick arrows,
  lots of white space, no photorealism, no gradients. Underlined hand-drawn
  main title. Footer credit in a small white rounded box, bottom-right:
  "{{CREDIT}}".

CONSISTENCY: same character, same line weight, numbers 1-{{N_ITEMS}} match
  between Panel 2 and Panel 3. All text must be legible and spelled correctly.
```

---

## 5. Output Variants

### A. Text-only (for LLMs without image generation)
Ask for the content as Markdown first, then render it as HTML/SVG or hand it to a designer:
```
Produce the infographic content for {{TOPIC}} as:
1. Title
2. Panel 1: source label + axes + placement of each option on the map
3. Panel 2: N item cards (name, subtitle, <=25 words, metaphor object to draw)
4. Panel 3: markdown table (options x columns)
5. Panel 4: punchline + subline
6. Image-generation prompt (fill in the Master Prompt)
```

### B. Carousel (LinkedIn/Instagram, 6-8 slides)
1. Hook slide: title + metaphor illustration
2. "Start here": axes map
3-6. Two options per slide (object + tagline + when to use)
7. Matrix
8. Punchline + CTA + credit

### C. Kids' book (one topic per spread)
- Left page: the metaphor character meets the problem (1-2 sentences, age-appropriate words).
- Right page: the options as friendly objects, each with a one-line job.
- Last spread: the punchline as "The Big Idea", with a "Your turn: which would you pick?" question.
- Keep reading level to `{{AUDIENCE}}`; swap jargon for the metaphor term and define the real term once in a small "Grown-up word" box.

### D. Slide deck
One slide per panel; panel 2 can split into N sub-slides.

---

## 6. Metaphor Bank (map option behaviors to objects)

| Behavior | Electric grid | City/transport | Kitchen/restaurant | Airport |
|---|---|---|---|---|
| Default / on-demand | Standard meter | City bus | Order a la carte | Standard ticket |
| Guaranteed fast / premium | Hospital generator | Ambulance lane | Chef's table | Priority boarding |
| Cheap, can wait | Off-peak timer | Night freight | Meal prep batch | Standby fare |
| Reserved capacity | Dedicated transformer | Season pass | Catering contract | Chartered jet |
| Own it yourself | Solar panels | Own car | Home kitchen | Private hangar |
| Runs locally / offline | Power bank | Walking | Packed lunch | Carry-on only |

Other worlds: **library, postal service, water system, farm-to-table, theme park fast-pass, ocean shipping, orchestra, hospital triage, subway map**.

---

## 7. Quality Checklist

- [ ] One metaphor world, used consistently (no mixed metaphors)
- [ ] Each option's object mirrors its real behavior
- [ ] Axes are real tradeoffs, and every option is placed on them
- [ ] Matrix has a constant column plus highlighted rows
- [ ] Punchline is <15 words and quotable
- [ ] Numbers match across panels
- [ ] Every item card <=25 words; no jargon without the metaphor term beside it
- [ ] Style consistent (outline weight, palette, character)
- [ ] Credit footer included
- [ ] Factual accuracy of the underlying topic verified (pricing, specs, and claims)

---

## 8. Worked Example (the reference infographic)

| Field | Value |
|---|---|
| Title | The Inference Grid: Six Serving Archetypes |
| Metaphor | Electric power grid |
| Axes | Latency budget (vertical) x Runtime location, cloud to edge (horizontal) |
| Constant | Identical model weights across all six |
| Options | 1 Real-Time Mains (standard) / 2 Premium-Speed generator (priority) / 3 Flex-Batch off-peak timer (discount) / 4 Provisioned transformer (reserved) / 5 Self-Hosted solar (on-prem GPUs) / 6 On-Device power bank (local silicon) |
| Matrix columns | Weights flow, Standard rate, Off-peak discount |
| Highlights | Flex/Batch (yellow), Provisioned (green) |
| Punchline | "Inference spend is an allocation problem, not a modeling problem." |
| Subline | Align serving archetype with business value & constraints. |

### More topic seeds
- **Cloud storage tiers** x city logistics (hot/cold/archive as warehouses)
- **Auth methods** x airport security (passport, boarding pass, TSA PreCheck...)
- **Database types** x library (card catalog, stacks, reading room...)
- **Incident response levels** x hospital triage
- **How the internet works (for kids)** x postal service

---

## 9. Tips

- Draft text first and image second; most failures are content problems, not art problems.
- Image models garble small text: keep each card under 25 words, or generate the art without text and overlay the text in Figma/Canva.
- Generate the character once and reuse it across a series for brand consistency.
- Iterate panel by panel if the single-shot poster comes out cluttered.
