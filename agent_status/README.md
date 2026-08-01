# agent_status/

The shared status board: one JSON file per AI agent session, kept on `master`
so concurrent agents on separate branches can see each other. The file format,
naming scheme, and commit rules are in [`../AGENTS.md`](../AGENTS.md),
"`agent_status/` — the shared status board".

Stale files from finished sessions are not garbage: they are the log of who
did what. Do not delete other agents' files, and do not "tidy" the directory.
