---
module: Why this matters
session: 1
order: 0
duration_min: 10
template: ../../templates/cbs-template.pptx
learning_goals:
  - See concretely what an agentic AI does for research that chat cannot
  - Calibrate expectations with the "research assistant" analogy — and its limits
---

# Slide 1 — Why this matters
<!-- layout: Section Header -->

**On slide:**
- AI you can *talk to* is old news. **AI that works inside your project** is the shift.
- Today's goal: Claude Code running inside your actual research workflow.

**Notes:**
> Open with the gap: everyone has used a chatbot; almost no one has handed an agent their real project folder. That leap is what today is about.

---

# Slide 2 — The promise: an agent in your repo
<!-- layout: Title and Content -->

**On slide:**
- Reads your files, runs your code (R / Stata / Python), edits in place, iterates.
- Works on data too big to paste — a 100 GB parquet is just a file it can query.
- Long-running tasks: clean, merge, plot, draft — while you supervise.

**Visual:** `../assets/agent-in-repo.svg` — (to build) a project folder with Claude reading/writing files beside a terminal running code. Century Gothic; accent `#0081CC`.

**Notes:**
> Keep it concrete and research-flavored. The point isn't "AI is powerful" — it's "the agent operates on YOUR files and data, not a copy you pasted into a box."

---

# Slide 3 — The "RA" analogy (and where it breaks)
<!-- layout: Comparison -->

**On slide:**
- **Like a research assistant:** give it context, it does the legwork, you review.
- **Unlike an RA:** instant and tireless; *no memory* between sessions unless you give it one (`CLAUDE.md`); and it will confidently make things up — so **you verify**.

**Notes:**
> The RA analogy lands with faculty, but set the boundary: an RA remembers last week; the agent doesn't unless you persist context. An RA says "I'm not sure"; the agent often won't. Verification is your job — which is why we teach git early.
