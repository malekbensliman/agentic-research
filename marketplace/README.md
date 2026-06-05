# marketplace/

The **CBS Claude Code marketplace** — a small collection of plugins useful for research workflows that faculty install once and reuse.

A marketplace is just a directory with a manifest plus plugin folders; it does **not** require its own repository (it can be a subdirectory like this one, a local path, or a GitHub repo). Faculty add it with `/plugin marketplace add <path-or-repo>`, then install individual plugins.

- `plugins/` — one folder per plugin (added as we build them).
- Manifest — defines the marketplace and lists its plugins (added next, once the exact path is confirmed against current docs).

Candidate plugins (from planning): a Research Grid / SSH helper, a journal-figure formatter, a replication-package checker, and Stata / R / Python language-parity helpers.
