# Changelog

Versions of the LLM Wiki template. A brain records the version it was built from in its rules file (`template_version`). When its owner says "check for template updates", the AI reads this file, lists the versions newer than that, and applies each one on the owner's yes.

Each entry has two parts:

- **Why:** what problem the change fixes, in a sentence or two.
- **Apply:** steps an AI can follow inside an existing brain. Steps name files by their role (the rules file, the Vault Map), because every brain names its rules file differently and may have renamed its domains.

Newest first.

---

## [0.2.4] 2026-10-20

Template updates read the changelog and files from the newest release tag instead of the `main` branch.

**Why:** a brain checking for updates fetched an old cached copy of `main` that stopped two versions back, and concluded the template had been rolled back. A tag's files never change, so fetching by tag can't return a stale copy. A version older than the brain's own is now treated as a stale copy, never as a rollback.

**Apply:**

1. In the rules file's "Template updates" section, replace step 1 with the template's step 1, including the paragraph under it that starts "If the newest version listed is older".
2. Set `template_version` to `0.2.4`.

---

## [0.2.3] 2026-10-19

Keeps open-items light. Finished items move to a new archive page the same turn, and held conflicts live only on their pages.

**Why:** open-items is read at the start of every session, so everything left in it costs tokens every time. In one long-running brain, checked items and old decisions had grown it to 121 KB, about 30,000 tokens per session. Moving finished items out as they close keeps that cost flat. Held conflicts already sit on their pages with a flag, and lint looks at every flagged page, so a second list in open-items only adds weight.

**Apply:**

1. In the rules file's session protocol, replace the sentence in the open-items step that starts "Keep it current:" with the template's, which starts "Keep it current and light:".
2. In the rules file's directory diagram, replace the `open-items.md` line with the template's two lines (open-items, then open-items-archive). In the table of rule homes, add the template's `[[open-items-archive]]` row.
3. In the rules file's trust layer, in "Hold contradictions", replace "and add a line to `open-items.md` naming who could resolve it." with the template's ending, which starts "and name on the page who could resolve it."
4. Create `wiki/open-items-archive.md` from the template, with `{{CREATED}}` set to today. If the brain already keeps an archive of its own, keep it and add the three sections it lacks (Done, Shelved, Retired decisions).
5. In `wiki/open-items.md`, replace the opening sentence that starts "Check items off" with the template's, which starts "When an item finishes". Then list every checked item for the owner. On their yes, move each one, word for word, to the archive under *Done*, newest first.
6. If open-items has a held-conflicts section, check that each conflict it names carries a `conflicts` flag and a Conflicts section on its page. Add any that are missing. Then, on the owner's yes, move the section into the archive under *Retired decisions*, noting that held conflicts now live on their pages.
7. Add the template's `[[open-items-archive]]` line to the index's System section and to the Vault Map's entry points.
8. In the lint skill, replace step 1's ending "Vault Map drift, and hub candidates." and the "Open-items drift" bullet with the template's. If the frontmatter says `skills: installed`, rebuild and reinstall the lint skill afterward.
9. Replace `skills/lint/tools/vault_check.py` and `skills/lint/tools/test_vault_check.py` with the template's versions, then run `python3 -B skills/lint/tools/test_vault_check.py`. The checker now flags checked items left in open-items and an open-items file past 25 KB.
10. Set `template_version` to `0.2.3`.

---

## [0.2.2] 2026-10-16

Makes the migration guide's rule for shared files explicit: keep the brain's file and add what's missing, never replace it.

**Why:** a migration plan that said "keep the brain's map" read like an overwrite to one owner, and keeping a file as it was could also leave out a section the template depends on. Now every shared file keeps the owner's version as the base, and the plan lists each piece to add for approval.

**Apply:** nothing. The change is in `MIGRATE.md`, which is only used during a move onto the template.

---

## [0.2.1] 2026-10-16

Lets a brain keep its own index sections, and stops the checker flagging skill links in a brain whose skills are installed in an AI app.

**Why:** moving a real brain showed two false alarms that would come back on every lint. An index grouped by the owner's own sections, such as work in progress, reference, was always flagged as not following the domains. And with `skills: installed`, links like `[[ingest]]` were reported as broken, because there's no skill file in the folder.

**Apply:**

1. In the rules file's "Index format" section, replace the first sentence with the one from the template's `BRAIN.md` that starts "Organized by domain, one section per domain, unless". If this brain's index uses its own sections, add the `### Index sections` table it describes.
2. If the frontmatter says `skills: installed`, add the sentence from the template's `BRAIN.md` that ends "still count as skill links.", and make sure that table in `CLAUDE.md` names each installed skill in its first column.
3. Replace `skills/lint/tools/vault_check.py` and `skills/lint/tools/test_vault_check.py` with the template's versions, then run `python3 -B skills/lint/tools/test_vault_check.py`.
4. Set `template_version` to `0.2.1`.

---

## [0.2.0] 2026-10-16

Adds a guide for moving an existing brain onto the template, lets a brain keep its skills installed in an AI app, and gives a brain a place for checks of its own.

**Why:** people who built a wiki before this template existed can now bring it up to date without starting over. Some of those brains keep their skills installed in an AI app rather than in the folder, and template updates need to handle that. Many also have a health check of their own, built from lessons that brain learned, and those checks should keep running beside the template's. A rehearsal move of a real brain also showed the checker flagging pages it should have left alone.

**Apply:**

1. In the rules file's frontmatter, add `skills: folder` on the line after `template_version`. (Use `skills: installed` only if this brain's skills live in an AI app instead of the folder.)
2. In the rules file's "Skills live in this folder" section, after the **Rule** paragraph, add the paragraph from the template's `BRAIN.md` that starts "Where the skills live is recorded in the frontmatter".
3. In the rules file's "Template updates" section, after step 4, add the paragraph from the template's `BRAIN.md` that starts "If the frontmatter says `skills: installed`".
4. In the same section, before the paragraph that starts "Never apply a template change", add the paragraph from the template's `BRAIN.md` that starts "An update may replace". In the "Skills live in this folder" section, add the sentence from the template's `BRAIN.md` that starts "Checks that only make sense for this brain".
5. Replace `skills/lint/tools/vault_check.py` and `skills/lint/tools/test_vault_check.py` with the template's versions. Then run `python3 -B skills/lint/tools/test_vault_check.py`. The new checker treats pages tagged `system` as system pages, accepts unprefixed pages listed by exact name in the Vault Map, and scales the hub threshold with the brain's size.
6. In the lint skill, step 1, add the two sentences from the template's lint skill that start "If `skills/lint/tools/extra_checks.py` exists".
7. In the Vault Map's "Rules of the road", add the two sentences from the template's Vault Map that start "A page kept unprefixed on purpose".
8. Set `template_version` to `0.2.0`.

`MIGRATE.md` itself is not copied into existing brains. It is read from the template when needed.

---

## [0.1.0] 2026-10-16

First release.

**Why:** a starting point for a brain that goes past the original LLM Wiki idea, with the structure and checks worked out over months of daily use.

**Apply:** nothing. This is the version every brain starts from.
