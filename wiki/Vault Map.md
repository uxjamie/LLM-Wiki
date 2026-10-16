---
title: "Vault Map"
tags: [system]
status: evergreen
audience: [internal]
people: []
project: ""
date_created: {{CREATED}}
date_updated: {{CREATED}}
sources: 0
---

# Vault Map

How to **move through** this brain and **where to put** new pages. The rules live in [[{{RULES_STEM}}]]. The catalog of what exists lives in [[index]]. The live views live in [[queries]]. This map connects them. Read it when you need to find the right pages fast or file a new one consistently.

`wiki/` is flat, with no subfolders. Organization comes from the **domain tag**, the **name prefix**, and **`[[wikilinks]]`**.

---

## Navigation

**Start at [[index]]**, then open the target page and the pages it links to. The second ring of links is often where the real detail sits: the actual number, the source, the decision.

Entry points:

- [[index]]: every page, by domain. Read first for any question.
- [[open-items]]: standing decisions and open work. A decision here governs until {{OWNER_FIRST}} changes it.
- [[queries]]: live views by status, project, person, and staleness. Needs Obsidian with Dataview.
- [[log]]: append-only history of what changed and why.

### Domains and their prefixes

Each domain is an index section. The prefixes in backticks are the page names that live under it. `<...>` marks the variable part. `lint` reads these patterns, so keep the backticks.

<!-- SETUP: One row per domain from the rules file's Domains table. Delete this comment. -->

| Domain | Prefixes |
|---|---|
| Research | `<Topic> — <subtitle> (<Author>)` for a distilled outside source |
| Ideas | `Ideas — <title>` |
| People | `People — <name>` |
| Projects | `Projects — <name>`, `Meetings — <title>` |
| Tools | `Tools — <title>` |
| Personal | `{{OWNER_FIRST}} — <topic>` |
| System | No prefix: `index`, `log`, `open-items`, `queries`, `Vault Map` |

### Hub pages

Pages that many other pages route through. A hub is counted by **distinct pages linking in**, not by mentions. `lint` lists candidates. Add a hub here when it has earned it, and remove one that has gone quiet.

- None yet.

---

## Creation

Everything you write lives in `wiki/` (knowledge) or `outputs/` (deliverables). Never edit a file in `raw/`. New source files are the only writes there (the rule is in [[{{RULES_STEM}}#Directory structure]]). The full frontmatter and naming rules are in [[{{RULES_STEM}}#Wiki page format]].

### Page type → template → prefix

<!-- SETUP: Keep the rows whose domain survived. Add a row for each new domain. Every template in templates/ must appear in this table. Delete this comment. -->

| Page type | Domain | Template | Name |
|---|---|---|---|
| Distilled outside source (article, talk, paper, document) | research | `Template — Source` | `<Topic> — <subtitle> (<Author>)` |
| Idea, thesis, proposal | ideas | `Template — Idea` | `Ideas — <title>` |
| Person | people | `Template — Person` | `People — <name>` |
| Project | projects | `Template — Project` | `Projects — <name>` |
| Meeting notes | projects | `Template — Meeting` | `Meetings — <title>` |
| Method, reference, checklist | tools | none, match a sibling | `Tools — <title>` |
| Page about {{OWNER_FIRST}} | personal | none, match a sibling | `{{OWNER_FIRST}} — <topic>` |

### Rules of the road

- **Filenames are Title Case with ` — ` as the only separator.** Wikilinks are case-sensitive. A wrong-case file is an invisible page.
- **Every page needs an inbound link** from a related page or the [[index]], and an index entry on its own line.
- **A page with no prefix is a system page.** Content pages always take a prefix from the table above. When none fits, add a row here first, or ask {{OWNER_FIRST}}.
- **Frontmatter feeds Dataview. Body links feed the graph.** Both, always.
- **Deliverables go to `outputs/<project>/`** under the output lifecycle (`-WIP`, `-FINAL`, `-SHARED`, `-PUBLISHED`, `-ARCHIVE`), never into `wiki/`.
- **When unsure where something belongs**, file it and add a `needs-review` tag.

---

## Keeping this map current

[[ingest]] updates this map when a source brings something structural: a new prefix, page type, template, domain, or hub. [[lint]] flags prefixes and templates the map does not cover. The rule lives in [[{{RULES_STEM}}#Vault Map]].
