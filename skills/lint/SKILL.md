---
name: lint
description: Run a health check on the {{BRAIN_NAME}} brain. Applies only when working inside the {{BRAIN_NAME}} folder, an LLM Wiki brain. Use on "lint", "health check", "audit the brain", "what's stale", "what's missing", "what should I look at", on a schedule, or about every 20 ingests. Keeps the wiki consistent as it grows and surfaces connections the owner might miss.
---

# Lint

Trigger on "lint", "health check", "audit the brain", "what's stale", "what's missing", or a schedule.

## Guard, first, always

Confirm you are inside the {{BRAIN_NAME}} brain: the folder's root holds the rules file (the file `CLAUDE.md` and `AGENTS.md` tell you to read first), its frontmatter carries `llm-wiki: rules` and `brain: "{{BRAIN_NAME}}"`, and `wiki/index.md` exists. If not, say this skill belongs to the {{BRAIN_NAME}} brain and stop. Never create brain files in a folder that is not the brain.

## Procedure

1. **Run the mechanical check first.** From the brain's root: `python3 -B skills/lint/tools/vault_check.py`. It reports and never changes anything. It reads the domain, status, and audience tables from the rules file, and the prefixes and hubs from the Vault Map, so it follows this brain's own rules. It covers: setup leftovers, the adapters pointing at the right rules file, skill descriptions carrying the brain's name, frontmatter, filenames and separators, broken, empty, and wrong-case links, orphans, the index, stalled drafts, rules in the wrong home, root docs naming paths that don't exist, Vault Map drift, hub candidates, and an open-items file that has started to grow back (the *Archive pass* below handles it). If `skills/lint/tools/extra_checks.py` exists, run it next: `python3 -B skills/lint/tools/extra_checks.py`. It holds checks specific to this brain, often carried over from a checker the brain had before, and its findings go in the same report. Judge each finding before it goes in the report. Some are intended. If Python is not available, do the same checks by reading. Don't edit `vault_check.py` for this brain. It belongs to the template, and template updates replace it. A check this brain needs goes in `extra_checks.py`, with its tests in `test_extra_checks.py`. If the template's checker raises a false flag, say so in the report as one to send to the template's maintainer.
2. **Read `index.md`, `log.md`, and `open-items.md`**, then scan the pages for what a script can't judge:
   - **Contradictions** between pages filed at different times. Keep both sides with sources. Look again at every page already carrying a `conflicts` flag.
   - **Stale claims** a newer source has overtaken, and time-sensitive pages past their shelf life.
   - **Domain fit.** Read each page's first tag against its definition in the rules file. The usual slips: `personal` used for things the owner knows or works on rather than pages about the owner, the brain's own subject used as a domain, and tags carried over from an import.
   - **Vault Map currency.** Judge each map finding from step 1 before proposing a map change. A stray prefix is often a misnamed page, not a new page type. Read the hub candidates: add a page to the map's hub list when many distinct pages route through it, and remove a listed hub that has gone quiet. A page with no prefix is a system page, so a content page without one is a naming problem, not a hub, unless the map lists it by its exact name.
   - **Open-items drift.** Items finished in the log but never moved to the archive. Decisions made in chat that never reached the decisions log. Decisions now superseded, or folded into the rules file, an adapter or a page, still sitting in the live file. Step 1 flags checked items left behind and a file past 25 KB. Propose the moves (rules file, *Session protocol*). Never run an archive pass unasked.
   - **Missing pages.** Concepts or people mentioned across several pages without a page of their own.
   - **Root docs.** Read the rules file, `CLAUDE.md`, `AGENTS.md`, and `README.md` against the real folder: paths, the directory diagram, the skill table, and workflow notes. A root doc that contradicts the real tree misleads every later session.
   - **Rules in two homes.** Behavior belongs in the rules file. Tool mechanics belong in the adapters. Page types and prefixes belong in the Vault Map. Flag a behavioral rule copied into an adapter, a tool mechanic in the rules file, and a skill that restates a rule instead of pointing at it. A skill's numbered step gets obeyed more readily than a policy paragraph, so a restated rule that drifts does real damage.
   - **Skill links are not findings.** `[[ingest]]`, `[[lint]]`, and `[[courier]]` resolve to nothing on purpose. Never create stub pages for them.
3. **Mine connections.** This part earns the lint its slot. Look for pages that share people, projects, tags, or themes but never link. Look for idea pages whose combination suggests something nobody has asked for yet. Name three to five concrete candidates with the pages behind them. Gaps a web search could fill count too.
4. **Write the report** to `outputs/lint-YYYY-MM-DD.md`, grouped by type, most urgent first, connection candidates last.
5. **Propose fixes and wait for approval** before changing pages. Renames always wait: list each file and every page whose links will change. Trivial repairs (a missing wikilink, an index line) can go ahead if the owner has allowed it.
6. **Log it:** `## [YYYY-MM-DD] lint | summary`. If the brain uses git, end with `Not committed, awaiting the owner's trigger.`

## Scheduled runs

The owner may have set lint to run on its own (setup or migration offers it, and the decisions log in `open-items.md` records it). On a scheduled run nobody is there to approve anything, so:

1. Do steps 1 to 4 as usual: the mechanical check, the read-through, connection mining, and the report.
2. Change no pages. Step 5's trivial repairs wait too, even if the owner has allowed them in a live session.
3. Add one line to `open-items.md`: `Lint report ready: outputs/lint-YYYY-MM-DD.md, <n> findings, <n> connection leads. Review and approve fixes.` If the previous scheduled report's line is still there unreviewed, say so in the new line instead of adding a second one.
4. Log it as in step 6, adding `(scheduled)` after `lint`.
5. Never commit, never run an archive pass, never rename.

The task's own instructions name only the brain's folder and this skill, never `wiki/`, `raw/`, or other folders inside it. Folder names live here, so a later rename can't break the task.

The task's instructions, adapted to the tool that runs them:

> Open the {{BRAIN_NAME}} brain in <full path to this folder>. Read the rules file (the root file `CLAUDE.md` or `AGENTS.md` names), follow its session protocol, then run the lint skill as a scheduled run. Report only. Change no pages.

## Archive pass

Run only on the owner's yes, when step 1 reports open-items past 25 KB or the owner asks to slim it. Moving finished items the same turn (rules file, *Session protocol*) keeps the file light day to day. This pass handles live items that have grown long.

1. **Plan first.** Show the owner the method below with two worked examples, one item and one ruling, and wait for a yes.
2. **Snapshot.** Copy `wiki/open-items.md` to `outputs/_snapshots/YYYY-MM-DD-open-items.md`.
3. **Keep the history.** Copy the whole body of `wiki/open-items.md` (everything below its frontmatter), word for word, into `wiki/open-items-archive.md` under `## Open items, full text before the trim (YYYY-MM-DD)`. The whole body, not only the items, so the opening text and section notes survive too.
4. **Trim.** Rewrite each live item as one line: its status and the next action, keeping its key links, with one tag:
   - **Decide:** needs the owner's call.
   - **Track:** waiting on someone else or a date.
   - **Clear:** can close now with the owner's ruling, proposed in the item.
   - **Do:** a task the owner can just do.
5. **Rulings.** Turn each decision still in force into a one-line standing ruling, with its date, under `## Standing rulings`. A ruling already written into the rules file or a page is named in one line, not restated. Move the full decisions log to the archive, and leave an empty `## Decisions log` for new decisions.
6. **Prove it.** Run `python3 -B skills/lint/tools/archive_check.py outputs/_snapshots/YYYY-MM-DD-open-items.md`. It must report nothing lost. Then run the checker and report the new size.
7. **Log it** as `update`.

## Reminders

- Report. Don't silently rewrite.
- Lint looks back at what is broken. Connection mining looks forward at what is possible. Both belong in every pass.
- Good as a recurring scheduled task. See *Scheduled runs* above.
