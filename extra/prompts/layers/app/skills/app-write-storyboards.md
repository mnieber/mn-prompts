# Writing storyboards

A storyboard explains a part of the design to a human reader, as a short sequence of frames. Each frame is an
infographic with a message underneath. A storyboard is documentation, not a spec: it is not part of the five
development phases, and no code or test is derived from it.

`RULE`: only write a storyboard when I ask for one, and only about a design that has settled (usually: its scenarios
exist). A storyboard is expensive to redraw, so it should not chase a design that is still changing.

## Where a storyboard lives

Each storyboard has its own directory:

```
doc/storyboards/<storyboard_slug>/
  storyboard.md
  frame_01_<frame_slug>.svg
  frame_02_<frame_slug>.svg
  ...
```

`storyboard.md` has this layout:

```markdown
---
title: A central server stores a debate
sources:
  - extra/spec/design/personal_data.md
  - src/services/<service>/doc/spec/scenarios/s020_<name>.md
artifact: https://claude.ai/artifact/<id>
---

# A central server stores a debate

<One paragraph: what the storyboard aims to explain.>

## <Frame title>

![<Alt text: what the frame shows, in one or two sentences.>](frame_01_<frame_slug>.svg)

<The message: two to four sentences that explain the frame to the reader.>
```

- `sources` lists the files that the storyboard was drawn from. It is the exception to the rule against
  cross-references: it is how we find out that a frame may be stale (see below).
- `artifact` is the URL of the published slide show, if there is one. It is optional.
- The SVG files are the source of the frames. There is no other source (no generator script, no YAML).

## What a frame should be

`RULE`: a frame is an infographic, not a box-and-arrow diagram. If the frame could also have been a Mermaid diagram,
it doesn't add anything to the scenario specs, which already contain those.

What makes a frame informative:

- One idea per frame. A storyboard has three to six frames.
- Show the mechanism with concrete example data (statement 3, log entry #8, debate 41, a URL with a `#key=`
  fragment), so the reader sees the idea at work instead of reading about it.
- Use space to carry meaning: one column per machine or actor, one lane per actor in a sequence, side-by-side
  cards for "before / after" or "what A sees / what B sees".
- Use visual metaphors where they help: a log as a tape of numbered cells, a secret as a key in a vault, a
  blocked flow as a no-entry sign, encrypted text as ciphertext or grey bars.
- Keep the vocabulary consistent across the frames of a storyboard: the same colour per actor, the same icons, the
  same placement.
- Number steps only when the order is real. Annotate the frame with short labels; put explanations in the message.
- Make example data look like examples (`oaky.example`, shortened tokens such as `tq7f…`). Take every fact from
  the `sources`, never from assumptions.

## How to write the SVG

`RULE`: start each frame from the template
[examples/blogs/doc/storyboards/template_frame.svg](../../../examples/blogs/doc/storyboards/template_frame.svg). It is
only a template: copy its `<style>`, `<defs>` and background rectangle, and replace its content (after the `CONTENT`
comment) with the frame's own drawing. Its content shows the visual vocabulary (actor boxes, shared and private
zones, a log tape, a numbered step, arrows, a no-entry sign), but don't copy its layout when another layout tells the
frame's story better.

Each SVG must render on its own, inside an `<img>` tag on GitHub:

- The frames are dark-only: a dark background card, whatever the theme of the page around it. There is no light
  palette and no `prefers-color-scheme` query.
- The root element has `xmlns`, a `viewBox`, and `width` and `height` that are equal to the size of the viewBox
  (e.g. 960 × 520). The first child is a `<title>` with the alt text.
- A `<style>` element defines every colour as a token on `:root`. Shapes and text use classes that refer to the
  tokens, never literal colours. Add a token when a frame needs a colour that the template doesn't have.
- The first shape is the background rectangle of the template.
- Use system font stacks (e.g. `system-ui, "Segoe UI", Helvetica, Arial, sans-serif`, and `ui-monospace, Menlo,
  Consolas, "DejaVu Sans Mono", monospace`). An SVG in an `<img>` cannot load web fonts.
- Fallback fonts differ in width, so leave about 15% spare room after each text. When two text runs sit on one
  line, put them in one `<text>` with `<tspan>`s, so the second one follows the first instead of sitting at a
  fixed `x`.
- Put the icons (`<symbol>`) and arrowheads (`<marker>`, one per colour) in `<defs>`, and place them with `<use>`.
- No external references: no images, fonts or scripts.

`RULE`: after drawing or changing a frame, render it, look at the result, and fix overlapping or clipped text (also
text that touches the edge of its box). For example:

```bash
google-chrome --headless=new --hide-scrollbars --window-size=960,520 --screenshot=frame.png <frame>.svg
```

## Updating a storyboard

A frame holds more information than any description of it, so we accept that a storyboard can become somewhat
stale, and we update it conservatively.

- To find frames that may be stale, compare the last commit of each SVG with the last commits of the `sources`
  (e.g. `git log -1 --format=%ci -- <file>`). Then check the frame against the changed source, and only redraw what
  is now wrong.
- Edit the SVG directly. Small changes (a label, an extra item) are cheap; a change that moves many elements is
  about as expensive as drawing the frame again.
- Keep the message and alt text in `storyboard.md` in step with the frame.

## The slide show

When I ask for a slide show, build an HTML page from `storyboard.md` and the SVGs (one slide per frame: the title,
the frame, and the message underneath), publish it as an artifact, and put its URL in the `artifact` field. When the
storyboard changes later, republish to the same URL.
