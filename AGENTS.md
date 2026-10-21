# AGENTS.md: adapter for other AI tools

<!-- SETUP: Delete this paragraph during setup. -->
**If `SETUP.md` is in this folder, setup has not run yet.** Read `SETUP.md` and offer to run it before anything else. Until then the rules file is `BRAIN.md`.

**Read `{{RULES_FILE}}` first, at the start of every session.** It holds every behavioral rule for the {{BRAIN_NAME}} brain. This file is for AI tools that read `AGENTS.md` (Codex and others). Claude has its own adapter, `CLAUDE.md`. If a rule appears both here and in `{{RULES_FILE}}`, keep it in `{{RULES_FILE}}` and remove it here.

## Session bootstrap

1. Read `{{RULES_FILE}}`.
2. Follow its session protocol: the last 10 entries of `wiki/log.md`, then `wiki/index.md` and `wiki/open-items.md`.
3. If this folder is not available, say so and stop. Never recreate brain files somewhere else.

## When to use each skill

This tool may not load skills on its own. That's fine. The brain's skills are step-by-step instructions kept in this folder, in `skills/`. Nothing needs installing. When one of the situations below comes up, read that skill's file and follow it from start to finish.

| Skill | Use it when | Read |
|---|---|---|
| ingest | A new source arrives: a file lands in `raw/`, {{OWNER_FIRST}} pastes text or a link, shares a thought worth keeping, or says "ingest this", "file this", "save this", "add this to the brain". Use it even when the word "ingest" is never said. | `skills/ingest/SKILL.md` |
| lint | {{OWNER_FIRST}} says "lint", "health check", "what's stale", "what's missing", "what should I look at", about 20 sources have been ingested since the last lint, or a scheduled health check runs. | `skills/lint/SKILL.md` |
| courier | {{OWNER_FIRST}} says "share this", "make this shareable", "sanitize this", or wants to give a page to someone who doesn't have the brain. | `skills/courier/SKILL.md` |

If a copy of one of these skills is also installed in the app, follow the copy in this folder. When a skill is added to `skills/`, add a row here and in `CLAUDE.md`.

## Scheduled health check

When {{OWNER_FIRST}} wants lint to run on its own (setup or migration asks), use this tool's scheduler if it has one, with the task instructions in the lint skill's *Scheduled runs* section. Tell {{OWNER_FIRST}} what the task needs to run (the computer on, the app open, this folder available). If the tool has no scheduler, say so and suggest a repeating calendar reminder to say "lint" instead. Record the schedule in the decisions log in `wiki/open-items.md`: how often, the app that runs it, and the task's name.

## Helper scripts

Run Python helpers with `python3 -B` so no `__pycache__` folder is written into the brain.

<!-- SETUP: Keep this section if the owner uses git. Otherwise delete it. -->
## Git

If this brain uses git, sync only on {{OWNER_FIRST}}'s trigger, with ordinary `git add`, `git commit`, `git push`. The rule is in `{{RULES_FILE}}`.
