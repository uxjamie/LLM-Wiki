#!/usr/bin/env python3
"""Tests for vault_check.py. Run: python3 -B test_vault_check.py

Builds a small stand-in brain in a temp folder with one planted defect per check,
plus the cases that must stay clean because the brain does them on purpose:
skill links, same-page heading links, old names in the append-only log, a
company name that starts lowercase, example paths in the rules file. The rules
file is named ORBIT.md here on purpose: the checker must find it by its
frontmatter marker, never by name. When a false flag turns up in a real brain,
add a case here so it stays fixed.
"""
import io
import os
import shutil
import sys
import tempfile
from contextlib import redirect_stderr, redirect_stdout

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import vault_check as vc                        # noqa: E402

TODAY = '2026-10-16'


def page(title, tags='[tools]', status='evergreen', audience='[internal]', sources=1,
         created='2026-06-01', updated='2026-10-01', extra='', body='Body text.'):
    return (f'---\ntitle: "{title}"\ntags: {tags}\nstatus: {status}\naudience: {audience}\n'
            f'people: []\nproject: ""\ndate_created: {created}\ndate_updated: {updated}\n'
            f'sources: {sources}\n{extra}---\n\n# {title}\n\n{body}\n')


RULES = ('---\nllm-wiki: rules\nbrain: "Orbit"\ntemplate_version: 0.1.0\n---\n\n# Orbit: Operating Rules\n\n'
         '```\nOrbit/\n├── ORBIT.md               ← rules\n├── skills/                ← skills\n'
         '├── wiki/                  ← wiki\n│   ├── index.md           ← catalog\n'
         '│   └── gone-page.md       ← a stale entry\n└── outputs/\n```\n\n'
         'Example names: `EXAMPLE.md` and `outputs/<project>/<slug>-WIP.md`. Real path: `wiki/index.md`. '
         'Stale path: `scripts/missing.sh`. Own checks: `skills/lint/tools/extra_checks.py`. Skills: [[lint]] and [[ingest]].\n\n'
         '## Wiki page format\n\n### Domains\n\n| Domain | What |\n|---|---|\n'
         '| `research` | sources |\n| `ideas` | thinking |\n| `people` | people |\n'
         '| `tools` | methods |\n| `components` | a custom domain |\n| `design-decisions` | hyphenated |\n'
         '| `system` | machinery |\n\n'
         '### Statuses\n\n| Status | Meaning |\n|---|---|\n| `seed` | x |\n| `developing` | x |\n'
         '| `draft` | x |\n| `published` | x |\n| `evergreen` | x |\n\n'
         '### Audiences\n\n| Audience | Meaning |\n|---|---|\n| `internal` | x |\n| `team` | x |\n\n'
         '## Vault Map\n\nThe map rule.\n\n## Index format (`wiki/index.md`)\n\nEntries.\n')

FILES = {
    'ORBIT.md': RULES,
    'CLAUDE.md': 'Read `ORBIT.md` first.\n',
    'AGENTS.md': 'Read `BRAIN.md` first.\n',                       # stale pointer after a rename
    'skills/lint/SKILL.md': '---\nname: lint\ndescription: Health check for the Orbit brain.\n---\nLint.\n',
    'skills/ingest/SKILL.md': ('---\nname: ingest\ndescription: Ingest into the Orbit brain.\n---\n'
                               'Never run git push from here. Read the rules file. Save as `<slug>-WIP.md`.\n'),
    'skills/courier/SKILL.md': ('---\nname: courier\ndescription: Share a page from the brain.\n---\n'
                                'Read ORBIT.md first. Read CLAUDE.md too. Then read BRAIN.md.\nNever write to C:\\Users\\sam.\n'),
    'raw/2026-07-01-source.md': 'A raw source.\n',
    'wiki/log.md': '# Log\n\n## [2026-06-01] ingest | old name [[People — Old Name]]\n',
    'wiki/open-items.md': page('Open Items', tags='[system]', body='See [[Tools — Good]].\n\n## Held conflicts\n\nNone yet.'),
    'wiki/queries.md': page('Queries', tags='[system]', body='Views.'),
    'wiki/index.md': (
        '---\ntitle: "Index"\ntags: [system]\nstatus: evergreen\naudience: [internal]\n'
        'date_updated: 2026-10-01\n---\n\n# Index\n\n'
        '## Tools\n\n'
        '- [[Tools — Good]] — a fine page *(1 source)*\n'
        '- [[Tools — Miscounted]] — wrong count *(5 sources)*\n'
        '- [[Tools — Ghost]] — not a real page *(1 source)*\n'
        '- [[Tools — Bare]]\n'
        '- [[Tools — Hyphen - Bad]] — hyphen separator *(1 source)*\n'
        '- [[lowercase-page]] — breaks the convention *(1 source)*\n'
        '- [[Ideas — Misfiled]] — under the wrong section *(1 source)*\n'
        '## Ideas\n\n'
        '- [[Ideas — Stalled]] — an old draft *(1 source)*\n'
        '- [[Ideas — Stalled]] — listed twice *(1 source)*\n'
        '- [[Ideas — Hub]] — linked from many pages *(1 source)*\n'
        '## People\n\n'
        '- [[People — Held]] — a conflict heading with a label *(1 source)*\n'
        '- [[People — Flagged]] — conflicts flag, no section *(1 source)* - [[People — Merged]] — two on one line *(1 source)*\n'
        '## Components\n\n'
        '- [[Components — Button]] — custom domain page *(1 source)*\n'
        '- [[Acme — Tagged]] — undeclared domain tag *(1 source)*\n'
        '## Research\n\n'
        '- [[e2 Labs — Company Overview]] — a lowercase company name *(1 source)*\n'
        '- [[Graph Thing — Agents as Graphs (Doe)]] — a distilled outside source *(1 source)*\n'
        '- [[Unprefixed Content]] — content page with no prefix *(1 source)*\n'
        '- [[Method Page]] — unprefixed on purpose, listed in the map *(1 source)*\n'
        '## Design Decisions\n\n'
        '- [[Decision — Use Tokens]] — hyphenated domain under a spaced heading *(1 source)*\n'
        '## Tools\n\n'
        '- [[Prose Only — Thing]] — named only in map prose *(1 source)*\n'
        '- [[Logistics — Shipping]] — a prefix only a bare `log` word could cover *(1 source)*\n'
        '- [[Tools — Block Tags]] — block-style tags *(1 source)*\n'
        '- [[Tools — With BOM]] — byte-order mark *(1 source)*\n'
        '- [[Tools — Heading Word]] — a heading that mentions conflict *(1 source)*\n'
        '- [[Tools — Snapshotted]] — links to a page that only has a snapshot copy *(1 source)*\n'
        '- [[Tools — Bad Date]] — compact date *(1 source)*\n'
        '## Business\n\n'
        '## System\n\n'
        '- [[Vault Map]] — navigation and filing *(0 sources)*\n'
        '- [[open-items]] — standing decisions\n'
        '- [[queries]] — live views\n'),
    'wiki/Vault Map.md': page('Vault Map', tags='[system]', sources=0, body=(
        'Outputs live at `outputs/<project>/<slug>` and `Prose Only — <thing>` in prose does not count.\n\n'
        '| Domain | Prefixes |\n|---|---|\n| Tools | `Tools —` |\n| Ideas | `Ideas — <title>` |\n'
        '| People | `People — <name>` |\n| Components | `Components — <name>` |\n'
        '| Research | `<Company> — Company Overview`, `<Topic> — <subtitle> (<Author>)` |\n'
        '| Design decisions | `Decision — <title>` |\n'
        '| System | No prefix: `index`, `log`, a bare `<slug>` |\n| Kept unprefixed | `Method Page` |\n\n'
        '## Hub pages\n\n- [[Tools — Good]]\n- [[Tools — Orphan]]\n\n'
        '## Creation\n\n| Page type | Template |\n|---|---|\n| Idea | `Template — Idea` |\n'
        '| Component | `Template — Component` |\n')),
    'wiki/Graph Thing — Agents as Graphs (Doe).md': page(
        'Graph Thing — Agents as Graphs (Doe)', tags='[research]'),
    'templates/Template — Idea.md': 'An idea template.\n',
    'templates/Template — Component.md': 'A component template.\n',
    'templates/Template — Unmapped.md': 'A template the map never names.\n',
    'wiki/Tools — Good.md': page('Tools — Good', body=(
        'Links: [[Ideas — Stalled]], [[Tools — Miscounted]], [[Tools — Bare]], [[lint]], '
        '[[2026-07-01-source]], [[#Body heading]], [[People — Merged]], [[Ideas — Hub]], '
        '[[ORBIT#Wiki page format]], [[ORBIT#No Such Section]], [[ORBIT#Index format (`wiki/index.md`)]].\n\n## Body heading\n\n'
        '| a | b |\n|---|---|\n| [[Tools — Miscounted\\|alias in a table]] | x |\n\n'
        '`[[Not A Link In Code]]`')),
    'wiki/Ideas — Stalled.md': page('Ideas — Stalled', tags='[ideas]', status='developing',
                                    updated='2026-08-01', body='Back to [[Tools — Good]]. [[Ideas — Hub]]'),
    'wiki/Ideas — Misfiled.md': page('Ideas — Misfiled', tags='[ideas]', body='[[Ideas — Hub]]'),
    'wiki/Ideas — Hub.md': page('Ideas — Hub', tags='[ideas]', body='The hub.'),
    'wiki/Tools — Miscounted.md': page('Tools — Miscounted', sources=2, body='[[Tools — Good]] [[Ideas — Hub]]'),
    'wiki/Tools — Bare.md': page('Tools — Bare', body=(
        'Broken: [[People — Nobody]]. Empty: [[People — ]]. Case: [[tools — good]]. '
        'Missing heading: [[#No Such Heading]]. [[Ideas — Hub]]')),
    'wiki/Tools — Hyphen - Bad.md': page('Tools — Hyphen - Bad', body='[[Ideas — Hub]]'),
    'wiki/e2 Labs — Company Overview.md': page('e2 Labs — Company Overview', tags='[research]'),
    'wiki/People — Flagged.md': page('People — Flagged', tags='[people]', extra='conflicts: [x]\n'),
    'wiki/People — Merged.md': page('People — Merged', tags='[people]',
                                    body='## Conflicts\n\nTwo sides, no flag.'),
    'wiki/lowercase-page.md': page('lowercase', status='finished', audience='[internal, blog]',
                                   sources='two', created='2026-09-01', updated='2026-08-01'),
    'wiki/Acme — Tagged.md': page('Acme — Tagged', tags='[acme, process]'),
    'wiki/Components — Button.md': page('Components — Button', tags='[components]'),
    'wiki/Unprefixed Content.md': page('Unprefixed Content', tags='[research]'),
    'wiki/Method Page.md': page('Method Page', tags='[research]'),
    'wiki/Tools — Orphan.md': page('Tools — Orphan'),
    'wiki/plays.md': page('Plays', tags='[system]', body='Recurring moves.'),
    'wiki/People — Held.md': page('People — Held', tags='[people]', extra='conflicts: [y]\n', body='## Conflicts: who owns it\n\nBoth sides.'),
    'wiki/Decision — Use Tokens.md': page('Decision — Use Tokens', tags='[design-decisions]'),
    'wiki/Prose Only — Thing.md': page('Prose Only — Thing', tags='[tools]'),
    'wiki/Logistics — Shipping.md': page('Logistics — Shipping', tags='[tools]'),
    'wiki/Tools — Block Tags.md': ('---\ntitle: "Tools — Block Tags"\ntags:\n  - tools\n  - obsidian\nstatus: evergreen\n'
                                   'audience:\n  - internal\npeople: []\nproject: ""\ndate_created: 2026-06-01\n'
                                   'date_updated: 2026-10-01\nsources: 1\n---\n\nBody.\n'),
    'wiki/Tools — With BOM.md': '\ufeff' + page('Tools — With BOM'),
    'wiki/Tools — Heading Word.md': page('Tools — Heading Word', body='## Conflict resolution style\n\nCalm.'),
    'wiki/Tools — Snapshotted.md': page('Tools — Snapshotted', body='See [[Tools — Deleted Page]].'),
    'outputs/_snapshots/2026-10-01/Tools — Deleted Page.md': page('Tools — Deleted Page'),
    'wiki/Tools — Bad Date.md': page('Tools — Bad Date', updated='20261001'),
    'wiki/Tools — Thin.md': '---\ntitle: "Thin"\ntags: [tools]\n---\n\nNo dates. [[Tools — Orphan]]\n',
}

fails = []
passed = 0


def ok(name, cond, detail=''):
    global passed
    if cond:
        passed += 1
    else:
        fails.append(f'{name}: {detail}')


def build(root, files):
    for rel, text in files.items():
        path = os.path.join(root, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(text)


def has(items, *needles):
    return any(all(n in i for n in needles) for i in items)


root = tempfile.mkdtemp(prefix='llmwiki-')
try:
    build(root, FILES)
    ok('rules file found by marker, not name', vc.find_rules_files(root) == ['ORBIT.md'], vc.find_rules_files(root))
    v = vc.Vault(root, 'ORBIT.md')
    today = vc.dt.date.fromisoformat(TODAY)
    setup = vc.check_setup(v)
    pointers = v.rule_findings + vc.check_pointers(v)
    fm, stalled = vc.check_frontmatter(v, today)
    names = vc.check_filenames(v)
    broken, case, empty, orphans, inbound = vc.check_links(v)
    index = vc.check_index(v)
    homes = vc.check_rule_homes(v)
    roots = vc.check_root_docs(v)
    vmap = vc.check_map(v)
    hubs = vc.check_hubs(v, inbound)

    # ── rules tables are read from the rules file ──────────────────────────
    ok('domains read from the rules file', 'components' in v.domains and 'projects' not in v.domains, v.domains)
    ok('audiences read from the rules file', v.audiences == {'internal', 'team'}, v.audiences)
    ok('no table findings when the tables exist', not v.rule_findings, v.rule_findings)

    # ── setup and pointers ─────────────────────────────────────────────────
    ok('a configured brain has no setup leftovers', not setup, setup)
    ok('stale adapter pointer found', has(pointers, 'AGENTS.md', 'ORBIT.md', 'BRAIN.md'), pointers)
    ok('a correct adapter pointer passes', not has(pointers, 'CLAUDE.md'), pointers)
    ok('skill description without the brain name found', has(pointers, 'courier', 'Orbit'), pointers)
    ok('skill descriptions with the name pass', not has(pointers, 'skills/lint/') and not has(pointers, 'ingest'), pointers)

    # ── frontmatter ────────────────────────────────────────────────────────
    ok('missing fields', has(fm, 'Tools — Thin.md', 'missing', 'status', 'date_updated'), fm)
    ok('system page needs fewer fields', not has(fm, 'open-items.md', 'missing'), fm)
    ok('index (system) needs fewer fields', not has(fm, 'index.md', 'missing'), fm)
    ok('log.md has no frontmatter by design', not has(fm, 'log.md'), fm)
    ok('bad status', has(fm, 'lowercase-page.md', 'status "finished"'), fm)
    ok('audience outside the declared table', has(fm, 'lowercase-page.md', 'audience', 'blog'), fm)
    ok('sources not a number', has(fm, 'lowercase-page.md', 'sources "two"'), fm)
    ok('updated before created', has(fm, 'lowercase-page.md', 'earlier than date_created'), fm)
    ok('undeclared domain flagged (the brain subject as a domain)', has(fm, 'Acme — Tagged.md', 'first tag "acme"'), fm)
    ok('a custom declared domain passes', not has(fm, 'Components — Button.md'), fm)
    ok('flag without section', has(fm, 'People — Flagged.md', 'flag but no Conflicts section'), fm)
    ok('section without flag', has(fm, 'People — Merged.md', 'Conflicts section but no conflicts flag'), fm)
    ok('clean page stays clean', not has(fm, 'Tools — Good.md'), fm)

    # ── stalled drafts ─────────────────────────────────────────────────────
    ok('developing page 76 days old is stalled', has(stalled, 'Ideas — Stalled.md', '76 days'), stalled)
    ok('evergreen pages never stall', not has(stalled, 'Tools — Good.md'), stalled)

    # ── filenames ──────────────────────────────────────────────────────────
    ok('lowercase-hyphenated name flagged', has(names, 'lowercase-page.md'), names)
    ok('hyphen used as a separator flagged', has(names, 'Tools — Hyphen - Bad.md', 'hyphen'), names)
    ok('"e2 Labs" may start lowercase', not has(names, 'e2 Labs'), names)
    ok('system files keep their names', not has(names, 'index.md') and not has(names, 'open-items.md'), names)

    # ── links ──────────────────────────────────────────────────────────────
    ok('broken link found', has(broken, 'Tools — Bare.md', 'People — Nobody'), broken)
    ok('missing same-page heading found', has(broken, 'No Such Heading'), broken)
    ok('missing heading on another page found', has(broken, 'ORBIT#No Such Section'), broken)
    ok('a real heading on the rules file resolves', not has(broken, 'ORBIT#Wiki page format'), broken)
    ok('empty link found', has(empty, '[[People — ]]'), empty)
    ok('case-only match found', has(case, 'tools — good'), case)
    ok('skill links are never findings', not has(broken + empty + case, '[[lint]]')
       and not has(broken, '[[ingest]]'), broken)
    ok('a link to a raw source resolves', not has(broken, '2026-07-01-source'), broken)
    ok('a same-page heading link is fine', not has(broken + empty, 'Body heading'), broken + empty)
    ok('an escaped pipe in a table resolves', not has(broken, 'alias in a table'), broken)
    ok('links inside code are ignored', not has(broken, 'Not A Link In Code'), broken)
    ok('old names in log.md are history, not findings', not has(broken, 'Old Name'), broken)

    # ── orphans ────────────────────────────────────────────────────────────
    ok('a page with no inbound link is an orphan', 'Tools — Thin.md' in orphans, orphans)
    ok('a page linked only by another page is not', 'Tools — Orphan.md' not in orphans, orphans)
    ok('index entries count as inbound', 'Acme — Tagged.md' not in orphans, orphans)
    ok('system files are never orphans', 'open-items.md' not in orphans, orphans)

    # ── index ──────────────────────────────────────────────────────────────
    ok('duplicate entry', has(index, 'Ideas — Stalled', 'listed again'), index)
    ok('count mismatch', has(index, 'Tools — Miscounted', 'says 5', 'page says 2'), index)
    ok('entry for a page that does not exist', has(index, 'Tools — Ghost', 'not a page'), index)
    ok('entry without a description', has(index, 'Tools — Bare', 'no description'), index)
    ok('two entries on one line', has(index, '2 entries on one line'), index)
    ok('unlisted page', has(index, '"Tools — Orphan" is not listed'), index)
    ok('system files need no entry', not has(index, '"open-items" is not listed'), index)
    ok('system files may be listed', not has(index, '"open-items" is not a page'), index)
    ok('entry under the wrong domain section', has(index, 'Ideas — Misfiled', 'under "Tools"', '"ideas"'), index)
    ok('section that is not a declared domain', has(index, 'section "Business"'), index)

    # ── rule homes ─────────────────────────────────────────────────────────
    ok('git command in a skill flagged', has(homes, 'ingest', 'git push'), homes)
    ok('a stale rules file name in a skill is flagged', has(homes, 'courier', '"BRAIN.md"'), homes)
    ok('the real rules file name in a skill is fine', not has(homes, '"ORBIT.md"'), homes)
    ok('adapter names are fine in skills', not has(homes, '"CLAUDE.md"'), homes)
    ok('-WIP.md filename patterns are not rules files', not has(homes, '"WIP.md"'), homes)
    ok('a skill pointing at "the rules file" is fine', not has(homes, 'skills/lint/'), homes)

    # ── root docs ──────────────────────────────────────────────────────────
    ok('stale backticked path found', has(roots, 'scripts/missing.sh'), roots)
    ok('stale entry in the directory diagram found', has(roots, 'wiki/gone-page.md'), roots)
    ok('real paths pass', not has(roots, 'wiki/index.md`'), roots)
    ok('the optional extra checks file may be absent', not has(roots, 'extra_checks.py'), roots)
    ok('examples are not paths', not has(roots, 'EXAMPLE.md') and not has(roots, '<project>'), roots)

    # ── vault map ──────────────────────────────────────────────────────────
    ok('a prefix the map does not name is flagged', has(vmap, '"Acme —"', '1 page'), vmap)
    ok('a prefix the map names passes', not has(vmap, '"Tools —"') and not has(vmap, '"People —"'), vmap)
    ok('a prefix written with a placeholder passes', not has(vmap, '"Ideas —"'), vmap)
    ok('<Company> — Company Overview covers a company page', not has(vmap, 'e2 Labs'), vmap)
    ok('<Topic> — <subtitle> (<Author>) covers an outside source', not has(vmap, 'Graph Thing'), vmap)
    ok('a content page with no prefix is flagged', has(vmap, 'Unprefixed Content.md', 'no prefix'), vmap)
    ok('an unmapped template is flagged', has(vmap, 'Template — Unmapped.md'), vmap)
    ok('a mapped template passes', not has(vmap, 'Template — Idea.md'), vmap)
    ok('the map itself is not a finding', not has(vmap, 'Vault Map.md:'), vmap)

    # ── hubs ───────────────────────────────────────────────────────────────
    ok('a page five distinct pages link to is a hub candidate', has(hubs, 'Ideas — Hub', 'distinct pages'), hubs)
    ok('a quiet listed hub is flagged', has(hubs, 'Tools — Orphan', 'listed as a hub'), hubs)
    ok('hubs count distinct pages, not mentions', len(inbound['Ideas — Hub']) == len(set(inbound['Ideas — Hub'])), inbound)

    # ── review fixes (2026-10-16) ──────────────────────────────────────────
    ok('block-style YAML tags are read', not has(fm, 'Tools — Block Tags.md'), fm)
    ok('a byte-order mark does not hide frontmatter', not has(fm, 'Tools — With BOM.md'), fm)
    ok('a heading that only mentions conflict is not a Conflicts section', not has(fm, 'Tools — Heading Word.md'), fm)
    ok('a compact date is not a date', has(fm, 'Tools — Bad Date.md', 'date_updated'), fm)
    ok('a spaced heading matches a hyphenated domain', not has(index, 'section "Design Decisions"')
       and not has(index, '"Decision — Use Tokens" is under'), index)
    ok('a bare backticked word does not cover a prefix', has(vmap, '"Logistics —"'), vmap)
    ok('a prefix written only in prose does not count', has(vmap, '"Prose Only —"'), vmap)
    ok('a snapshot copy does not hide a broken link', has(broken, 'Tools — Deleted Page'), broken)
    ok('a single-backslash Windows path in a skill is flagged', has(homes, 'courier', 'local path'), homes)

    ok('an unprefixed page listed by exact name in the map passes', not has(vmap, 'Method Page.md'), vmap)
    ok('a link to a heading containing code resolves', not has(broken, 'Index format'), broken)
    ok('a system-tagged page keeps its lowercase name', not has(names, 'plays.md'), names)
    ok('a system-tagged page needs no index entry', not has(index, '"plays"'), index)
    ok('a system-tagged page is never an orphan', 'plays.md' not in orphans, orphans)
    ok('a system-tagged page needs no prefix', not has(vmap, 'plays.md'), vmap)
    ok('"Conflicts: label" counts as a Conflicts section', not has(fm, 'People — Held.md'), fm)
    ok('a system page may gather held conflicts without a flag', not has(fm, 'open-items.md'), fm)
    ok('hub threshold rises with brain size', vc.hub_threshold(v) == max(vc.HUB_MIN, round(len(v.pages) * 0.05)))

    v.text = {k: t for k, t in v.text.items() if k != 'Vault Map.md'}
    ok('a missing map is one finding', len(vc.check_map(v)) == 1 and 'is missing' in vc.check_map(v)[0], vc.check_map(v))

    # ── open items stay light (0.2.3) ──────────────────────────────────────
    ok('an open-items with no checked items passes', vc.check_open_items(v) == [], vc.check_open_items(v))
    v.text['open-items.md'] = page('Open Items', tags='[system]', body='- [ ] live\n- [x] done\n  - [X] nested done')
    oi = vc.check_open_items(v)
    ok('checked items left in open-items are flagged', sum('checked item' in i for i in oi) == 2, oi)
    ok('an unchecked item is not flagged', not has(oi, 'live'), oi)
    v.text['open-items.md'] = page('Open Items', tags='[system]', body='- [ ] a live item\n' * 2000)
    ok('an open-items past 25 KB is flagged', has(vc.check_open_items(v), 'propose an archive pass'), vc.check_open_items(v))
    del v.text['open-items.md']
    ok('a brain with no open-items is not flagged here', vc.check_open_items(v) == [], vc.check_open_items(v))
finally:
    shutil.rmtree(root)


# ── an unconfigured template reports setup leftovers ───────────────────────
tpl = tempfile.mkdtemp(prefix='llmwiki-tpl-')
try:
    build(tpl, {
        'BRAIN.md': ('---\nllm-wiki: rules\nbrain: "{{BRAIN_NAME}}"\ntemplate_version: 0.1.0\n---\n\n'
                     '# {{BRAIN_NAME}}\n\n<!-- SETUP: fill this -->\n\n### Domains\n\n| D | W |\n|---|---|\n'
                     '| `research` | x |\n\n### Statuses\n\n| S | M |\n|---|---|\n| `seed` | x |\n| `evergreen` | x |\n\n'
                     '### Audiences\n\n| A | M |\n|---|---|\n| `internal` | x |\n'),
        'SETUP.md': 'Run me. {{BRAIN_NAME}}\n',
        'CLAUDE.md': 'If SETUP.md exists, run it. Until then the rules file is `BRAIN.md`. Read `{{RULES_FILE}}`.\n',
        'AGENTS.md': 'Read `{{RULES_FILE}}`.\n',
        'wiki/index.md': '---\ntitle: "Index"\ntags: [system]\nstatus: evergreen\naudience: [internal]\n'
                         'date_updated: {{CREATED}}\n---\n\n# Index\n\n## Research\n\n## System\n',
    })
    tv = vc.Vault(tpl, 'BRAIN.md')
    ts = vc.check_setup(tv)
    ok('SETUP.md still present is reported', has(ts, 'SETUP.md is still at the root'), ts)
    ok('placeholders are reported per file', has(ts, 'BRAIN.md', '{{BRAIN_NAME}}', 'SETUP comment'), ts)
    ok('a placeholder date is not also a frontmatter finding', not vc.check_frontmatter(tv, vc.dt.date.today())[0], vc.check_frontmatter(tv, vc.dt.date.today())[0])
    ok('adapters holding placeholders are not pointer findings', not vc.check_pointers(tv), vc.check_pointers(tv))
finally:
    shutil.rmtree(tpl)


# ── skills installed in an app, and index sections the owner chose ────────
inst = tempfile.mkdtemp(prefix='llmwiki-inst-')
try:
    rules = ('---\nllm-wiki: rules\nbrain: "Beacon"\ntemplate_version: 0.2.1\nskills: installed\n---\n\n'
             '# Beacon\n\n### Domains\n\n| D | W |\n|---|---|\n| `tools` | x |\n| `people` | x |\n| `system` | x |\n\n'
             '## Index format\n\n### Index sections\n\n| Section | Holds |\n|---|---|\n'
             '| `Work in progress` | live work |\n| `Reference` | lookups |\n')
    build(inst, {
        'BEACON.md': rules,
        'CLAUDE.md': ('Read `BEACON.md` first.\n\n## When to use each skill\n\n| Skill | Use it when | Where |\n'
                      '|---|---|---|\n| ingest | a source arrives | installed in the app |\n'
                      '| `lint` | health check | installed in the app |\n'),
        'wiki/index.md': ('---\ntitle: "Index"\ntags: [system]\nstatus: evergreen\naudience: [internal]\n'
                          'date_updated: 2026-10-01\n---\n\n# Index\n\n## Work in progress\n\n'
                          '- [[Tools — Plan]] — the plan\n\n## Reference\n\n- [[People — Ada]] — a person\n\n'
                          '## Stray\n\n'),
        'wiki/Tools — Plan.md': page('Tools — Plan', body='Run [[ingest]] then [[lint]]. Not [[courier]].'),
        'wiki/People — Ada.md': page('People — Ada', tags='[people]', body='See [[Tools — Plan]].'),
    })
    vi = vc.Vault(inst, 'BEACON.md')
    ib, _, _, _, _ = vc.check_links(vi)
    ii = vc.check_index(vi)
    ok('installed skills named in the adapter table resolve', not has(ib, '[[ingest]]') and not has(ib, '[[lint]]'), ib)
    ok('a skill missing from the table is still broken', has(ib, 'courier'), ib)
    ok('declared index sections pass', not has(ii, 'Work in progress') and not has(ii, '"Reference"'), ii)
    ok('an undeclared section is still flagged', has(ii, '"Stray" is not a declared domain'), ii)
    ok('a page in a declared section is not called misplaced', not has(ii, 'but its domain is'), ii)
finally:
    shutil.rmtree(inst)


# ── a check before a migration: other folder name, no marker yet ──────────
pre = tempfile.mkdtemp(prefix='llmwiki-pre-')
try:
    build(pre, {'OLD.md': '# Old rules\n\n### Domains\n\n| D | W |\n|---|---|\n| `tools` | x |\n',
                'pages/index.md': '---\ntitle: "Index"\ntags: [system]\nstatus: evergreen\naudience: [internal]\ndate_updated: 2026-10-01\n---\n\n# Index\n\n## Tools\n'})
    with redirect_stdout(io.StringIO()) as out_, redirect_stderr(io.StringIO()):
        code = vc.main(['--vault', pre, '--wiki', 'pages', '--rules', 'OLD.md', '--today', TODAY])
    ok('--wiki and --rules let the checker run before a migration', code == 0, out_.getvalue()[:300])
    with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
        code2 = vc.main(['--vault', pre, '--today', TODAY])
    ok('without them, the same folder is not a brain yet', code2 == 2)
finally:
    vc.WIKI = 'wiki'
    shutil.rmtree(pre)


# ── it never looks clean when it cannot read ───────────────────────────────
def exit_code(argv):
    with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
        return vc.main(argv)


empty_dir = tempfile.mkdtemp(prefix='llmwiki-not-a-brain-')
ok('a folder that is not a brain exits 2', exit_code(['--vault', empty_dir]) == 2)
build(empty_dir, {'ONE.md': '---\nllm-wiki: rules\n---\n', 'TWO.md': '---\nllm-wiki: rules\n---\n',
                  'wiki/index.md': '# Index\n'})
ok('two rules files exit 2', exit_code(['--vault', empty_dir]) == 2)
shutil.rmtree(empty_dir)

# ── the brain this file lives in still runs end to end ─────────────────────
if vc.find_rules_files(vc.DEFAULT_VAULT) and os.path.isfile(os.path.join(vc.DEFAULT_VAULT, 'wiki', 'index.md')):
    ok('this brain runs and exits 0', exit_code(['--vault', vc.DEFAULT_VAULT, '--today', TODAY]) == 0)
    ok('a bad --today exits 2', exit_code(['--vault', vc.DEFAULT_VAULT, '--today', 'soon']) == 2)
else:
    print(f'  (skipped the end-to-end run: {vc.DEFAULT_VAULT} is not a brain)')

if fails:
    print(f'{len(fails)} FAILED, {passed} passed')
    for f in fails:
        print('  FAIL', f)
    sys.exit(1)
print(f'all {passed} checks passed')
