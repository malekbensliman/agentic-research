---
module: Four ways to work with Claude
session: 1
order: 1
duration_min: 15
template: ../../templates/cbs-template.pptx
learning_goals:
  - Recognize the four ways to use Claude and how they differ
  - Internalize that all four run the same model — what changes is environment access + autonomy
  - Understand why research workflows live at the VS Code + Terminal end
---

# Slide 1 — Four ways to work with Claude
<!-- layout: Title and Content -->

**On slide:**
- Same model underneath — what changes is **how much of your machine it sees** and **how much it does on its own**.
- Chat · Cowork · VS Code extension · Terminal — one spectrum, conversational → agentic.

**Visual:** `../assets/four-modes-spectrum.svg` — horizontal spectrum, four modes left→right over a grey→blue gradient (`#9E9A92` → `#0081CC`); left label "conversational · isolated — you bring the context", right label "agentic · integrated — full system access"; bottom-right pill (`#0081CC`) "▸ We spend our time on VS Code + Terminal". Font: Century Gothic. [Spectrum layout approved 2026-06-05.]

**Notes:**
> The key reframe: these aren't four products you choose between — they're four cockpits on the same engine. "Should I use Cowork or Claude Code for research?" really means "how much do I want the agent to see and do?" Move fast here.

---

# Slide 2 — Same engine, different cockpit
<!-- layout: Two Content -->

**On slide:**
- The *same* request, three ways:
  - **Chat** — you paste the data, copy the answer back by hand.
  - **Cowork** — it edits your local doc / sheet; no terminal.
  - **Claude Code** — it reads your files, runs code, edits in place — and you watch.
- Output is essentially the same; what differs is **friction** and **reach**.

**Visual:** (optional) three small panels, same prompt → same answer.

**Notes:**
> Demystify. The anxiety comes from thinking these are different AIs — they aren't. Show the same question answered in each, then: "do it however you like, but here's why the terminal end wins for real work."

---

# Slide 3 — So why the terminal?
<!-- layout: Title and Content -->

**On slide:**
- Two things only the filesystem-aware modes give you:
  - **Real data access** — your 100 GB parquet never fits in a chat window; here DuckDB just queries it.
  - **Long-running, iterative edits** — across your whole project, not one pasted snippet.
- Extensible: MCP · skills · plugins · subagents.

**Visual:** `../assets/why-terminal.svg` — (to build) a chat window "⚠ file too large" beside a terminal running a DuckDB query over a big file.

**Notes:**
> Jesse's line: "Here's my 100 GB parquet — you can't upload it to chat, but watch, we work efficiently with DuckDB without anyone needing to know what a database is." This sells the approach to a research audience.

---

# Slide 4 — Where we'll focus
<!-- layout: Section Header -->

**On slide:**
- **VS Code** — the on-ramp: open a folder, *see* your files, ask Claude to explain the project.
- **Terminal** — the power end: everything above, scriptable, over SSH.

**Notes:**
> We go fast past Chat / Cowork, then spend our real time in VS Code + the terminal. Frame it "Linux, not macOS": a little setup, then enormous leverage.
