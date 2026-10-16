---
title: "Queries"
tags: [system]
status: evergreen
audience: [internal]
date_created: {{CREATED}}
date_updated: {{CREATED}}
---

# Queries

Live views of the brain, built from page frontmatter. Needs the Dataview plugin in Obsidian. Without it, the blocks below show as plain code and nothing breaks.

---

## Open items

Every unchecked item in [[open-items]].

```dataview
TASK
FROM "wiki/open-items"
WHERE !completed
```

## Recently updated

```dataview
TABLE status, date_updated AS "Updated", sources
FROM "wiki"
WHERE file.name != "log"
SORT date_updated DESC
LIMIT 20
```

## Held conflicts

Pages carrying a `conflicts` flag.

```dataview
TABLE conflicts AS "Conflict", date_updated AS "Updated"
FROM "wiki"
WHERE conflicts
SORT date_updated DESC
```

## Pages by domain

```dataview
TABLE WITHOUT ID tags[0] AS "Domain", length(rows) AS "Pages"
FROM "wiki"
WHERE tags
GROUP BY tags[0]
SORT length(rows) DESC
```

## People

```dataview
TABLE date_updated AS "Updated", sources AS "Sources"
FROM "wiki"
WHERE startswith(file.name, "People —")
SORT file.name ASC
```

## Stalled drafts

`draft` or `developing` pages untouched for 30 days.

```dataview
TABLE status, date_updated AS "Updated"
FROM "wiki"
WHERE (status = "draft" OR status = "developing") AND date_updated <= date(today) - dur(30 days)
SORT date_updated ASC
```

## Needs review

```dataview
LIST
FROM "wiki"
WHERE contains(tags, "needs-review")
```

## Pages by project

```dataview
TABLE WITHOUT ID project AS "Project", length(rows) AS "Pages"
FROM "wiki"
WHERE project
GROUP BY project
SORT length(rows) DESC
```

## Orphans

Pages nothing links to.

```dataview
LIST
FROM "wiki"
WHERE length(file.inlinks) = 0 AND file.name != "index"
```

## Outputs, newest first

```dataview
TABLE file.mtime AS "Modified"
FROM "outputs"
SORT file.mtime DESC
LIMIT 20
```
