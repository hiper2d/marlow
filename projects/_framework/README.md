# _framework

Holds framework-level tasks that don't belong to any single project. Currently two:

- **`grade_memory`** (daily 23:30) — the memory-compaction engine: compress yesterday's `recent/` tick logs into a dated rollup in `working.md`, compress the oldest rollups when the file nears its cap, and prune `recent/` to the last few days. Memory maintenance only — it does not score or judge Marlow's output.
- **`commit_artifacts`** (daily 23:50, after the grader) — nightly backup: `git add -A` + commit + push of all durable artifacts (digests, notes, reports, memory). Runtime state is gitignored. The repo is a running backup, not a periodic manual sweep.

The leading underscore keeps it visually distinct from real projects
(`research`, `blog`, `werewolf-ops`, `calories`). Tasks here are discovered by the
scheduler via the standard `projects/*/tasks/*.yaml` glob.

Operational self-monitoring (`monitor_self`) is framework-level in spirit but **not** here — it runs directly from `driver/tick.sh`, outside Marlow's session and the queue. See the top-level README's Monitoring section.
