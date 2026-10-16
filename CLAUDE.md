# CLAUDE.md: adapter for Claude

<!-- SETUP: Delete this paragraph during setup. -->
**If `SETUP.md` is in this folder, setup has not run yet.** Read `SETUP.md` and offer to run it before anything else. Until then the rules file is `BRAIN.md`.

**Read `{{RULES_FILE}}` first, at the start of every session.** It holds every behavioral rule for the {{BRAIN_NAME}} brain. This file holds only the mechanics of running it in Claude: the Claude desktop app working in this folder, or Claude Code started in it. If a rule appears both here and in `{{RULES_FILE}}`, that is drift: keep it in `{{RULES_FILE}}` and remove it here.

---

## Session bootstrap

1. Read `{{RULES_FILE}}`.
2. Follow its session protocol: the last 10 entries of `wiki/log.md`, then `wiki/index.md` and `wiki/open-items.md`.
3. If this folder is not available in the session, say so and stop before writing anything. Never recreate brain files somewhere else.

## When to use each skill

The brain's skills are step-by-step instructions kept in this folder, in `skills/`. Nothing needs installing. When one of the situations below comes up, read that skill's file and follow it from start to finish.

| Skill | Use it when | Read |
|---|---|---|
| ingest | A new source arrives: a file lands in `raw/`, {{OWNER_FIRST}} pastes text or a link, shares a thought worth keeping, or says "ingest this", "file this", "save this", "add this to the brain". Use it even when the word "ingest" is never said. | `skills/ingest/SKILL.md` |
| lint | {{OWNER_FIRST}} says "lint", "health check", "what's stale", "what's missing", "what should I look at", or about 20 sources have been ingested since the last lint. | `skills/lint/SKILL.md` |
| courier | {{OWNER_FIRST}} says "share this", "make this shareable", "sanitize this", or wants to give a page to someone who doesn't have the brain. | `skills/courier/SKILL.md` |

If a copy of one of these skills is also installed in the app, follow the copy in this folder. When a skill is added to `skills/`, add a row here and in `AGENTS.md`.

## Helper scripts

Run Python helpers with `python3 -B` so no `__pycache__` folder is written. Some connected folders refuse deletes, and a cache folder written there can't be cleaned up from a session.

## Deletes and renames

Some connected folders refuse deletes or renames. If one fails, don't work around it. Tell {{OWNER_FIRST}} what you were trying to do and ask. When a file has to go and deleting is not possible, move it into a `_to_delete` folder inside `outputs/` and say so.

Before any large reorganization, copy the affected files into a dated `_snapshots` folder inside `outputs/` first, unless git is in use and the changes are committed.

<!-- SETUP: Keep this section if the owner uses git. Otherwise delete it. -->
## Git

The rule (owner-triggered only, never force-push) is in `{{RULES_FILE}}`. This is the how.

**When git runs directly in this folder**, sync with ordinary commands on {{OWNER_FIRST}}'s trigger:

```
git add -A
git commit -m "<action>: <description>"
git push
```

**When the folder is mounted into a sandbox that refuses deletes** (some Claude desktop setups do this), git fails, because it creates and removes lock files on nearly every write. Commits either fail (`cannot lock ref`) or leave a stale lock that breaks the next one. Use the script instead:

```
bash scripts/git-sync.sh "<action>: <description>"
```

It copies `.git` to a fresh temporary folder outside the mount, reconciles with the remote, commits there with this folder as the work tree, pushes as a fast-forward, and cleans up. The mounted `.git` is never written.

When you use the script, **never read git status or history from the mounted `.git`.** It stays frozen at the last commit made outside the sandbox, so `git status` and `git log` there are misleading, not merely stale. To see the real state, query the remote (`git ls-remote origin main`). `wiki/log.md` is the reliable record of what has changed since the last sync.

If the script prints `PUSH REJECTED`, the remote moved during the sync. Re-run it. Nothing is forced.

Never print a token. If the remote URL holds one, mask any command output that might echo it.

## Web and connected tools

Use whatever web search, fetch, and connectors this Claude workspace provides. Anything fetched is a source: save the useful part to `raw/` with its URL before distilling it.

## Viewer

Plain markdown. Obsidian is optional and recommended (see `README.md`). Nothing depends on it.
