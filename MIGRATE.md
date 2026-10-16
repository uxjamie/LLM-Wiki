# MIGRATE.md: bring an existing brain up to this template

**If you're a person reading this:** this guide is for a brain you already have. You built a wiki from Karpathy's idea file, or set up something similar with your AI, and now you want the structure, checks, and updates this template adds without starting over. You don't follow these steps yourself. Your AI does, and it asks you before changing anything.

1. **Leave this template out of your brain.** Don't copy these files into your brain's folder. Your AI reads them from GitHub (or from a separate downloaded copy).
2. **Open your existing brain's folder in your AI tool,** the same way you normally work with it.
3. **Type:**

   > Follow the migration guide at https://github.com/uxjamie/LLM-Wiki/blob/main/MIGRATE.md

   If your AI can't reach GitHub, download this template, unzip it somewhere outside your brain, and give your AI the path to that folder instead.

Your AI looks through your brain first and changes nothing. Then it shows you one plan that keeps your own way of doing things wherever it works, and asks only about the places that differ. It makes a full backup copy, then applies the changes in three steps you approve. Your pages, sources, and decisions stay. Plan on 30 to 60 minutes, depending on the size of your brain.

**Everything below is written for the AI.**

---

## What you are doing

You are moving an existing, working knowledge base onto the LLM Wiki template so it gains the template's structure, checks, and update path. The brain already holds the owner's pages, sources, conventions, and decisions. **Nothing of theirs may be lost, or rewritten without their say.** This is a renovation, not a rebuild.

Ground rules for the whole move:

- **Survey and plan before you change anything.** Until the owner approves the plan, the only files you write are your own notes in `outputs/_migration/`.
- **The owner's way wins a tie.** Where the brain already does something its own way and the template differs, keep theirs unless they choose otherwise. Never overwrite one of their rules, decisions, or tools to match the template.
- **Back up before the first change** (step 3). No exceptions.
- **Sources stay as they are.** Never edit the contents of a file in the sources folder. Renaming the folder itself is fine once approved.
- **Finished outputs and history stay as they are.** Don't edit files in `outputs/` or past log entries, even when they mention old folder names.
- **Never delete.** Where something must go, move it to `outputs/_migration/retired/` and say so.
- **Dates mean real work.** Never change a page's `date_updated` for a path fix or a frontmatter-only edit. Those dates show which pages have stalled.
- **Plain language with the owner.** They may not know words like frontmatter, domain, or plugin. Explain each choice in one everyday sentence and show examples.

## Getting the template's files

You need the template's files to copy from. Use whichever works:

- **From GitHub:** each file is at `https://raw.githubusercontent.com/uxjamie/LLM-Wiki/main/<path>`, for example `.../main/BRAIN.md` or `.../main/skills/lint/tools/vault_check.py`. The full list is on the repository page.
- **From a downloaded copy:** the owner gives you the folder path. Read from it. Never write into it.

You will need: `BRAIN.md` (the rules template), `CLAUDE.md`, `AGENTS.md`, `CHANGELOG.md`, `skills/` (the three skills and `skills/lint/tools/`), `templates/`, `wiki/Vault Map.md`, `wiki/open-items.md`, and, only if they apply, `wiki/queries.md`, `.obsidian/`, and `scripts/git-sync.sh`.

Skip `SETUP.md`. It's for brand-new brains.

---

## Step 1. Survey (no changes)

Look through the brain and write what you find to `outputs/_migration/YYYY-MM-DD-survey.md`.

1. **Folders by role.** Which folder holds the original sources, which holds the pages the AI writes, which holds finished outputs. Their current names. Any other folders (extras).
2. **Instructions.** Every file that tells the AI how the brain works: `CLAUDE.md`, `AGENTS.md`, a separate rules file, others. Whether behavior and tool details are mixed in one file.
3. **Pages.** How many. Whether they start with frontmatter (the details block between `---` lines at the top), which fields appear, how consistently.
4. **Names and tags.** How pages are named (prefixes, separators such as ` — ` or ` - `), the tags in use, most common first, and pages with no prefix.
5. **System pages.** An index (list of every page)? A log of changes? A list of decisions or open work? A map of how the brain is organized? A skill registry? Their names, even when they differ from the template's, and how the index is sectioned.
6. **Trust habits.** Do pages cite sources, label confidence, record disagreements? Is any material marked confidential?
7. **Templates, skills, and tools.** Page templates. Written procedures (skills) and where they live: in the folder, installed in an AI app, or both (for example a folder copy packaged into an installed plugin). Whether installed copies mention folder names. Scripts, including helper code inside skill folders. Whether it's a git repository or an Obsidian vault.
8. **Collisions.** Every file the template would add that the brain already has, under the same name or for the same job: a health-check script, a sync script, templates, the index, the map, open items, queries.
9. **Size of a rename.** For each folder that might be renamed, the files that mention its name, grouped: instructions and rules, skills and helper code, settings, pages, templates, and, to be left alone, outputs, log entries, and sources.
10. **Baseline check.** If the brain has its own health-check script, run it and save the output. Then run the template's checker on the brain as it is now, pointing it at the current pages folder and rules file:

    ```
    python3 -B <template>/skills/lint/tools/vault_check.py --vault . --wiki <pages folder> --rules <rules file>
    ```

    Save both outputs to `outputs/_migration/`. They are the "before" picture for step 5. Many findings here only reflect the template's stricter rules. That's expected.

Keep the survey factual. Don't propose changes yet.

## Step 2. One plan, with the owner's way as the default

Write the plan to `outputs/_migration/YYYY-MM-DD-plan.md` and show it as a side-by-side: what the brain has now, what it will have, and what changes. **Default every choice to what the brain already does,** and ask only where the brain differs from the template or a choice is needed. Give your recommendation and one plain reason for each question.

The plan covers:

1. **Name.** Usually the brain's current name.
2. **Folder names.** "The template calls the sources folder `raw` and the pages folder `wiki`. Rename yours to match? Recommended: yes. The built-in checker and future template updates expect those names." Give the counts from step 1.
3. **Groups (domains).** Propose a domain table from the brain's existing tags, with a one-line definition for each, written to match how the owner actually uses it. **Point out where their use differs from the template's guidance,** for example `personal` used for things the owner knows rather than pages about the owner, or the brain's own subject used as a group. Ask whether to keep their use or adopt the template's, and write the definition to match the answer. Keep `system`.
4. **Index sections.** The template's index has one section per domain. If the owner's index is sectioned differently (for example a Portfolio or Library section that isn't a domain), ask whether to regroup it, or keep their sections and declare each one a domain.
5. **Status and sharing levels.** Keep the brain's own values as the declared lists unless the owner wants the template's.
6. **New rules, each opt-in.** List each rule the template would add that the brain doesn't have, each as its own yes or no. Typical ones: a note of misheard names beside each transcript in the sources folder, a confidentiality section (ask whether any material belongs to an employer or client), the template's output file naming, web research habits, git habits, and template updates. Add only the yeses.
7. **Skills.** If the brain has its own procedures, offer:
   - **Folder** (recommended): the procedures live as files in `skills/`. Where the template has a skill for the same job, keep the owner's version unless they choose otherwise.
   - **Folder with an installed copy:** the folder is the source, and a copy is installed in an AI app so it triggers on its own (often a packaged plugin). After the move, the installed copy must be rebuilt and reinstalled, because until then it still mentions the old folder names.
   - **Installed only:** the skills stay installed in an AI app. Future template changes to a skill arrive as files the owner installs by hand.
8. **Collisions.** For each collision from step 1, propose keeping the brain's file. In particular:
   - **The brain's own health-check script:** keep both. Its checks often come from lessons this brain learned, so none of them should stop running. The template's checker goes in as `skills/lint/tools/vault_check.py`, and the brain's script moves to `skills/lint/tools/extra_checks.py` (its tests, if any, to `test_extra_checks.py`). Lint runs both, and template updates replace `vault_check.py` but never touch `extra_checks.py`. List the checks the two scripts share, and offer to remove those from `extra_checks.py` so findings aren't reported twice. Trim only on a yes, and keep the full original in `outputs/_migration/retired/`.
   - **A sync script, templates, a map, an index, open items:** keep the brain's and merge in what's missing.
   - **A skill registry page:** keep it. The skill table added to `CLAUDE.md` then lists triggers only and points to the registry.
9. **Extras.** Keep every extra folder and file where it is. Pages that work like system pages (an old log archive, a registry) get `system` as their first tag, so the checker treats them as system pages.
10. **Instructions file.** If one file mixes behavior and tool details, propose splitting it: behavior moves into the rules file, and tool details stay in `CLAUDE.md`. Keep one file if the owner prefers.
11. **Obsidian and git.** Keep as they are.

Wait for a yes. Revise and show it again if the owner changes anything substantial.

## Step 3. Back up everything

Prefer a backup **outside** the brain: a sibling folder such as `<brain name>-backup-YYYY-MM-DD`, if your tool can write there. Otherwise, copy into `outputs/_snapshots/YYYY-MM-DD-before-migration/` and:

- leave the snapshot folder itself out of the copy
- if the brain uses git, add the snapshot folder to `.gitignore`
- if it uses Obsidian, add the snapshot folder to Obsidian's excluded files, so its duplicate pages stay out of search and the graph, and link updates never reach them

Check that the copy has the same number of files as the original. If the brain uses git and has no uncommitted changes, ask whether the owner would like a commit before you start. Commit only on a yes.

Tell the owner where the backup is, and that undoing the move means copying it back.

## Step 4. Apply, in three checkpoints

Report at the end of each checkpoint and wait for a yes before the next.

### Checkpoint A: folders

1. Rename the sources folder to `raw/` and the pages folder to `wiki/` (if approved).
2. Update references to the old names in: the instructions and rules files, the README, skills, **helper code inside skill folders** (a hardcoded path there breaks silently), other scripts, templates, Obsidian settings, dashboard queries, and pages.
3. Leave alone: `outputs/`, past log entries, and files in the sources folder.
4. **Read each match before replacing it.** Some mentions aren't this brain's paths: a note about another brain, a quotation, an example. Replace only real references to this brain's folders.
5. Wikilinks like `[[Page]]` don't contain folder names and need no change. Fix any path-style links (`[[old-folder/Page]]`).
6. Report the counts by group, and anything you deliberately left unchanged.

### Checkpoint B: rules, adapters, and system pages

1. **Rules file.** Keep its name, or create one named after the brain if there is none. At the top, add the template's frontmatter: `llm-wiki: rules`, `brain`, `owner`, `template: https://github.com/uxjamie/LLM-Wiki`, `template_version` (the newest version in the template's `CHANGELOG.md`), `skills: folder` or `skills: installed`, and `created` (the brain's start date, if known). Add the Domains, Statuses, and Audiences tables, each value in backticks in the first column, because the checker reads them. Add only the new rules the owner said yes to. **Merge, don't replace:** where the brain has a section on the same subject, keep theirs and add only what's missing.
2. **Adapters.** Make `CLAUDE.md` point to the rules file and hold tool details, using the template's `CLAUDE.md` as the pattern. Add the "When to use each skill" table, with triggers only if the brain has a skill registry. Add `AGENTS.md` the same way. If behavior moves out of `CLAUDE.md`, show the owner what moved.
3. **System pages.**
   - **Index:** apply the approved sections. Keep every existing entry.
   - **Log:** keep it. Add an entry for this move at the end.
   - **Open items:** keep the brain's equivalent if it has one. Otherwise create `open-items.md` from the template. Decisions go newest first.
   - **Vault Map:** if the brain has one, merge into it: align its domain table, give hubs their own heading, and add any prefixes in use that it misses. Otherwise create it from the survey: the domains, the prefixes under each (in backticks, with `<...>` for the variable part), the page-type table (every template must appear), and the hub pages, counted by distinct pages linking in. **Pages the owner keeps without a prefix on purpose** go in a Vault Map table by their exact name, in backticks.
   - **Queries:** keep the brain's own. Add the template's only if the owner uses Obsidian with Dataview and has none.

### Checkpoint C: pages, templates, skills, and the checker

1. **Page details.** Content pages need `title`, `tags`, `status`, `audience`, `people`, `project`, `date_created`, `date_updated`, and `sources`. System pages need `title`, `tags`, `status`, `audience`, and `date_updated`. Add only missing fields, using the approved mapping, with the domain first in `tags`. Never change a page's body, and don't change `date_updated` for this. If more than 10 pages change, show the owner a sample of three first.
2. **Names.** Apply only page renames the owner approved, updating every link to each.
3. **Templates.** Keep the brain's. Add the template's only for domains that have none.
4. **Skills.** As approved in step 2:
   - **Folder:** copy only the template skills the brain lacks, and fill in the brain's name.
   - **Folder with an installed copy:** as with folder, then tell the owner the installed copy needs rebuilding and reinstalling now, because it still mentions the old folder names.
   - **Installed only:** write merged versions to `outputs/skill-updates/<name>/SKILL.md` for the owner to install.
5. **Checker and scripts.** If the brain had its own health-check script, move it to `skills/lint/tools/extra_checks.py` first (and its tests to `test_extra_checks.py`), fix any old folder names inside it, and run it once to confirm it still works from its new place. Then copy `vault_check.py` and `test_vault_check.py` from the template's `skills/lint/tools/`. Apply any trimming the owner approved. Keep the brain's other scripts, and add the template's `scripts/git-sync.sh` only if the brain has no sync script and needs one. Copy the template's `CHANGELOG.md` to the brain's root.
6. **README.** Leave the owner's README as it is, apart from the folder-name fixes in checkpoint A. Offer to add a short "Everyday use" section.

## Step 5. Check

From the brain's root, run:

```
python3 -B skills/lint/tools/vault_check.py
```

If `skills/lint/tools/extra_checks.py` exists, run it too. Compare with the baseline from step 1 and sort the findings into three groups:

- **Caused by the move:** a path still pointing to an old folder name, a missing table, an index entry left behind. Fix these now and run the check again.
- **Already there before:** findings that also appear in the baseline, such as stalled drafts, old orphan pages, and broken links that predate the move. Don't fix them now.
- **New checks:** things the brain never checked before, such as content pages with no prefix, or hubs the map doesn't list. These are questions for the owner, not errors.

Write the second and third groups to `outputs/_migration/YYYY-MM-DD-findings.md`, and add one line to open items suggesting a lint pass to work through them. If the checker can't run, do the same checks by reading, and tell the owner.

## Step 6. Wrap up

1. Log the move: `## [YYYY-MM-DD] update | Moved onto the LLM Wiki template v<version>`, with what changed and where the backup is.
2. Record each decision from step 2 in the decisions log, newest first, with today's date.
3. Tell the owner, in plain words:
   - what changed, and that their pages, sources, and decisions are all still there
   - where the backup is, and that it can be removed once they're happy
   - what the checker found, in the three groups, and that their own checks still run beside it
   - that "check for template updates" now works
   - any installed skills to rebuild or replace, and where the files are

The backup, survey, plan, baseline, and findings stay until the owner decides to remove them.
