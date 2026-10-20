---
name: ingest
description: Ingest a new source into the {{BRAIN_NAME}} brain. Applies only when working inside the {{BRAIN_NAME}} folder, an LLM Wiki brain. Use whenever a file lands in raw/, someone pastes content or a link into chat, or says "ingest this", "file this", "save this", "add this to the brain", or shares a thought worth keeping. Use it even when the word ingest is not said. The job is to distill the source into structured wiki pages with silent checks, not to leave a pile of files.
---

# Ingest

Trigger when a new source arrives, or on "ingest this", "file this", "save this". The checks run silently. Nothing waits for approval. Findings get reported after filing.

## Guard, first, always

Confirm you are inside the {{BRAIN_NAME}} brain: the folder's root holds the rules file (the file `CLAUDE.md` and `AGENTS.md` tell you to read first), its frontmatter carries `llm-wiki: rules` and `brain: "{{BRAIN_NAME}}"`, and `wiki/index.md` exists. If not, say this skill belongs to the {{BRAIN_NAME}} brain and stop. Never create brain files in a folder that is not the brain.

If `SETUP.md` is still at the root, setup has not run. Offer to run it first.

## Procedure

1. **Orient.** If the session has not done it yet, follow the rules file's session protocol. Read `wiki/index.md`, `wiki/open-items.md`, and `wiki/Vault Map.md` so you know what exists, what is decided, and how pages are named.
2. **Capture the source.** A file in `raw/` stays where it is. Something shared in chat gets saved to `raw/` first as `YYYY-MM-DD-topic.md`, then ingested. From here on the source is immutable. For a transcript, write the misrenderings note the rules file's trust layer describes.
3. **Name and place the page.** Pick the page type from the Vault Map's page-type table and name the page from its prefix. If no row fits, that is a structural change (step 7). If the right prefix is unclear, ask rather than invent one. Pick the domain (first tag) from the rules file's Domains table by **what kind of page it is**, reading each definition. The brain's own subject is never the domain. `personal` is only for pages about the owner.
4. **Synthesize.** Write or update the page in `wiki/`, using the matching template from `templates/` when one exists. Complete the frontmatter: title, tags, status, audience, people, project, dates, sources. Write synthesis, not transcription.
5. **File surgery.** Find every existing page this source touches. Update them, strengthen connections, and add `[[wikilinks]]` both ways.
6. **Silent checks.** Run all three before touching the index and log.
   - **Self-audit.** Re-read the source. Test every third-party and quantitative claim on the new and updated pages against it. Fix any label that overstates the support. Drop anything untraceable. The owner's own thinking needs no label.
   - **Hygiene.** The new or updated index line has a description of 100 characters or fewer (rules file, *Index format*). The filename is Title Case with ` — ` as its only separator and a prefix the map lists. The frontmatter carries every required field, and the first tag is a declared domain. Every new page has at least one inbound link. **Scope: the pages this ingest touched, nothing else.** If a check hints at a wider pattern, don't sweep it. Add one line to `open-items.md` naming the pattern for the next lint, and carry on.
   - **Contradiction check.** Compare new claims against existing pages. First ask whether the accounts are separated in time: a change is not a dispute. A real conflict gets a Conflicts section on the page with both sides and their sources, a `conflicts:` frontmatter flag, and a line in `open-items.md` naming who could resolve it.
7. **Index, map, log.** Add or update the page's line in `wiki/index.md`, under its domain's section. Update the source count on the index line of every page whose `sources` changed, including the pages updated in file surgery. If this ingest brought something structural (the rules file's Vault Map section says what counts), update `wiki/Vault Map.md` too. Most ingests leave the map alone. Append a `wiki/log.md` entry naming the files touched and why, including any map change.
8. **Open items.** Update `wiki/open-items.md` if the source settles a standing decision or opens a new one.
9. **Don't sync.** If the brain uses git, committing waits for the owner's trigger (rules file, Git section). End the log entry with `Not committed, awaiting the owner's trigger.`
10. **Report.** One short summary: what was filed, what was updated, and any check findings (a demoted claim, a recorded conflict, a renamed file, a map change and why). Silence on the checks means they passed.

## Imported pages

Pages arriving from another brain or tool are sources. Retag each to this brain's domains, rename it to this brain's prefixes and separator, and drop tags carried over from the old system before filing.

## Reminders

- The distilled pages are the knowledge. The raw files are the evidence.
- No source, no claim, for anything that isn't the owner's own thinking.
- Raw sources are immutable. Ask before removing anything.
- Frontmatter feeds Dataview. Body wikilinks feed the graph. Both, always.
- The full rules are in the rules file.
