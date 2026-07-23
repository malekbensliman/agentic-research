# activities/

Hands-on exercises faculty run during the workshop, plus sample repos to point Claude Code at.

## Activity 1 — Review an existing project (Session 1)
Bring a project you've already written.
1. Open the folder in VS Code (or `cd` into it) and start Claude: `claude` in the terminal.
2. Ask *"summarize this project"* — watch it read your files.
3. Run **`/review`** (or a code-review plugin from the CBS marketplace) to get feedback on the code.

Read-only and safe — nothing changes without approval. Goal: see Claude understand and critique **your** code.

## Activity 2 — Start a new project (Session 1)
From an empty folder:
1. `mkdir my-project && cd my-project` → `claude`.
2. `/init` to create a `CLAUDE.md`.
3. Describe your goal in **Plan mode**; review the plan; let it scaffold the structure + first code.

Goal: experience going from nothing to a working skeleton.

## Fallback sample project
A ready-made sample repo lives here for anyone without their own (or with IRB-sensitive) data, so everyone can do Activities 1–2.

## Activity 3 — When Words Sweat: language and loan funding (Session 2)
A ready-to-run marketing example in [`when-words-sweat/`](when-words-sweat/): 10,000 real
Prosper.com loan listings and a sequence of copy-paste prompts. Faculty drive the
**Claude Code desktop app** from a fresh `/init` through EDA, a simple model, a
richer text-based model, and a Qualtrics survey — proving their setup works while
answering a tangible question: *does the language of a loan request get it funded?*
See its `README.md` and `PROMPTS.md`.

## Bring-your-own-data (Session 2)
Faculty bring their own data / project to push toward a real result during Session 2.
