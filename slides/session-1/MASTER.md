---
session: 1
title: Integrating AI tools into the research workflow
template: ../../templates/cbs-template.pptx
font: Century Gothic
duration_min: ~150
---

<!-- MASTER deck for Session 1 — every module in one file for fast review.
     We split into per-module files (00-why.md, 01-four-modes.md, …) later.
     Structure: `#` = module (renders as a Section Header slide), `##` = slide.
     Each slide: On slide / Visual / Notes. Palette + fonts: ../../templates/cbs-style.md (Century Gothic, #0081CC). -->

# Module 0 — Why this matters
_~10 min_

## Slide — Why this matters
**On slide:**
- AI you can *talk to* is old news. **AI that works inside your project** is the shift.
- Today's goal: Claude Code running inside your actual research workflow.

**Notes:**
> Everyone has used a chatbot; almost no one has handed an agent their real project folder. That leap is what today is about.

## Slide — The promise: an agent in your repo
**On slide:**
- Reads your files, runs your code (R / Stata / Python), edits in place, iterates.
- Works on data too big to paste — a 100 GB parquet is just a file it can query.
- Long-running tasks: clean, merge, plot, draft — while you supervise.

**Visual:** `../assets/agent-in-repo.svg` — project folder + Claude reading/writing files beside a terminal running code.

**Notes:**
> The point isn't "AI is powerful" — it's that the agent operates on YOUR files and data, not a copy pasted into a box.

## Slide — The "RA" analogy (and where it breaks)
**On slide:**
- **Like a research assistant:** give it context, it does the legwork, you review.
- **Unlike an RA:** instant, tireless; *no memory* between sessions unless you give it one (`CLAUDE.md`); and it will confidently make things up — so **you verify**.

**Notes:**
> An RA remembers last week; the agent doesn't unless you persist context. An RA says "I'm not sure"; the agent often won't. Verification is your job — which is why we teach git early.

# Module 1 — Four ways to work with Claude
_~15 min_

## Slide — Four ways to work with Claude
**On slide:**
- Same model underneath — what changes is **how much of your machine it sees** and **how much it does on its own**.
- Chat · Cowork · VS Code extension · Terminal — one spectrum, conversational → agentic.

**Visual:** `../assets/four-modes-spectrum.svg` — horizontal spectrum, four modes over a grey→blue gradient (`#9E9A92` → `#0081CC`); left "you bring the context", right "full system access"; pill "▸ We spend our time on VS Code + Terminal". [Approved 2026-06-05.]

**Notes:**
> The key reframe: not four products you choose between — four cockpits on the same engine. "Cowork or Claude Code for research?" really means "how much do I want the agent to see and do?" Move fast here.

## Slide — Same engine, different cockpit
**On slide:**
- The *same* request, three ways:
  - **Chat** — you paste the data, copy the answer back by hand.
  - **Cowork** — it edits your local doc / sheet; no terminal.
  - **Claude Code** — it reads your files, runs code, edits in place — and you watch.
- Output is essentially the same; what differs is **friction** and **reach**.

**Notes:**
> Demystify. The anxiety comes from thinking these are different AIs — they aren't.

## Slide — So why the terminal?
**On slide:**
- **Real data access** — your 100 GB parquet never fits in a chat window; here DuckDB just queries it.
- **Long-running, iterative edits** — across your whole project, not one pasted snippet.
- Extensible: MCP · skills · plugins · subagents.

**Notes:**
> Jesse's line: "Here's my 100 GB parquet — you can't upload it to chat, but watch, we work with DuckDB without anyone needing to know what a database is." This sells the approach.

## Slide — Where we'll focus
**On slide:**
- **VS Code** — the on-ramp: open a folder, *see* your files, ask Claude to explain the project.
- **Terminal** — the power end: everything above, scriptable, over SSH.

**Notes:**
> Go fast past Chat / Cowork, then spend real time in VS Code + the terminal. "Linux, not macOS": a little setup, then enormous leverage.

# Module 2 — Agentic vs chatbot (and verifying)
_~10 min_

## Slide — "Agentic" in one sentence
**On slide:**
- A chatbot answers; an agent **acts** — it plans, runs tools, reads the result, and tries again, in a loop, until the task is done.
- You set the goal and the guardrails; it does the steps.

**Notes:**
> Contrast single-shot Q&A with the perceive–act–observe loop. That loop is why it does real work — and why it needs supervision.

## Slide — The landscape (and our pick)
**On slide:**
- Same idea, several tools: **Claude Code**, Codex, Cursor, OpenCode.
- Largely interchangeable; we teach **Claude Code** (stronger auto mode). Codex users welcome — we'll help.

**Notes:**
> Don't get religious — the concepts transfer. We pick Claude Code for a smoother auto mode.

## Slide — It will make things up — so verify
**On slide:**
- Agents hallucinate: invented functions, wrong numbers, confident errors.
- Defenses: **run** the code, **check** outputs, and **use git** so nothing is silently lost.

**Notes:**
> The honest slide. The fix isn't "trust it less" — it's a workflow that catches errors: execution, checks, version control. Sets up the git module.

# Module 3 — Installing Claude Code
_~15 min_

## Slide — What you need first
**On slide:**
- A terminal + **Homebrew** (the macOS package manager).
- Your research runtimes: **Python**, **R**, **Stata** — whatever you use.

**Notes:**
> Keep installs minimal and language-agnostic; people bring different stacks. Homebrew is the common denominator on Mac.

## Slide — Install Claude Code
**On slide:**
- One installer → `claude` available in your terminal.
- `claude` to start; `/login` to authenticate.

**Notes:**
> Live-install if the room's ready; otherwise show the command and the first-run screen. (Exact command on the slide at build time.)

## Slide — First run
**On slide:**
- `claude` inside any project folder → it reads that folder.
- Pick a model; you're in.

**Notes:**
> It sees the folder you start it in. That's the mental model for "what can it touch."

# Module 4 — The terminal & your editor
_~20 min_

## Slide — The terminal, demystified
**On slide:**
- It's just a text way to run programs — `claude` is one of them.
- You don't need to be a "terminal person"; you need ~5 commands.

**Notes:**
> Lower the intimidation. Most faculty fear the terminal; it's just a launcher.

## Slide — VS Code is your cockpit
**On slide:**
- Open a folder → **see your files** and exactly what Claude can access.
- Built-in terminal at the bottom; run `claude` there.
- Edits appear as **diffs** you accept or reject.

**Visual:** `../assets/vscode-cockpit.svg` — VS Code: file tree left, integrated terminal bottom running `claude`, a diff open.

**Notes:**
> The recommended starting point. The win is visibility: you watch the agent, file by file.

## Slide — Multiplexing (optional power)
**On slide:**
- tmux / zellij: many panes; long jobs that survive disconnects.
- cmux: tabbed setup with a browser — nice once you multitask.

**Notes:**
> Mark as optional/advanced. Don't scare beginners; flag it for the keen.

## Slide — Linux, not macOS
**On slide:**
- A set-it-up-yourself experience, not a polished app.
- A little configuration up front → large, durable leverage.

**Notes:**
> Malek's framing. Set the expectation honestly so people invest the 30 minutes.

# Module 5 — Claude Code at Columbia
_~10 min_

## Slide — Access & pricing
**On slide:**
- How to get Claude Code through Columbia (account / credits).
- What's covered vs a personal API key.

**Notes:**
> Fill exact Columbia access details at build time. Flag that costs are usage-based; `/cost` shows spend.

## Slide — Privacy & your data
**On slide:**
- What leaves your machine vs stays local.
- Sensitive / IRB data: know the boundary **before** pointing an agent at it.

**Notes:**
> Be concrete and cautious — faculty data is often sensitive. Give a clear rule of thumb and where to check policy.

# Module 6 — Driving Claude Code
_~20 min_

## Slide — Permission modes
**On slide:**
- **Plan** (think first, no edits) · **Accept edits** · **Auto** (runs tools itself) · **Skip permissions** ("YOLO" — careful).
- Start in Plan; graduate to Auto as you trust it.

**Notes:**
> The steering wheel. Match mode to risk. YOLO only in throwaway / sandboxed contexts.

## Slide — The context window & /compact
**On slide:**
- Finite memory; long sessions degrade.
- `/compact` summarizes; `/clear` resets. Keep sessions focused.

**Notes:**
> Explain why long chats get worse, and that managing context is a skill (more in Session 2).

## Slide — Slash commands you'll actually use
**On slide:**
- `/init` · `/clear` · `/compact` · `/resume` · `/cost`.

**Notes:**
> Keep to the few they'll use day one. `/cost` reassures the budget-conscious.

## Slide — CLAUDE.md is project memory
**On slide:**
- A file in your repo the agent reads every time — conventions, data locations, gotchas.
- `/init` drafts one; you refine it.

**Notes:**
> The "give your RA a memory" point from Module 0, paid off. Show a tiny example.

# Module 7 — Demo: chatbot vs Claude Code
_~15 min_

## Slide — The task
**On slide:**
- Treasury International Capital (TIC) data: pull it, clean it, plot a series.
- Same task, two ways.

**Notes:**
> Quick, real, finance-flavored, everyone can follow.

## Slide — In the chatbot
**On slide:**
- Paste data in, copy code out, run it yourself, paste errors back. Repeat.
- Friction scales with data size; big files don't fit.

**Notes:**
> Make the friction visible. The "before."

## Slide — In Claude Code
**On slide:**
- "Here's the folder" → it downloads, cleans, plots, fixes its own errors.
- You watch and verify.

**Notes:**
> The "after." Same result, a fraction of the friction. Land the contrast hard.

# Module 8 — Version control with git
_~20 min_

## Slide — Why git (especially now)
**On slide:**
- An agent edits many files fast. Git is your **undo** and your **record**.
- Without it, a bad run can quietly clobber work.

**Notes:**
> Frame git not as engineering ceremony but as a safety net for working with an agent.

## Slide — The minimal workflow
**On slide:**
- `git init` · `git add` · `git commit` · `git branch` · `git diff`.
- Commit before you let the agent loose; commit again when it's good.

**Notes:**
> Five commands. Claude can run them for you. Show, don't lecture.

## Slide — When Claude breaks something
**On slide:**
- `git diff` to see what changed; `git restore` / revert to undo.
- A clean commit means you can always get back.

**Notes:**
> The payoff for the verification theme. Demonstrate breaking something, then reverting.

# Module 9 — Assignments
_~5 min_

## Slide — Your assignments
**On slide:**
- **Redo:** take one finished project — how could it have been faster / better with an agent?
- **Dream:** brainstorm a project that was impossible before AI.
- **Bring data:** come to Session 2 with your own data to analyze.

**Notes:**
> These prime Session 2. Encourage real (non-sensitive) data; a fallback sample will be provided.
