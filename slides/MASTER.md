---
title: The Modern Researcher's Tech Stack
subtitle: Using AI agents for academic research
template: ../templates/cbs-template.pptx
font: Century Gothic
sessions: 2
---

<!-- WORKSHOP MASTER DECK — both sessions in one file for fast single-pass review.
     Split into session-1/ and session-2/ per-module files later.
     Structure: `#` = Session (divider), `##` = Module (section header), `### Slide` = slide.
     Each slide: On slide / Visual / Notes. Fonts + palette: ../templates/cbs-style.md
     (Century Gothic, #0081CC). Image-note paths are relative to this file (assets/...). -->

# Session 1 — Integrating AI tools into the research workflow

## Module 0 — Why this matters
_~10 min_

### Slide — Why this matters
**On slide:**
- AI you can *talk to* is old news. **AI that works inside your project** is the shift.
- Today's goal: Claude Code running inside your actual research workflow.

**Notes:**
> Everyone has used a chatbot; almost no one has handed an agent their real project folder. That leap is what today is about.

### Slide — The promise: an agent in your repo
**On slide:**
- Reads your files, runs your code (R / Stata / Python), edits in place, iterates.
- Works on data too big to paste — a 100 GB parquet is just a file it can query.
- Long-running tasks: clean, merge, plot, draft — while you supervise.

**Visual:** `assets/agent-in-repo.svg` — project folder + Claude reading/writing files beside a terminal running code.

**Notes:**
> The point isn't "AI is powerful" — it's that the agent operates on YOUR files and data, not a copy pasted into a box.

### Slide — The "RA" analogy (and where it breaks)
**On slide:**
- **Like a research assistant:** give it context, it does the legwork, you review.
- **Unlike an RA:** instant, tireless; *no memory* between sessions unless you give it one (`CLAUDE.md`); and it will confidently make things up — so **you verify**.

**Notes:**
> An RA remembers last week; the agent doesn't unless you persist context. An RA says "I'm not sure"; the agent often won't. Verification is your job — which is why we teach git early.

## Module 1 — Four ways to work with Claude
_~15 min_

### Slide — Four ways to work with Claude
**On slide:**
- Same model underneath — what changes is **how much of your machine it sees** and **how much it does on its own**.
- Chat · Cowork · VS Code extension · Terminal — one spectrum, conversational → agentic.

**Visual:** `assets/four-modes-spectrum.svg` — horizontal spectrum, four modes over a grey→blue gradient (`#9E9A92` → `#0081CC`); left "you bring the context", right "full system access"; pill "▸ We spend our time on VS Code + Terminal". [Approved 2026-06-05.]

**Notes:**
> The key reframe: not four products you choose between — four cockpits on the same engine. Move fast here.

### Slide — Same engine, different cockpit
**On slide:**
- The *same* request, three ways: **Chat** (paste in, copy out) · **Cowork** (edits a local doc; no terminal) · **Claude Code** (reads files, runs code, edits in place — you watch).
- Output is essentially the same; what differs is **friction** and **reach**.

**Notes:**
> Demystify. The anxiety comes from thinking these are different AIs — they aren't.

### Slide — So why the terminal?
**On slide:**
- **Real data access** — your 100 GB parquet never fits in a chat window; here DuckDB just queries it.
- **Long-running, iterative edits** — across your whole project, not one pasted snippet.
- Extensible: MCP · skills · plugins · subagents.

**Notes:**
> Jesse's line: "you can't upload a 100 GB parquet to chat, but watch — we work with DuckDB without anyone needing to know what a database is."

### Slide — Where we'll focus
**On slide:**
- **VS Code** — the on-ramp: open a folder, *see* your files, ask Claude to explain the project.
- **Terminal** — the power end: everything above, scriptable, over SSH.

**Notes:**
> Go fast past Chat / Cowork, then spend real time in VS Code + the terminal. "Linux, not macOS": a little setup, then enormous leverage.

## Module 2 — What a coding agent actually is
_~12 min_

### Slide — The terminal: your computer's full control surface
**On slide:**
- One text prompt can drive *anything* the machine does: edit files, run programs (R / Stata / Python), install software, download data, hit the network, automate it all.
- The GUI — windows and buttons — is a convenient *subset*; the terminal is the full set.

**Visual:** (live demo) — run a few commands: `ls`, a one-line R / Python snippet, `curl` a file.

**Notes:**
> Don't lecture — *show* it. A 60-second live demo. Takeaway: the terminal is the whole computer, in text. Sets up the reveal.

### Slide — A coding agent = an LLM + a terminal
**On slide:**
- Take a language model. Let it **type commands into a terminal and read the output**, in a loop.
- That's the whole trick: an LLM with **hands** (the terminal) and **eyes** (your files).

**Visual:** `assets/llm-plus-terminal.svg` — LLM box + terminal box → "agent", with a loop arrow (act → read output → act).

**Notes:**
> The demystifying "aha." Everything else — modes, MCP, skills — is detail on top of this one idea. Once people get "LLM + terminal," agents stop feeling like magic.

### Slide — Same idea, several tools
**On slide:**
- Claude Code · Codex · Cursor · OpenCode — all "an LLM + a terminal / editor."
- We teach **Claude Code** (stronger auto mode). Codex users welcome — we'll help.

**Notes:**
> Don't get religious — the concept transfers.

### Slide — Power cuts both ways → verify & guardrail
**On slide:**
- Because it can do *anything*, it can also do the wrong thing **confidently** (hallucinations).
- Defenses: **run** the code, **check** outputs, **commit to git** so nothing is silently lost.

**Notes:**
> Motivates permission modes (Module 6) and git (Module 8) — guardrails are what make the power safe.

## Module 3 — Installing Claude Code
_~15 min_

### Slide — What you need first
**On slide:**
- A terminal + **Homebrew** (the macOS package manager).
- Your research runtimes: **Python**, **R**, **Stata** — whatever you use.

**Notes:**
> Keep installs minimal and language-agnostic. Homebrew is the common denominator on Mac.

### Slide — Install Claude Code
**On slide:**
- One installer → `claude` available in your terminal.
- `claude` to start; `/login` to authenticate.

**Notes:**
> Live-install if the room's ready; otherwise show the command and the first-run screen.

### Slide — First run
**On slide:**
- `claude` inside any project folder → it reads that folder.
- Pick a model; you're in.

**Notes:**
> It sees the folder you start it in. That's the mental model for "what can it touch."

## Module 4 — The terminal, your editor & your first session
_~25 min_

### Slide — The terminal, demystified
**On slide:**
- You saw it can do anything — but *you* only need ~5 commands.
- You don't need to be a "terminal person."

**Notes:**
> Callback to Module 2. Lower the intimidation: it's just a launcher.

### Slide — VS Code is your cockpit
**On slide:**
- Open a folder → **see your files** and exactly what Claude can access.
- Built-in terminal at the bottom; run `claude` there.
- Edits appear as **diffs** you accept or reject.

**Visual:** `assets/vscode-cockpit.svg` — VS Code: file tree left, integrated terminal bottom running `claude`, a diff open.

**Notes:**
> The recommended starting point. The win is visibility: you watch the agent, file by file.

### Slide — Your first session: an existing project
**On slide:**
- `cd your-project` → `claude` (or open the folder in VS Code and use the bottom terminal).
- Ask *"summarize this project,"* then run **`/review`** to get a code review of it.
- Read-only by default — nothing changes without your say-so.

**Visual:** (hands-on) — open a real project and run `/review`.

**Notes:**
> First hands-on: bring your own project. Summarize → `/review` (or a code-review plugin from the CBS marketplace). The "aha" is watching it actually understand YOUR code — safely, no edits.

### Slide — Starting a new project
**On slide:**
- From nothing: `mkdir my-paper && cd my-paper` → `claude`.
- `/init` writes a `CLAUDE.md`; describe your goal in **Plan mode**; let it scaffold the structure + first code.

**Notes:**
> The other on-ramp — from an empty folder. Pairs with Session 2's "blank folder → result" demo. Show how fast a working skeleton appears.

### Slide — Multiplexing (optional power)
**On slide:**
- tmux / zellij: many panes; long jobs that survive disconnects.
- cmux: tabbed setup with a browser — nice once you multitask.

**Notes:**
> Optional/advanced. Flag it for the keen; don't scare beginners.

### Slide — Linux, not macOS
**On slide:**
- A set-it-up-yourself experience, not a polished app.
- A little configuration up front → large, durable leverage.

**Notes:**
> Set the expectation honestly so people invest the 30 minutes.

## Module 5 — Claude Code at Columbia
_~10 min_

### Slide — Access & pricing
**On slide:**
- How to get Claude Code through Columbia (account / credits).
- What's covered vs a personal API key.

**Notes:**
> Fill exact Columbia details at build time. Costs are usage-based; `/cost` shows spend.

### Slide — Privacy & your data
**On slide:**
- What leaves your machine vs stays local.
- Sensitive / IRB data: know the boundary **before** pointing an agent at it.

**Notes:**
> Be concrete and cautious. Give a clear rule of thumb and where to check policy.

## Module 6 — Driving Claude Code
_~20 min_

### Slide — Permission modes
**On slide:**
- **Plan** (think first, no edits) · **Accept edits** · **Auto** (runs tools itself) · **Skip permissions** ("YOLO" — careful).
- Start in Plan; graduate to Auto as you trust it.

**Notes:**
> The steering wheel. Match mode to risk. YOLO only in throwaway / sandboxed contexts.

### Slide — Working with an agent *is* managing context
**On slide:**
- The agent only knows what's in its **context window** — your files, what you've said, what it has read.
- Most "it got worse / went off track" moments are really **context** problems.
- Your job shifts from writing code to **curating what the agent can see** — right things in, noise out.

**Notes:**
> The second big idea, after "LLM + terminal": you're not programming, you're managing attention. Frame everything else — `/compact`, `CLAUDE.md`, `/clear` — as context hygiene.

### Slide — The context window & /compact
**On slide:**
- The window is **finite**; as it fills, early details fade and quality drops.
- **`/compact`** = summarize the conversation so far into a shorter form — frees space while keeping the gist, so a long session doesn't degrade or hit the limit.
- **`/clear`** = wipe and start fresh when you switch tasks.

**Notes:**
> Make `/compact` concrete: a "keep the summary, drop the transcript" button. Demo it mid-task. Rule of thumb — one task per session; `/compact` when it's getting long, `/clear` when you move on.

### Slide — Slash commands you'll actually use
**On slide:**
- `/init` · `/clear` · `/compact` · `/resume` · `/cost`.

**Notes:**
> Keep to the few they'll use day one. `/cost` reassures the budget-conscious.

### Slide — CLAUDE.md is project memory
**On slide:**
- A file in your repo the agent reads every time — conventions, data locations, gotchas.
- `/init` drafts one; you refine it.

**Notes:**
> The "give your RA a memory" point, paid off. Show a tiny example.

## Module 7 — Demo: chatbot vs Claude Code
_~15 min_

### Slide — The task
**On slide:**
- Treasury International Capital (TIC) data: pull it, clean it, plot a series.
- Same task, two ways.

**Notes:**
> Quick, real, finance-flavored, everyone can follow.

### Slide — In the chatbot
**On slide:**
- Paste data in, copy code out, run it yourself, paste errors back. Repeat.
- Friction scales with data size; big files don't fit.

**Notes:**
> Make the friction visible. The "before."

### Slide — In Claude Code
**On slide:**
- "Here's the folder" → it downloads, cleans, plots, fixes its own errors.
- You watch and verify.

**Notes:**
> The "after." Same result, a fraction of the friction.

## Module 8 — Version control with git
_~20 min_

### Slide — Why git (especially now)
**On slide:**
- An agent edits many files fast. Git is your **undo** and your **record**.
- Without it, a bad run can quietly clobber work.

**Notes:**
> Git as a safety net for working with an agent, not engineering ceremony.

### Slide — The minimal workflow
**On slide:**
- `git init` · `git add` · `git commit` · `git branch` · `git diff`.
- Commit before you let the agent loose; commit again when it's good.

**Notes:**
> Five commands. Claude can run them for you. Show, don't lecture.

### Slide — When Claude breaks something
**On slide:**
- `git diff` to see what changed; `git restore` / revert to undo.
- A clean commit means you can always get back.

**Notes:**
> The payoff for the verification theme. Demonstrate breaking, then reverting.

## Module 9 — Assignments
_~5 min_

### Slide — Your assignments
**On slide:**
- **Redo:** take one finished project — how could it have been faster / better with an agent?
- **Dream:** brainstorm a project that was impossible before AI.
- **Bring data:** come to Session 2 with your own data to analyze.

**Notes:**
> These prime Session 2. Encourage real (non-sensitive) data; a fallback sample is provided.

# Session 2 — AI for academic research

## Module 0 — Recap & common failures
_~10 min_

### Slide — Since Session 1
**On slide:**
- What did you try? What broke?
- Quick round the room: one win, one wall.

**Notes:**
> Start social; surface real problems to troubleshoot live.

### Slide — The usual failure modes
**On slide:**
- Lost context (a long session drifted) · over-trusting unverified output · no git safety net · vague prompts.
- Each has a fix we'll cover today.

**Notes:**
> Normalize failure and map each one to today's modules.

## Module 1 — Context management
_~15 min_

### Slide — Why long sessions degrade
**On slide:**
- The context window is finite; as it fills, early details fade and quality drops.
- "It got dumber" usually means "the window is full."

**Notes:**
> Make the window concrete — the #1 cause of degraded sessions.

### Slide — /compact and /clear
**On slide:**
- `/compact`: summarize and keep going. `/clear`: hard reset between tasks.
- One task per session; don't let it sprawl.

**Notes:**
> Practical hygiene. Demo a `/compact` mid-task.

### Slide — The memory hierarchy
**On slide:**
- **user** (`~/.claude/CLAUDE.md`) · **project** (`./CLAUDE.md`) · **local** (`.claude/settings.local.json`).
- Put durable facts in `CLAUDE.md` so you never re-explain.

**Notes:**
> Tie back to "give your RA a memory." Show the three levels live.

## Module 2 — Extending Claude Code (skills, MCP, plugins, hooks)
_~30 min_

### Slide — Ways to extend it
**On slide:**
- **Skills · MCP · Plugins · Subagents · Hooks · custom slash commands** — bolt new capabilities onto the LLM + terminal core.

**Notes:**
> Frame as "more tools and hands" on the same agent from Session 1.

### Slide — MCP (Model Context Protocol)
**On slide:**
- A standard way to plug in tools/data: databases, APIs, services (Qualtrics, WRDS, …).
- Install once; the agent gains a new power.

**Notes:**
> MCP = the agent's plug-in ports. Connect one live.

### Slide — Skills
**On slide:**
- Reusable, packaged know-how and commands.
- Example: a **Stata skill** to run Stata from the command line.

**Notes:**
> Demo the Stata skill — big for this audience (R/Stata/Python parity).

### Slide — Plugins & a CBS marketplace
**On slide:**
- Plugins bundle skills / MCP / commands; install from a **marketplace**.
- We're building a **CBS marketplace** — add it once, install what you need.

**Notes:**
> Tease the marketplace deliverable; everyone installs by the end.

### Slide — Subagents & output styles
**On slide:**
- **Subagents:** parallel helpers for big tasks.
- **Output styles** (Explanatory / Learning) tune voice — handy for academic writing.

**Notes:**
> Keep light; point to where each helps research.

### Slide — Git worktrees
**On slide:**
- Run several agent tasks in parallel on separate branches without collisions.

**Notes:**
> Advanced; cmux makes worktrees painless.

### Slide — Hooks
**On slide:**
- Run **your own shell commands automatically on events** — format after every edit, run tests on save, ping you when a long task finishes.
- Configured in settings; the agent triggers them, you don't.

**Notes:**
> Hooks = automation *around* the agent. Great for "always do X after Y" without remembering — and for reproducible pipelines.

## Module 3 — Remote work
_~20 min_

### Slide — Claude where you aren't
**On slide:**
- `claude --teleport` // `/teleport` · `/remote-control` (drive it from your phone) · `claude --remote`.

**Notes:**
> Show remote-control from a phone — a crowd-pleaser.

### Slide — The Research Grid
**On slide:**
- SSH into Columbia's compute; run long jobs.
- tmux / zellij so sessions survive disconnects.

**Notes:**
> For heavy data/compute. Pair with worktrees + tmux.

## Module 4 — Collaborative demo
_~25 min_

### Slide — Blank folder → result, live
**On slide:**
- Empty folder → a finding, using Columbia data.
- Plan: query **WRDS** for a country's **CDS** series → find dates of relevant news → visualize the risk spike.

**Notes:**
> The flagship live build. Straightforward, interesting, everyone can replicate.

### Slide — Demo 2 — Qualtrics MCP
**On slide:**
- Pull survey data through the **Qualtrics MCP**; analyze in place.

**Notes:**
> Shows MCP on a real research data source.

## Module 5 — Your project, the plan-mode way
_~25 min_

### Slide — Turn your idea into a plan
**On slide:**
- In **Plan mode**, write the prompt; let it draft a plan. Don't execute yet.

**Notes:**
> The structured workflow. Plan first — the plan is the artifact.

### Slide — Iterate the plan (get a second opinion)
**On slide:**
- Read and edit the plan by hand; ask **another model** (e.g., GPT) to critique it.

**Notes:**
> Cross-model review catches gaps before you spend compute.

### Slide — Execute & supervise
**On slide:**
- Run in **Auto** (or skip-permissions in a safe sandbox); watch, verify, commit.

**Notes:**
> Connect back to permission modes + git from Session 1.

## Module 6 — LLMs for unstructured data
_~20 min_

### Slide — Scrape → structure
**On slide:**
- Example: scrape **EDGAR** filings → build a **parquet / SQLite** with **DuckDB**.
- The agent writes the scraper and the queries; you don't need to know SQL.

**Notes:**
> Powerful for empirical work. Show DuckDB over a big file.

### Slide — Where the compute & credits come from
**On slide:**
- Running inside **Claude / Codex** vs **OpenRouter** credits vs your own **OpenAI / Anthropic API key**.
- Trade-offs: convenience, cost, control.

**Notes:**
> Demystify billing/keys — people get confused here.

### Slide — (Time permitting) Writing like you
**On slide:**
- Generate a style file from your past writing; draft new text in your voice.

**Notes:**
> Optional, fun closer for the writing-inclined.

## Module 7 — Show & tell
_~20 min_

### Slide — Show your result
**On slide:**
- Quick interactive presentations: what you built, what surprised you.

**Notes:**
> The payoff. Keep it moving; celebrate progress.

## Module 8 — Security & good hygiene
_~10 min_

### Slide — Working safely
**On slide:**
- Sandboxing / containers for risky runs; mind secrets & keys; use permission modes; git as undo.
- Sensitive / IRB data: keep it local; know what leaves your machine.

**Notes:**
> Close on responsible use. Containers are optional/advanced.
