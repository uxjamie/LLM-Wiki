# SETUP.md: turn this template into your brain

**If you're a person reading this:** you don't need to follow these steps yourself. Open this folder in an AI tool that can work with the files on your computer (the Claude desktop app working in this folder, Claude Code, Codex, or a similar tool) and type:

> Run SETUP.md

Your AI will ask you a few questions in plain language: what to call your brain, what it's for, and how you'd like pages grouped. It shows you a plan and changes nothing until you say yes. It takes about ten minutes, and you can change any answer later by telling your AI.

**Everything below is written for the AI.**

---

## What you are doing

You are turning a blank LLM Wiki template into a named, working brain for one person. You will interview them, show a plan, apply it on their yes, prove the result is clean, and retire this file.

Ground rules for the whole setup:

- **Ask, don't guess.** When an answer is unclear, ask a follow-up. A wrong guess here gets copied into every page the brain writes later.
- **One batch of questions, then a plan, then changes.** Don't change any file until the person approves the plan in step 3.
- **Plain language.** Assume the person has never used a wiki like this, never edited a configuration file, and may not know words like markdown, frontmatter, domain, git, or plugin. Explain each choice in one everyday sentence, say why it matters, and give the default. Never make them type file names or code. Show examples rather than terms.
- **Never delete a file.** Where this setup removes something, it moves it or empties it, and says so.

---

## Step 1. Check the folder

Confirm all of these before asking anything:

- **Find the rules file:** the one `.md` file at the root whose frontmatter holds `llm-wiki: rules`. In a fresh template it is `BRAIN.md`. Find it by that marker, not by name, because an interrupted setup may already have renamed it.
- **Check its `brain:` value.** If it is still `"{{BRAIN_NAME}}"`, setup has not run: carry on. If it holds a real name and the file has no `{{` placeholders left, setup has already run. Say so and stop. If it holds a real name but placeholders remain, an earlier setup stopped partway. Tell the person, read `wiki/log.md` for what was done, and finish the remaining steps instead of starting over.
- **If two root files carry the marker**, a rename went wrong. Stop and ask the person which one is current.
- `wiki/index.md`, `wiki/Vault Map.md`, and `skills/lint/tools/vault_check.py` exist.

If one of those files is missing, the download is incomplete. Tell the person to download the template again, and stop.

## Step 2. Interview

Ask these in one message (or one form, if your tool has a question widget). Give each question its default so the person can accept it quickly.

1. **Name.** "What should this brain be called? One or two words works best (Atlas, Field Notes, Lighthouse). The name shows up in the rules file name, the README, the index and log headings, and the skill descriptions."
2. **Owner.** "What's your name? Your first name is used in page names for pages about you, like `Sam — Working Style`."
3. **Purpose.** "What is this brain for? Give me two to four things you want it to hold or help with. What should stay out?"
4. **Domains.** Propose the default domains below, adjusted to their purpose, and ask them to confirm, rename, add, or drop. Explain: "Every page gets one domain as its first tag. A domain says what kind of page it is, so the list should split the brain into useful groups."
5. **Pages about you.** "Do you want pages about yourself, like how you work and write, or your background? They help the AI work the way you like. This adds a `personal` domain." Default: yes, with one starter page, `<First name> — Working Style`.
6. **Sharing.** "Will anything in here belong to your employer or a client? If so, I'll treat everything as confidential and keep it from leaking into anything you share." If yes, the Confidentiality section stays and pages can carry `confidential: employer`. Then: "Who might you share things from this brain with: no one, your team, or the public?" This sets the sharing levels. Default: `internal` (just you), `team`, `public`.
7. **Git.** "Do you want to use git? It's a tool that saves a history of every change so you can go back to an earlier version. If you haven't used it, choose no. The brain keeps its own written log of changes either way." Options: no (default), git in this folder only, or git with an online copy such as a private GitHub repository. With git, the AI only saves a version when the person asks.
8. **Obsidian.** "Will you read the brain in Obsidian? It's a free app that shows your pages with clickable links and a map of how they connect. The brain works fine without it." Default: yes.
9. **Regular health check.** "Want me to check the brain on my own every so often? I look for broken links, outdated facts, and gaps, and point out pages that should be connected. I write you a short report and change nothing until you say yes. Your computer needs to be on with this app open when it runs." Options: every two weeks (default), weekly, monthly, or no (you'll say "lint" when you want one). If the tool has no way to schedule a task, skip this question and suggest a calendar reminder at hand-over.

### Default domains

| Domain | What belongs here |
|---|---|
| `research` | Knowledge distilled from outside sources: articles, talks, papers, documents, interviews. |
| `ideas` | The owner's own thinking: theses, proposals, frameworks, opinions. |
| `people` | One page per person. |
| `projects` | Initiatives with a goal and an end: what, why, status, decisions. |
| `tools` | Methods, references, checklists, how-tos. |
| `personal` | Pages about the owner: who they are, how they work, their history. Not things they know or work on. |
| `system` | The brain's own machinery. Always kept. |

Rules to hold while tailoring the list. Explain them if the person proposes something that breaks one.

- **The brain's own subject is never a domain.** In a brain about one company, a domain with that company's name sorts nothing, because every page would carry it. It can be a second tag instead.
- **`personal` means pages about the owner.** A meeting the owner attended, or a project they lead, takes the domain of its kind.
- **Keep `system`.** The index, open-items, its archive, Vault Map, and queries use it.
- **Fewer is better.** Five to eight domains is plenty. Each one becomes an index section.
- **Define each one in a single line.** The definition is what future sessions read when a page's domain is unclear.

Examples of tailoring: a design-system brain might use `components`, `patterns`, `foundations`, `decisions`, `research`, `people`, `system`. A team-knowledge brain might use `process`, `research`, `projects`, `people`, `tools`, `system`.

## Step 3. Show the plan and wait

Derive these from the answers, then show them in one short message:

- **Brain name:** for example `Atlas`.
- **Rules file:** the name in capitals with spaces turned into hyphens, plus `.md` (`Atlas` → `ATLAS.md`, `Field Notes` → `FIELD-NOTES.md`). Offer it, and let the person pick a different file name.
- **Owner:** full name and first name.
- **Purpose:** their two to four lines, tightened.
- **Domains:** the final table with definitions.
- **Prefixes:** one page-type row per domain for the Vault Map (see step 4.6), so the person sees how pages will be named.
- **Audiences, confidentiality, git, Obsidian, health check:** their choices. The health check is scheduled last, in step 7, once the brain checks clean.
- **Files that change:** every file in step 4.

Wait for a yes. Apply any changes they ask for, and show the plan again if the changes were large.

## Step 4. Build the brain

Do these in order.

1. **Rename the rules file.** Rename `BRAIN.md` to the chosen rules file name. If renaming fails, don't work around it on your own. Tell the person and ask them to rename it themselves (give the exact new name), then continue. If they can't, write the new file with the full content, and replace everything in `BRAIN.md` with one line: `Superseded by <new name>. Safe to delete.` That removes its `llm-wiki: rules` marker, so only one rules file remains.
2. **Fill the placeholders** in every file under the root, `wiki/`, `templates/`, `skills/`, and `.obsidian/`:

   | Placeholder | Becomes |
   |---|---|
   | `{{BRAIN_NAME}}` | The brain name |
   | `{{RULES_FILE}}` | The rules file name, for example `ATLAS.md` |
   | `{{RULES_STEM}}` | The rules file name without `.md`, for example `ATLAS` |
   | `{{OWNER}}` | The owner's full name |
   | `{{OWNER_FIRST}}` | The owner's first name |
   | `{{PURPOSE}}` | The purpose, as a short bulleted list |
   | `{{CREATED}}` | Today's date, `YYYY-MM-DD` |

   Leave `README.md`, `CHANGELOG.md`, and this file for steps 4.9 and 6.
3. **Resolve every `<!-- SETUP: ... -->` comment.** Each one says what to keep or delete. Then delete the comment itself. Where they are:
   - The rules file: the note under the title (delete), the working-style paragraph, the Domains table, the Audiences table, the Confidentiality section, the Git section.
   - `CLAUDE.md` and `AGENTS.md`: the not-yet-set-up paragraph (delete), the Git section (keep only with git).
   - `wiki/index.md`: the domain sections. `wiki/Vault Map.md`: the domains table and the page-type table.
   - `.obsidian/graph.json` holds no comments (JSON can't). Step 4.10 covers it.
4. **Domains.** Write the confirmed table into the rules file's Domains section. Keep each domain in backticks in the first column (`` `research` ``). The health check reads the domains from those backticks and ignores rows without them. Use lowercase, with hyphens for multi-word domains (`design-decisions`).
5. **Index.** In `wiki/index.md`, write one `##` section per domain in the order of the Domains table, with `## System` last. Use the domain as the heading in title case (`design-decisions` → `## Design Decisions`). The System section keeps its existing entries.
6. **Vault Map.** In `wiki/Vault Map.md`:
   - In the domains table, write one row per domain with the prefixes that live under it, each in backticks with `<...>` for the variable part: `People — <name>`, `<Topic> — <subtitle> (<Author>)`. A script reads these patterns, so keep the backticks.
   - In the page-type table, keep the rows whose domain survived, adjust names to match renamed domains, and add a row for each new domain. Every template in `templates/` must appear in this table.
   - Starter prefixes for the default domains: `Ideas — <title>`, `People — <name>`, `Projects — <name>`, `Tools — <title>`, `Meetings — <title>` (under the domain meetings fit best, usually `projects` or `research`), `<Topic> — <subtitle> (<Author>)` for distilled outside sources, and `<Owner first name> — <topic>` for `personal`.
   - Leave the hub list empty. Hubs are earned, not declared.
7. **Templates.** For each domain that was dropped, move its template from `templates/` to `outputs/_setup/unused-templates/`. One exception: `Template — Meeting` is tagged `projects` but useful in most brains. If `projects` was dropped, retag it to the surviving domain meetings fit best (ask if unclear) and move its `Meetings —` prefix to that domain's row in the Vault Map. For a new domain that needs a recurring page shape, write a template following the pattern of the others. Every template's first tag must be a domain from the final list.
8. **Owner page.** If the person wants pages about themselves, create `wiki/<First name> — Working Style.md` from the stub below, add it to the index under the `personal` section, and keep the rules file's working-style paragraph pointing at it.

   If the person does not want pages about themselves, remove every trace of `personal`: the working-style paragraph in the rules file, the `personal` row of its Domains table, the two sentences after that table that use a page about the owner as the example, the "Pages about <owner>" bullet in the Confidentiality section (if kept), the Personal rows of both Vault Map tables, the `## Personal` index section, and the owner's colour group in `.obsidian/graph.json`.

   ```markdown
   ---
   title: "<First name> — Working Style"
   tags: [personal]
   status: seed
   audience: [internal]
   people: ["<Full name>"]
   project: ""
   date_created: <today>
   date_updated: <today>
   sources: 0
   ---

   # <First name> — Working Style

   How <First name> likes to work and write. Read before writing anything in their voice. Grows as they correct drafts.

   ## How I like to work

   ## How I write

   ## Words and habits to avoid

   ## Related

   - [[Vault Map]]
   ```

9. **README.** Replace `README.md` with the brain's own README, using the block at the end of this file, filled in.
10. **Obsidian.** If the person won't use Obsidian, move `.obsidian/` and `wiki/queries.md` to `outputs/_setup/obsidian/`. Then remove every mention of `queries`: its line in the rules file's directory diagram, the word in the rules file's `system` domain definition, its entry in `wiki/index.md`, and the mentions in `wiki/Vault Map.md` (the opening paragraph, the entry points, and the System row). If they will use Obsidian, update the colour groups in `.obsidian/graph.json` so each domain's prefix gets a colour, and drop groups for domains that were removed.
11. **Git.** If the person chose git and git is not set up yet, run `git init -b main` in the folder (or, if the tool cannot run commands, give the person the commands). With a remote, ask for its URL and add it as `origin`. Don't commit. The first commit waits for the person's trigger.
12. **Log.** Replace the placeholder entry in `wiki/log.md` with:

    `## [YYYY-MM-DD] init | <Brain name> set up from the LLM Wiki template v<template_version>`

    followed by a few lines: the domains, the choices made, the files renamed or moved.
13. **Open items.** In `wiki/open-items.md`, record each setup choice in the decisions log with today's date, so later sessions know they were decisions and not accidents.

## Step 5. Prove it is clean

From the brain's root, run:

```
python3 -B skills/lint/tools/vault_check.py
```

The report should show one finding only: "SETUP.md is still at the root", which step 6 clears. A leftover `{{...}}` or `<!-- SETUP` comment shows up under "Setup leftovers". Fix every other finding and run it again until that one is all that remains. If your tool cannot run commands, read through each file for leftovers yourself and tell the person the script could not run.

Then open three files and read them as a newcomer would: the rules file, `wiki/Vault Map.md`, and `wiki/index.md`. They should read as one brain with one name and one set of domains.

## Step 6. Retire this file

Ask the person before touching this file. On their yes, move it to `outputs/_setup/SETUP-ARCHIVE-YYYY-MM-DD.md`. It is history now: the log and open-items hold what was decided.

## Step 7. Schedule the health check and hand over

**Schedule it.** If the person chose a regular health check, create it now, following the adapter's *Scheduled health check* section (`CLAUDE.md` for Claude, `AGENTS.md` for other tools). Record it in the decisions log and the log. If it can't be created, say why and suggest a calendar reminder instead.

Then tell the person, briefly and in plain words (no file jargon):

- what was built and where the rules live
- how to add the first source: drop a file into `raw/` or paste something into the chat and say "ingest this"
- how to ask questions: just ask
- how to keep it healthy: if a health check is scheduled, how often it runs, that each one leaves a report and a note in open items for them to review, and that it fixes nothing without their yes. Otherwise, say "lint" every couple of weeks
- if they chose Obsidian, the Obsidian steps from the README
- that "check for template updates" brings in later improvements to the template

---

## The brain's README

Write this as the new `README.md`, filled in. Keep the credit line at the bottom.

```markdown
# <Brain name>

<One or two sentences: what this brain is for, in the owner's words.>

This folder is a personal knowledge base that your AI assistant writes and keeps up to date. You add things worth knowing and ask questions. The AI writes the pages, links them together, and keeps a record of every change. Everything is plain text files in this folder on your computer.

## Everyday use

Talk to your AI in plain words. These phrases work, and so do your own versions of them.

| You say | What happens |
|---|---|
| "ingest this", "save this", "file this" | The AI saves the original in `raw/`, then writes or updates the pages it touches. |
| Any question | The AI answers from your pages and says where each answer came from. |
| "lint" or "health check" | The AI checks for broken links, outdated facts, and gaps, points out pages worth connecting, and suggests fixes before making them. <If scheduled: "It also runs on its own every <interval> and leaves a report for you to review."> |
| "share this" | The AI makes a clean copy of a page for someone else, with private details removed, in `outputs/shared/`. |
| "check for template updates" | The AI looks for improvements to the template this brain came from and offers to add them. |

## Where things are

- `raw/`: your originals. The AI never changes them.
- `wiki/`: the pages the AI writes. Start with `wiki/index.md`, a list of every page.
- `outputs/`: finished things, like reports and shareable copies.
- `<RULES_FILE>`: the rules your AI follows. It reads them at the start of every session.

## Reading it in Obsidian

<!-- SETUP: Keep this section if the owner uses Obsidian. Otherwise delete it. Delete this comment either way. -->

1. Install Obsidian from obsidian.md, choose **Open folder as vault**, and pick this folder.
2. Optional: install the **Dataview** plugin from Obsidian's community plugins, so `wiki/queries.md` shows live tables of open items and recent changes.
3. Open the graph view to see how your pages connect. Well-connected pages are your core topics.

Leave Obsidian's paid Sync and Publish features off unless you mean to send the brain somewhere.

---

Built from the [LLM Wiki template](https://github.com/uxjamie/LLM-Wiki) by Jamie Hall, based on Andrej Karpathy's [LLM Wiki idea file](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f). MIT License.
```
