---
title: The Modern Researcher's Tech Stack
subtitle: Using AI agents for academic research
template: ../templates/cbs-template.pptx
font: Century Gothic
sessions: 2
---

<!-- WORKSHOP MASTER DECK: rebuilt from slides/draftv0.pptx (Malek's edited deck) as the baseline.
     Structure: `#` = Session (divider), `##` = Module (section header), `### Slide` = slide.
     Each slide: On slide / Visual / Notes. Fonts + palette: ../templates/cbs-style.md
     (Century Gothic, #0081CC). Image paths are relative to this file (assets/...).
     TODO bullets are intentional: they mark Malek's open items, kept visible for editing.
     The only em-dashes in this file are the two DSL delimiters the preprocessor needs:
     "### Slide — Title" and "**Visual:** path — description". Both are stripped or converted
     at render time, so no em-dash appears on a slide. Keep prose em-dash free. -->

# Session 1: Integrating AI tools into the research workflow

## Module 1: Four ways to work with Claude
_~20 min_

### Slide — At a glance
**On slide:**
- Today's goal: Claude Code (or Codex) running inside your actual research workflow.
  - Reads your files, runs your code (R / Stata / Python), edits documents, iterates.
  - Works on data too big to paste.
  - Handles long-running tasks while you supervise.
- Think of it as a research assistant?
  - Yes: give it context, it does the legwork, you review.
  - No: instant, tireless, and it will confidently make things up.

**Visual:** `assets/agent-in-repo.svg` — project folder + Claude reading/writing files beside a terminal running code.

### Slide — Four ways to work with Claude
**On slide:**
- Claude can be used through four different media:
  - Chat: all-purpose usage, mostly non-agentic.
  - Cowork: productivity (for example emails, calendars).
  - VS Code extension: a chatbot that lives next to your code and data.
    - Exactly the same as using Antigravity.
  - Terminal / CLI: similar to the extension, but can be heavily customized.

**Visual:** `assets/four-modes-spectrum.svg` — horizontal spectrum, four modes over a grey→blue gradient (`#9E9A92` → `#0081CC`); left "you bring the context", right "full system access"; pill "We spend our time on VS Code + Terminal". [Approved 2026-06-05.]

### Slide — What makes it agentic?
**On slide:**
- AI agent: a program that autonomously performs tasks on behalf of a user or another system by designing its workflow and using available tools.
- What does an agent need:
  - Interface: programmatic access at scale, the API.
  - Action layer: how the agent acts on the world, tool use (for example MCP).
  - Competence layer: what the agent is good at, skills and prompting.
- In other words: all AI agents start with the same LLM.
  - MCP gives the agent reach; skills give it expertise.
  - The difference is what it sees and how much it can do on its own.
- Key: how to manage context efficiently.

### Slide — Putting it together
**On slide:**
- **TODO: update this slide.**
- Each piece is a separate account you sign up for. Plug them together and you have the app.
- GitHub (the recipe): you get a copy of the code. Fork the repo; you now own a copy you can deploy and update later.
- Pinecone (the memory): you get a vector database. Create one index; this is where your uploaded documents will live.
- OpenAI (the brain): you get an API key. It reads your documents, embeds them, and answers your questions.
- Vercel (the host): you get a live URL. Connect your fork, paste the API keys as env vars, and click deploy.

### Slide — Today's focus
**On slide:**
- Difficulty: this is a Linux-style experience, rather than Windows or macOS.
  - You need to invest time to set up and customize it for your own workflow.
  - The ecosystem evolves fast, so we are all a bit ahead and a bit behind everyone else at the same time.
- Disclaimer: our approaches work for us but might not be optimal for you.
- Focus on:
  - VS Code: an interface to visualize your files (and interact with Claude).
  - Terminal: the most customizable way to interact with Claude.
    - Some of the content also applies to the extension: we will set up both and you will decide.
  - Git: a tool to help us guarantee a source of truth.
  - Claude.

**Notes:**
> Go fast past Chat and Cowork, then spend real time in VS Code and the terminal.

## Module 2: The terminal
_~12 min_

### Slide — The terminal: your computer's full control interface
**On slide:**
- An interface that lets you perform any operation on your computer.
  - To open a file you can double-click it, or type `open filename`.
  - From the terminal you can edit files, run programs (R / Stata / Python), install software, download data, hit the network.
- Quick aside: a coding agent = an LLM + a terminal.
  - Take an LLM: you can prompt it to generate terminal commands.
  - Make sure the commands are actually run in a terminal.
  - The result: an LLM that can interact with your computer.
  - Rinse and repeat: the LLM uses the terminal to create a file, read it, add or modify text, read it again.
  - That feedback loop is what lets an LLM become agentic.

**Visual:** `assets/llm-plus-terminal.svg` — LLM box + terminal box → "agent", with a loop arrow (act, read output, act).

**Notes:**
> Live demo: run a few commands. `ls`, a one-line R / Python snippet, `curl` a file.

### Slide — Playing with the terminal
**On slide:**
- **TODO: add a small activity so everyone knows how to open their terminal.**
  - Provide different instructions for Windows / Linux / macOS.
- Goal: demystify the terminal.

## Module 3: Setup, your editor, and your first session
_~30 min_

### Slide — The terminal, demystified
**On slide:**
- You do not need to be a "terminal person."
- The terminal can do anything, but you will likely need only about five commands.
  - **TODO: list the five commands and add them to the one-pager.**

**Notes:**
> Lower the intimidation: it is just a launcher.

### Slide — VS Code is your cockpit
**On slide:**
- VS Code is a powerful code editor.
  - One place to modify code in any language. **TODO: maybe add more detail here.**
- Open a folder to see your files and exactly what Claude will be able to access.
- Built-in terminal at the bottom; run `claude` there.
  - Edits appear as diffs you accept or reject.
  - **TODO: maybe move the terminal and diff bullets to a later slide.**
- Do you absolutely need VS Code? No. Some people work only with a terminal.
- **TODO: maybe add the difference between the VS Code terminal and the computer terminal.**

**Visual:** `assets/vscode-cockpit.svg` — VS Code: file tree left, integrated terminal bottom running `claude`, a diff open.

**Notes:**
> The recommended starting point. The win is visibility: you watch the agent, file by file.

### Slide — What you need first
**On slide:**
- A terminal + Homebrew (the macOS package manager).
- Your research runtimes: Python, R, Stata, whatever you use.

### Slide — Install Claude Code
**On slide:**
- One installer makes `claude` available in your terminal.
- `claude` to start; `/login` to authenticate.

### Slide — First run
**On slide:**
- `claude` inside any project folder makes it read that folder.
- Pick a model; you are in.

### Slide — Your first session: an existing project
**On slide:**
- Open the folder in VS Code, use the bottom terminal, and enter `claude`.
- **TODO: confirm whether to use `/review`, `/claude-automation-recommender`, or `/init`.**
- Ask "summarize this project," then run `/review` to get a code review of it.
- Read-only by default: nothing changes without your say-so.

**Visual:** (hands-on) — open a real project and run `/review`.

### Slide — Starting a new project
**On slide:**
- From nothing: `mkdir my-paper && cd my-paper`, then `claude`.
- `/init` writes a `CLAUDE.md`; describe your goal in Plan mode; let it scaffold the structure and first code.
- **TODO: same as above, but with the VS Code variant.**

## Module 4: Claude Code at Columbia
_~10 min_

### Slide — Access and pricing
**On slide:**
- How to get Claude Code through Columbia (account / credits).
- What is covered versus a personal API key.

**Notes:**
> Fill exact Columbia details at build time. `/cost` shows spend.

### Slide — Privacy and your data
**On slide:**
- What leaves your machine versus what stays local.
- Sensitive / IRB data: know the boundary before pointing an agent at it.

## Module 5: Driving Claude Code
_~25 min_

### Slide — Permission modes
**On slide:**
- Plan (think first, no edits), Accept edits, Auto (runs tools itself), Skip permissions ("YOLO", careful).
- Start in Plan; graduate to Auto as you trust it.

### Slide — Working with an agent is managing context
**On slide:**
- The agent only knows what is in its context window: your files, what you have said, what it has read.
- Most "it got worse / went off track" moments are really context problems.
- Your job shifts from writing code to curating what the agent can see: right things in, noise out.

### Slide — The context window and /compact
**On slide:**
- The window is finite; as it fills, early details fade and quality drops.
- `/compact` summarizes the conversation so far into a shorter form: frees space while keeping the gist, so a long session does not degrade or hit the limit.
- `/clear` wipes and starts fresh when you switch tasks.
- **TODO: explain what goes in the context.**

### Slide — Slash commands you'll actually use
**On slide:**
- `/init`, `/clear`, `/compact`, `/resume`, `/cost`.
- **TODO: add these to the one-pager.**

### Slide — CLAUDE.md is project memory
**On slide:**
- A file in your repo the agent reads every time: conventions, data locations, gotchas.
- `/init` drafts one; you refine it.
- **TODO: add repo-level versus user-level memory.**

### Slide — My setup (just one example)
**On slide:**
- Disclaimer: this is just my setup, optimized for me. You can get the same result with a simpler setup.
- I use Visual Studio Code.
  - I have tweaked my terminal to show a lot of info you do not need.
  - It lets me see all my code in one place.
- "Clean" code is stored in GitHub.
  - GitHub connects to Google Cloud, Firebase, Supabase, AWS, Vercel.
  - It gives version control and collaboration.
  - Use an LLM to help you set up a repo.
- I work with Claude Code as my coding agent.
  - I have also tried the Claude Code extension, Codex (OpenAI), and GitHub Copilot.

### Slide — Using an AI agent
**On slide:**
- Most of you have already used an agent, sometimes without knowing it.
  - Key concept: an LLM that can reach specialized context and tools to take actions.
  - Example: modify a PowerPoint, add a calendar event.
- Problem: each tool or skill takes up space in a limited context window.
- Solution: move from a model view to a system view.
  - No longer "let us just build the biggest, most general model."
  - Instead, context management: take an existing LLM and build infrastructure that queries and uses the right tool or skill at the right time.
  - Software engineering is evolving toward system engineering.
- The infrastructure is still developing and can be overwhelming.

### Slide — The jargon, decoded
**On slide:**
- Focus on Claude Code.
- **TODO: the original comparison table did not survive the .pptx export; rebuild it (term and definition for skill, MCP, plugin, subagent, hook, slash command).**

### Slide — When to use each
**On slide:**
- Do not pre-build a setup. The list below is not exhaustive: you can and should be creative.
- **TODO: the original table did not survive the .pptx export; rebuild it (need, then which tool to reach for).**

## Module 6: Demo, chatbot versus Claude Code
_~15 min_

### Slide — The task
**On slide:**
- Treasury International Capital (TIC) data: pull it, clean it, plot a series.
- Same task, two ways.

### Slide — In the chatbot
**On slide:**
- Paste data in, copy code out, run it yourself, paste errors back. Repeat.
- Friction scales with data size; big files do not fit.

### Slide — In Claude Code
**On slide:**
- "Here's the folder" and it downloads, cleans, plots, fixes its own errors.
- You watch and verify.

## Module 7: Version control with git
_~20 min_

### Slide — Why git (especially now)
**On slide:**
- An agent edits many files fast. Git is your undo and your record.
- Without it, a bad run can quietly clobber work.

### Slide — The minimal workflow
**On slide:**
- `git init`, `git add`, `git commit`, `git branch`, `git diff`.
- Commit before you let the agent loose; commit again when it is good.

### Slide — When Claude breaks something
**On slide:**
- `git diff` to see what changed; `git restore` or revert to undo.
- A clean commit means you can always get back.

### Slide — Power cuts both ways: verify and guardrail
**On slide:**
- Because it can do anything, it can also do the wrong thing confidently (hallucinations).
- Defenses: run the code, check outputs, commit to git so nothing is silently lost.

## Module 8: Assignments
_~5 min_

### Slide — Your assignments
**On slide:**
- Redo: take one finished project. How could it have been faster or better with an agent?
- Dream: brainstorm a project that was impossible before AI.
- Bring data: come to Session 2 with your own data to analyze.

# Session 2: AI for academic research

## Module 1: Recap and common failures
_~10 min_

### Slide — Since Session 1
**On slide:**
- What did you try? What broke?
- Quick round the room: one win, one wall.

### Slide — The usual failure modes
**On slide:**
- Lost context (a long session drifted), over-trusting unverified output, no git safety net, vague prompts.
- Each has a fix we will cover today.

## Module 2: Context management
_~15 min_

### Slide — Why long sessions degrade
**On slide:**
- The context window is finite; as it fills, early details fade and quality drops.
- "It got dumber" usually means "the window is full."

### Slide — /compact and /clear
**On slide:**
- `/compact`: summarize and keep going. `/clear`: hard reset between tasks.
- One task per session; do not let it sprawl.

### Slide — The memory hierarchy
**On slide:**
- User (`~/.claude/CLAUDE.md`): applies to every project.
- Project / repo (`./CLAUDE.md`): conventions for this repo, shared with collaborators.
- Local (`.claude/settings.local.json`): your machine only, not committed.
- Put durable facts in `CLAUDE.md` so you never re-explain.

## Module 3: Extending Claude Code (skills, MCP, plugins, hooks)
_~30 min_

### Slide — Ways to extend it
**On slide:**
- Skills, MCP, plugins, subagents, hooks, custom slash commands: bolt new capabilities onto the LLM + terminal core.

### Slide — MCP (Model Context Protocol)
**On slide:**
- A standard way to plug in tools and data: databases, APIs, services (Qualtrics, WRDS, and more).
- Install once; the agent gains a new power.

### Slide — Skills
**On slide:**
- Reusable, packaged know-how and commands.
- Example: a Stata skill to run Stata from the command line.

### Slide — Plugins and a CBS marketplace
**On slide:**
- Plugins bundle skills, MCP, and commands; install from a marketplace.
- We are building a CBS marketplace: add it once, install what you need.

### Slide — Subagents and output styles
**On slide:**
- Subagents: parallel helpers for big tasks.
- Output styles (Explanatory, Learning) tune voice, handy for academic writing.

### Slide — Git worktrees
**On slide:**
- Run several agent tasks in parallel on separate branches without collisions.

### Slide — Hooks
**On slide:**
- Run your own shell commands automatically on events: format after every edit, run tests on save, ping you when a long task finishes.
- Configured in settings; the agent triggers them, you do not.

## Module 4: Remote work
_~20 min_

### Slide — Claude where you aren't
**On slide:**
- `claude --teleport` (or `/teleport`), `/remote-control` (drive it from your phone), `claude --remote`.

### Slide — Multiplexing (optional power)
**On slide:**
- tmux / zellij: many panes; long jobs that survive disconnects.
- cmux: a tabbed setup with a browser, nice once you multitask.

**Notes:**
> Moved here from Session 1. Optional and advanced; flag it for the keen, do not scare beginners.

### Slide — The Research Grid
**On slide:**
- SSH into Columbia's compute; run long jobs.
- tmux / zellij so sessions survive disconnects.

## Module 5: Collaborative demo
_~25 min_

### Slide — Blank folder to result, live
**On slide:**
- Empty folder to a finding, using Columbia data.
- Plan: query WRDS for a country's CDS series, find dates of relevant news, visualize the risk spike.

### Slide — Demo 2, Qualtrics MCP
**On slide:**
- Pull survey data through the Qualtrics MCP; analyze in place.

## Module 6: Your project, the plan-mode way
_~25 min_

### Slide — Turn your idea into a plan
**On slide:**
- In Plan mode, write the prompt; let it draft a plan. Do not execute yet.

### Slide — Iterate the plan (get a second opinion)
**On slide:**
- Read and edit the plan by hand; ask another model (for example GPT) to critique it.

### Slide — Execute and supervise
**On slide:**
- Run in Auto (or skip-permissions in a safe sandbox); watch, verify, commit.

## Module 7: LLMs for unstructured data
_~20 min_

### Slide — Scrape to structure
**On slide:**
- Example: scrape EDGAR filings, build a parquet / SQLite with DuckDB.
- The agent writes the scraper and the queries; you do not need to know SQL.

### Slide — Where the compute and credits come from
**On slide:**
- Running inside Claude / Codex, versus OpenRouter credits, versus your own OpenAI / Anthropic API key.
- Trade-offs: convenience, cost, control.

### Slide — (Time permitting) Writing like you
**On slide:**
- Generate a style file from your past writing; draft new text in your voice.

## Module 8: Show and tell
_~20 min_

### Slide — Show your result
**On slide:**
- Quick interactive presentations: what you built, what surprised you.

## Module 9: Security and good hygiene
_~10 min_

### Slide — Working safely
**On slide:**
- Sandboxing / containers for risky runs; mind secrets and keys; use permission modes; git as undo.
- Sensitive / IRB data: keep it local; know what leaves your machine.
