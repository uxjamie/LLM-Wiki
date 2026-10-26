#!/usr/bin/env python3
"""Vault check: the mechanical half of an LLM Wiki brain's health check.

This file belongs to the LLM Wiki template. Template updates replace it whole,
so a brain's own checks go in extra_checks.py beside it, never in here.

    python3 -B skills/lint/tools/vault_check.py                 # from the brain's root
    python3 -B skills/lint/tools/vault_check.py --vault <path>  # anywhere else
    python3 -B skills/lint/tools/vault_check.py --today 2026-10-16

It REPORTS. It changes nothing. The lint skill runs it first, so the AI's own
reading goes to what a script cannot judge: contradictions, stale claims, domain
fit, and connections worth making. Every finding is a candidate. Some will be
intended.

The brain's rules are NOT copied in here. Each run reads them from the brain:

    the rules file   the root .md file whose frontmatter says `llm-wiki: rules`
                     (its name changes per brain: BRAIN.md, ATLAS.md, ...)
    Domains          the table under the rules file's "Domains" heading
    Statuses         the table under its "Statuses" heading
    Audiences        the table under its "Audiences" heading
    prefixes, hubs   the backticked patterns and the "Hub pages" section in
                     wiki/Vault Map.md

What it checks:

    setup leftovers  {{PLACEHOLDERS}} and <!-- SETUP --> comments still present
    pointers         CLAUDE.md and AGENTS.md name the real rules file, and every
                     skill's description carries the brain's name
    frontmatter      required fields, declared status / audience values, a
                     declared domain as the first tag, real dates, and a
                     `conflicts` flag only together with a Conflicts section
    filenames        Title Case, ` — ` as the only separator, no two names that
                     differ only by case
    links            wikilinks to pages or headings that do not exist, wrong
                     case, empty links. Skill links ([[ingest]], [[lint]]) are
                     prose shorthand and never reported
    orphans          wiki pages nothing links to (log.md does not count)
    index            every page listed once, under a declared domain's section,
                     with a description of 100 characters or fewer and a
                     source count matching the page
    stalled          draft / developing pages untouched for 30+ days
    rule homes       skills carrying git commands, local paths, app menu paths,
                     or a hardcoded rules file name
    root docs        paths named in the rules file and adapters that do not exist
    vault map        prefixes in use and templates the map does not cover
    hubs             pages many distinct pages link to that the map's hub list
                     leaves out, and listed hubs that have gone quiet
    open items       checked items left in open-items.md (finished items move to
                     open-items-archive.md the same turn) and the file past 25 KB

Use -B (or PYTHONDONTWRITEBYTECODE=1). Some mounted folders cannot delete files,
so a stray __pycache__ folder written there could never be cleaned up.

Exit status: 0 = ran. 2 = not an LLM Wiki brain, or could not read it.
Part of the LLM Wiki template, https://github.com/uxjamie/LLM-Wiki (MIT).
"""
import argparse
import datetime as dt
import os
import re
import sys
import unicodedata

sys.dont_write_bytecode = True

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_VAULT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))

WIKI = 'wiki'
MAP_FILE = 'Vault Map.md'
REQUIRED = ['title', 'tags', 'status', 'audience', 'people', 'project',
            'date_created', 'date_updated', 'sources']
SYSTEM_REQUIRED = ['title', 'tags', 'status', 'audience', 'date_updated']
SYSTEM_FILES = {'index.md', 'log.md', 'open-items.md', 'queries.md'}
ADAPTERS = ['CLAUDE.md', 'AGENTS.md']
TOP_DIRS = ('wiki', 'raw', 'skills', 'scripts', 'templates', 'outputs')
SEP = ' — '
STALL_DAYS = 30
INDEX_DESC_LIMIT = 100                             # characters per index description (rules file, Index format)
OPEN_ITEMS_LIMIT = 25_000                           # bytes; past this an archive pass is due
HUB_MIN = 5            # distinct linking pages before a page is a hub candidate (small brains)
HUB_SHOW = 10          # most hub candidates to list
HUB_QUIET = 2          # a listed hub with fewer distinct linking pages has gone quiet

# Fallbacks, used only when the rules file has lost a table (reported as a finding).
DEFAULT_DOMAINS = {'research', 'ideas', 'people', 'projects', 'tools', 'personal', 'system'}
DEFAULT_STATUSES = {'seed', 'developing', 'draft', 'published', 'evergreen'}
DEFAULT_AUDIENCES = {'internal', 'team', 'public'}

PLACEHOLDER_RX = re.compile(r'\{\{[A-Z][A-Z_]*\}\}')
SETUP_RX = re.compile(r'<!--\s*SETUP\b')
KNOWN_ROOT_MD = {'SKILL.md', 'README.md', 'CLAUDE.md', 'AGENTS.md', 'CHANGELOG.md', 'SETUP.md'}

# Things a skill should point at, never carry.
RULE_HOME_PATTERNS = [
    (re.compile(r'\bgit\s+(?:pull|push|commit|fetch|clone|add|reset|rebase|merge|init)\b'), 'git command'),
    (re.compile(r'/Users/|/home/\w|\b[A-Za-z]:\\(?=\w)|~/'), 'local path'),
    (re.compile(r'\bSettings\s*>\s*\w+'), 'app menu path'),
    (re.compile(r'(?<![\w/-])[A-Z][A-Z0-9-]*\.md\b'), 'file name that exists nowhere in the brain (an old rules file name?)'),
]


def nfc(s):
    # macOS can store accented names decomposed. Compare names in one form.
    return unicodedata.normalize('NFC', s)


def read(path):
    with open(path, encoding='utf-8-sig', errors='replace') as f:     # -sig drops a byte-order mark
        return nfc(f.read())


def frontmatter(text):
    """Return (dict of raw values, body) or (None, text) when there is none."""
    m = re.match(r'---\r?\n(.*?)\r?\n---\r?\n?', text, re.S)
    if not m:
        return None, text
    fm, block = {}, None
    for line in m.group(1).splitlines():
        mm = re.match(r'([A-Za-z_][\w-]*):\s*(.*)$', line)
        if mm:
            fm[mm.group(1)] = mm.group(2).strip()
            block = mm.group(1) if not mm.group(2).strip() else None
            continue
        # Block-style list, as Obsidian's Properties panel writes it:
        #   tags:
        #     - research
        item = re.match(r'\s*-\s+(.*)$', line)
        if item and block:
            items = as_list(fm[block]) if fm[block] else []
            fm[block] = '[' + ', '.join(items + [item.group(1).strip().strip('"\'')]) + ']'
    return fm, text[m.end():]


def unquote(v):
    return (v or '').strip().strip('"\'')


def as_list(v):
    v = (v or '').strip()
    if v.startswith('[') and v.endswith(']'):
        return [x.strip().strip('"\'') for x in v[1:-1].split(',') if x.strip()]
    return [v.strip('"\'')] if v else []


def strip_code(text):
    text = re.sub(r'```.*?```', lambda m: '\n' * m.group(0).count('\n'), text, flags=re.S)
    return re.sub(r'`[^`\n]*`', '', text)


LINK = re.compile(r'!?\[\[([^\]\n]*)\]\]')


def links_in(text):
    """Yield (line_no, raw, page_target, heading) for every wikilink outside code.
    Fenced blocks are blanked. Inline code spans are skipped only when the link
    sits inside one, so a link whose heading contains `code` still resolves."""
    blanked = re.sub(r'```.*?```', lambda m: '\n' * m.group(0).count('\n'), text, flags=re.S)
    for i, line in enumerate(blanked.split('\n'), 1):
        spans = [s.span() for s in re.finditer(r'`[^`\n]*`', line)]
        for m in LINK.finditer(line):
            if any(a <= m.start() < b for a, b in spans):
                continue
            raw = m.group(1).replace('\\|', '|')          # [[Page\|label]] inside a table
            head = re.split(r'\|', raw, maxsplit=1)[0]
            target = re.split(r'[#^]', head, maxsplit=1)[0].strip()
            heading = head.split('#', 1)[1].strip() if '#' in head else ''
            yield i, raw, target, heading


def norm_heading(h):
    return re.sub(r'\s+', ' ', h).strip().lower()


def headings(text):
    return {norm_heading(h) for h in re.findall(r'^#{1,6}\s+(.*?)\s*#*\s*$', strip_code_blocks(text), re.M)}


def strip_code_blocks(text):
    return re.sub(r'```.*?```', '', text, flags=re.S)


def is_date(s):
    s = unquote(s)
    if not re.fullmatch(r'\d{4}-\d{2}-\d{2}', s):
        return False
    try:
        dt.date.fromisoformat(s)
        return True
    except ValueError:
        return False


def find_rules_files(root):
    found = []
    for f in sorted(os.listdir(root)):
        if f.endswith('.md') and os.path.isfile(os.path.join(root, f)):
            fm, _ = frontmatter(read(os.path.join(root, f)))
            if fm and unquote(fm.get('llm-wiki')) == 'rules':
                found.append(f)
    return found


def section(text, title_rx):
    """The text under the first heading matching title_rx, up to the next heading
    of the same or higher level."""
    lines = strip_code_blocks(text).split('\n')
    out, level = None, None
    for line in lines:
        m = re.match(r'^(#{1,6})\s+(.*?)\s*$', line)
        if m:
            if out is not None and len(m.group(1)) <= level:
                break
            if out is None and re.search(title_rx, m.group(2), re.I):
                out, level = [], len(m.group(1))
                continue
        if out is not None:
            out.append(line)
    return None if out is None else '\n'.join(out)


def first_cells(sec):
    """First cell of each body row of every table in sec, backticks removed."""
    cells = []
    for line in (sec or '').split('\n'):
        s = line.strip()
        if not s.startswith('|') or re.match(r'^\|[\s:|-]+\|?$', s):
            continue
        cells.append(s.strip('|').split('|')[0].strip().strip('`').strip())
    return cells[1:] if cells else []                  # the first row is the header


def table_keys(sec):
    """First backticked token in the first cell of each table row."""
    keys = set()
    for line in (sec or '').split('\n'):
        m = re.match(r'^\|\s*`([^`]+)`', line.strip())
        if m:
            keys.add(m.group(1).strip())
    return keys


class Vault:
    def __init__(self, root, rules_file):
        self.root = root
        self.rules_file = rules_file
        self.rules_text = read(os.path.join(root, rules_file))
        rfm, _ = frontmatter(self.rules_text)
        self.brain = unquote((rfm or {}).get('brain'))
        self.template_version = unquote((rfm or {}).get('template_version'))
        self.rule_findings = []
        self.domains = self._declared(r'^Domains\b', DEFAULT_DOMAINS)
        self.statuses = self._declared(r'^Statuses\b', DEFAULT_STATUSES)
        self.audiences = self._declared(r'^Audiences\b', DEFAULT_AUDIENCES)
        self.domains.add('system')
        # Optional: index sections the owner chose instead of one per domain.
        self.index_sections = table_keys(section(self.rules_text, r'^Index sections\b'))
        self.skills_mode = unquote((rfm or {}).get('skills')) or 'folder'
        self.wiki = os.path.join(root, WIKI)
        self.pages = sorted(nfc(f) for f in os.listdir(self.wiki) if f.endswith('.md'))
        self.skills = set()
        sk = os.path.join(root, 'skills')
        if os.path.isdir(sk):
            self.skills = {d for d in os.listdir(sk) if os.path.isfile(os.path.join(sk, d, 'SKILL.md'))}
        # Names a [[skill]] link may use. With `skills: installed` the skills live in an
        # AI app, so their names come from the adapters' "When to use each skill" table.
        self.skill_links = set(self.skills)
        if self.skills_mode == 'installed':
            for a in ('CLAUDE.md', 'AGENTS.md'):
                if not os.path.isfile(os.path.join(root, a)):
                    continue
                sec = section(read(os.path.join(root, a)), r'^When to use each skill\b')
                self.skill_links |= {c for c in first_cells(sec) if re.fullmatch(r'[\w.-]+', c)}
        # Every file a [[link]] could resolve to, by name with and without .md.
        # Pages in wiki/ win over same-named files elsewhere. Working copies under
        # outputs/_* (snapshots, setup leftovers, files waiting to be deleted) are
        # left out, so a copy there never hides a broken link.
        self.names = {}
        walk = []
        for dirpath, dirnames, filenames in os.walk(root):
            rel_dir = os.path.relpath(dirpath, root)
            dirnames[:] = sorted(d for d in dirnames if not d.startswith('.')
                                 and not (rel_dir == 'outputs' and d.startswith('_')))
            for f in sorted(filenames):
                if not f.startswith('.'):
                    walk.append(os.path.relpath(os.path.join(dirpath, f), root))
        walk.sort(key=lambda r: (not r.startswith(WIKI + os.sep), r))
        for rel in walk:
            f = nfc(os.path.basename(rel))
            stem = f[:-3] if f.endswith('.md') else f
            for key in {stem, f}:
                self.names.setdefault(key, rel.replace(os.sep, '/'))
        self.lower = {}
        for k in self.names:
            self.lower.setdefault(k.lower(), k)
        self.text = {p: read(os.path.join(self.wiki, p)) for p in self.pages}
        # System pages: the fixed four, plus any page whose first tag is `system`
        # (an old archive, a plays page, a skill registry). They keep their own
        # names, need no prefix, and are never orphans or required index entries.
        self.system_pages = set(SYSTEM_FILES & set(self.pages))
        for p in self.pages:
            fm, _ = frontmatter(self.text[p])
            tags = as_list((fm or {}).get('tags'))
            if tags and tags[0] == 'system':
                self.system_pages.add(p)  # nfc names open fine on macOS
        self.root_docs = [self.rules_file] + [d for d in ADAPTERS + ['README.md']
                                              if os.path.isfile(os.path.join(root, d))]

    def _declared(self, title_rx, fallback):
        keys = table_keys(section(self.rules_text, title_rx))
        if not keys:
            name = title_rx.strip('^\\b')
            self.rule_findings.append(f'{self.rules_file}: no "{name}" table found, so the defaults were used '
                                      f'({", ".join(sorted(fallback))})')
            return set(fallback)
        return keys


def has_placeholder(v):
    return bool(PLACEHOLDER_RX.search(v or ''))


# ── setup leftovers and pointers ──────────────────────────────────────────

def check_setup(v):
    out = []
    if os.path.isfile(os.path.join(v.root, 'SETUP.md')):
        if has_placeholder(v.rules_text):
            out.append('SETUP.md is still at the root and the rules file holds placeholders: '
                       'setup has not run. Say "Run SETUP.md".')
        else:
            out.append('SETUP.md is still at the root: setup ran but the file has not been retired '
                       '(SETUP.md, step 6).')
    files = list(v.root_docs)
    files += [f'{WIKI}/{p}' for p in v.pages]
    for sub in ('templates',):
        d = os.path.join(v.root, sub)
        if os.path.isdir(d):
            files += [f'{sub}/{f}' for f in sorted(os.listdir(d)) if f.endswith('.md')]
    files += [f'skills/{s}/SKILL.md' for s in sorted(v.skills)]
    od = os.path.join(v.root, '.obsidian')
    if os.path.isdir(od):
        files += [f'.obsidian/{f}' for f in sorted(os.listdir(od)) if f.endswith('.json')]
    for rel in files:
        if rel == 'README.md' and os.path.isfile(os.path.join(v.root, 'SETUP.md')):
            continue                                   # the template's own README, replaced at setup
        text = read(os.path.join(v.root, rel))
        ph = sorted(set(PLACEHOLDER_RX.findall(text)))
        n_setup = len(SETUP_RX.findall(text))
        bits = []
        if ph:
            bits.append(f'{len(PLACEHOLDER_RX.findall(text))} placeholder(s): {", ".join(ph)}')
        if n_setup:
            bits.append(f'{n_setup} SETUP comment(s)')
        if bits:
            out.append(f'{rel}: ' + '; '.join(bits))
    return out


def check_pointers(v):
    out = []
    if not v.brain:
        out.append(f'{v.rules_file}: frontmatter has no `brain:` name')
    for d in ADAPTERS:
        path = os.path.join(v.root, d)
        if not os.path.isfile(path):
            out.append(f'{d} is missing: tools that read it will not find the rules')
            continue
        text = read(path)
        if f'`{v.rules_file}`' not in text and not has_placeholder(text):
            named = sorted(set(re.findall(r'`([A-Z][A-Z0-9-]*\.md)`', text)) - KNOWN_ROOT_MD)
            out.append(f'{d} does not name the rules file `{v.rules_file}`'
                       + (f' (it names {", ".join(named)})' if named else ''))
    if v.brain and not has_placeholder(v.brain):
        for s in sorted(v.skills):
            fm, _ = frontmatter(read(os.path.join(v.root, 'skills', s, 'SKILL.md')))
            desc = (fm or {}).get('description', '')
            if v.brain not in desc:
                out.append(f'skills/{s}/SKILL.md: description does not name the brain "{v.brain}", '
                           f'so it could fire inside another brain')
    return out


# ── pages ─────────────────────────────────────────────────────────────────

def check_frontmatter(v, today):
    out, stalled = [], []
    for p in v.pages:
        if p == 'log.md':
            continue                                   # append-only history, no frontmatter by design
        fm, body = frontmatter(v.text[p])
        if fm is None:
            out.append(f'{p}: no frontmatter')
            continue
        tags = as_list(fm.get('tags'))
        system = bool(tags) and tags[0] == 'system'
        missing = [k for k in (SYSTEM_REQUIRED if system else REQUIRED) if k not in fm]
        if missing:
            out.append(f'{p}: missing {", ".join(missing)}')
        st = unquote(fm.get('status'))
        if st and st not in v.statuses:
            out.append(f'{p}: status "{st}" is not one of {", ".join(sorted(v.statuses))}')
        bad_aud = [a for a in as_list(fm.get('audience')) if a not in v.audiences]
        if bad_aud:
            out.append(f'{p}: audience {bad_aud} not in {sorted(v.audiences)}')
        if not tags:
            out.append(f'{p}: no tags, so no domain')
        elif tags[0] not in v.domains:
            out.append(f'{p}: first tag "{tags[0]}" is not a declared domain '
                       f'({", ".join(sorted(v.domains))})')
        for k in ('date_created', 'date_updated'):
            if k in fm and not has_placeholder(fm[k]) and not is_date(fm[k]):
                out.append(f'{p}: {k} "{fm[k]}" is not a YYYY-MM-DD date')
        if is_date(fm.get('date_created', '')) and is_date(fm.get('date_updated', '')):
            if unquote(fm['date_updated']) < unquote(fm['date_created']):
                out.append(f'{p}: date_updated is earlier than date_created')
        if 'sources' in fm and not re.fullmatch(r'\d+', unquote(fm['sources'])):
            out.append(f'{p}: sources "{fm["sources"]}" is not a whole number')
        has_flag = bool(as_list(fm.get('conflicts')))
        has_section = bool(re.search(r'^#{1,6}\s+(?:Held\s+)?Conflicts?\s*(?:$|[:(—–-])', strip_code_blocks(body), re.M | re.I))
        if has_flag and not has_section:
            out.append(f'{p}: has a conflicts flag but no Conflicts section')
        if has_section and not has_flag and not system and p not in v.system_pages:
            # system pages (open-items, queries) gather conflicts from other pages
            out.append(f'{p}: has a Conflicts section but no conflicts flag')
        if st in ('draft', 'developing') and is_date(fm.get('date_updated', '')):
            age = (today - dt.date.fromisoformat(unquote(fm['date_updated']))).days
            if age >= STALL_DAYS:
                stalled.append((age, f'{p}: {st}, last updated {unquote(fm["date_updated"])} ({age} days)'))
    return out, [s for _, s in sorted(stalled, reverse=True)]


def check_open_items(v):
    text = v.text.get('open-items.md')
    if text is None:
        return []
    out = []
    for i, line in enumerate(text.split('\n'), 1):
        if re.match(r'\s*[-*]\s+\[[xX]\]', line):
            out.append(f'open-items.md:{i}: checked item still here, move it to the archive  {line.strip()[:90]}')
    size = len(text.encode('utf-8'))
    if size > OPEN_ITEMS_LIMIT:
        out.append(f'open-items.md: {size // 1000} KB, past {OPEN_ITEMS_LIMIT // 1000} KB, propose an archive pass (lint skill, Archive pass)')
    return out


def check_filenames(v):
    out = []
    seen = {}
    for p in v.pages:
        if p in v.system_pages:
            continue
        stem = p[:-3]
        if re.fullmatch(r'[a-z0-9][a-z0-9-]*', stem) or stem == stem.lower():
            out.append(f'{p}: lowercase name breaks the Title Case convention')
        m = re.search(r' (-|–) ', stem)
        if m:
            kind = 'hyphen' if m.group(1) == '-' else 'en dash'
            out.append(f'{p}: uses a {kind} as a separator. The only separator is " — " (em dash)')
        if re.search(r'\S—|—\S', stem):
            out.append(f'{p}: em dash without spaces. The separator is " — "')
        key = stem.lower()
        if key in seen:
            out.append(f'{p} and {seen[key]}: names differ only by case')
        seen[key] = p
    return out


def resolve(v, target):
    """'ok', 'case' (resolves only ignoring case), 'skill', 'empty', 'placeholder' or 'missing'."""
    t = target.strip()
    if has_placeholder(t):
        return 'placeholder', None
    if not t or t.endswith(('—', '-', '–')) or re.fullmatch(r'[\s—–-]*', t):
        return 'empty', None
    if t in v.skill_links:
        return 'skill', None
    base = t.split('/')[-1]
    for key in (t, base, t + '.md', base + '.md'):
        if key in v.names:
            return 'ok', v.names[key]
    for key in (t, base):
        if key.lower() in v.lower:
            return 'case', v.lower[key.lower()]
    return 'missing', None


def check_links(v):
    """Returns broken, case, empty, orphans, and inbound: page stem -> set of
    distinct wiki pages linking to it (for the hub check)."""
    broken, case, empty = [], [], []
    inbound = {p[:-3]: set() for p in v.pages}
    sources = [(f'{WIKI}/{p}', v.text[p]) for p in v.pages]
    sources += [(d, read(os.path.join(v.root, d))) for d in v.root_docs]
    heading_cache = {}
    for where, text in sources:
        own = headings(text)
        for line_no, raw, target, heading in links_in(text):
            if not target and raw.startswith('#'):
                if heading and norm_heading(heading) not in own:
                    broken.append(f'{where}:{line_no}: [[{raw}]] names a heading this page does not have')
                continue
            if where == f'{WIKI}/log.md':
                continue                               # append-only history keeps old names on purpose
            kind, hit = resolve(v, target)
            if kind == 'empty':
                empty.append(f'{where}:{line_no}: empty link [[{raw}]]')
            elif kind == 'missing':
                broken.append(f'{where}:{line_no}: [[{raw}]] points to no file')
            elif kind == 'case':
                case.append(f'{where}:{line_no}: [[{raw}]] only matches "{hit}" if case is ignored')
            elif kind == 'ok' and heading and hit.endswith('.md') and not has_placeholder(heading):
                if hit not in heading_cache:
                    heading_cache[hit] = headings(read(os.path.join(v.root, hit)))
                if norm_heading(heading) not in heading_cache[hit]:
                    broken.append(f'{where}:{line_no}: [[{raw}]]: "{hit}" has no heading "{heading}"')
            if kind == 'ok' and hit and hit.startswith(WIKI + '/'):
                stem = os.path.basename(hit)[:-3]
                if stem in inbound and os.path.basename(where)[:-3] != stem:
                    inbound[stem].add(where)
    orphans = [f'{s}.md' for s, refs in sorted(inbound.items())
               if not refs and f'{s}.md' not in v.system_pages]
    return broken, case, empty, orphans, inbound


def check_index(v):
    out = []
    if 'index.md' not in v.text:
        return [f'{WIKI}/index.md is missing']
    listed, counts = {}, {}
    current = None
    def key(s):
        return re.sub(r'[\s_-]+', ' ', s).strip().lower()
    domain_by_section = {key(d): d for d in v.domains}
    own_sections = {key(s) for s in v.index_sections}
    page_domain = {}
    for p in v.pages:
        fm, _ = frontmatter(v.text[p])
        tags = as_list((fm or {}).get('tags'))
        if tags:
            page_domain[p[:-3]] = tags[0]
    for i, line in enumerate(v.text['index.md'].split('\n'), 1):
        h = re.match(r'^##\s+(.*?)\s*$', line)
        if h:
            current = h.group(1).strip()
            if key(current) not in domain_by_section and key(current) not in own_sections:
                out.append(f'index.md:{i}: section "{current}" is not a declared domain '
                           f'(sections follow the Domains table, or an Index sections table '
                           f'in {v.rules_file})')
            continue
        if not line.lstrip().startswith('- [['):
            continue
        entries = re.findall(r'(?:^|\s)-\s+\[\[([^\]|#]+)', line)
        if len(entries) > 1:
            out.append(f'index.md:{i}: {len(entries)} entries on one line ({", ".join(entries)})')
        name = entries[0].strip() if entries else None
        if not name:
            continue
        if name in listed:
            out.append(f'index.md:{i}: "{name}" is listed again (first at line {listed[name]})')
        listed.setdefault(name, i)
        rest = line.split(']]', 1)[1] if ']]' in line else ''
        desc = re.sub(r'\*\(\d+ sources?\)\*', '', rest).strip().lstrip('—–- ').strip()
        if not re.search(r'\w', desc):
            out.append(f'index.md:{i}: "{name}" has no description')
        elif len(desc) > INDEX_DESC_LIMIT:
            out.append(f'index.md:{i}: "{name}" description is {len(desc)} characters, past {INDEX_DESC_LIMIT}')
        m = re.search(r'\*\((\d+) sources?\)\*', line)
        if m:
            counts[name] = (int(m.group(1)), i)
        dom = page_domain.get(name)
        if current and dom and key(current) in domain_by_section and key(current) != key(dom):
            out.append(f'index.md:{i}: "{name}" is under "{current}" but its domain is "{dom}"')
    pages = {p[:-3] for p in v.pages}
    required = {p[:-3] for p in v.pages if p not in v.system_pages}
    for name, i in sorted(listed.items(), key=lambda x: x[1]):
        if name not in pages:
            out.append(f'index.md:{i}: "{name}" is not a page in {WIKI}/')
    for name in sorted(required - set(listed)):
        out.append(f'"{name}" is not listed in the index')
    for name, (n, i) in sorted(counts.items(), key=lambda x: x[1][1]):
        if name + '.md' in v.text:
            fm, _ = frontmatter(v.text[name + '.md'])
            src = unquote((fm or {}).get('sources'))
            if src.isdigit() and int(src) != n:
                out.append(f'index.md:{i}: "{name}" says {n} sources, the page says {src}')
    return out


# ── rules in the wrong home ───────────────────────────────────────────────

def check_rule_homes(v):
    out = []
    sk = os.path.join(v.root, 'skills')
    for name in sorted(v.skills):
        text = read(os.path.join(sk, name, 'SKILL.md'))
        for i, line in enumerate(text.split('\n'), 1):
            for pat, label in RULE_HOME_PATTERNS:
                for m in pat.finditer(line):
                    if label.startswith('file name'):
                        name_ = m.group(0)
                        # The real rules file, or a known root file, is fine to name.
                        # A name that exists nowhere is likely an old rules file name.
                        if name_ in KNOWN_ROOT_MD or name_ == v.rules_file or os.path.isfile(os.path.join(v.root, name_)):
                            continue
                    out.append(f'skills/{name}/SKILL.md:{i}: {label} "{m.group(0)}"  {line.strip()[:110]}')
                    break
    return out


PATHISH = re.compile(r'`([^`\n]+)`')
OPTIONAL_PATHS = {'skills/lint/tools/extra_checks.py',   # the brain's own checks, made only when needed
                  'skills/lint/tools/test_extra_checks.py'}


def check_root_docs(v):
    out = []
    folder = os.path.basename(v.root.rstrip(os.sep))
    for d in v.root_docs:
        text = read(os.path.join(v.root, d))
        found = set()
        # Backticked paths into the brain's own folders (`wiki/index.md`).
        for m in PATHISH.finditer(text):
            if m.group(1).split('/')[0] in TOP_DIRS:
                found.add(m.group(1))
        # Paths in the directory diagram, rebuilt from their indentation.
        stack = []
        for m in re.finditer(r'^([│ ]*)[├└]──\s+(.+?)(?:\s{2,}|\s*←|$)', text, re.M):
            depth = len(m.group(1)) // 4
            stack = stack[:depth] + [m.group(2).strip()]
            found.add('/'.join(s.rstrip('/') for s in stack) + ('/' if m.group(2).strip().endswith('/') else ''))
        for p in sorted(found):
            if re.search(r'[<>{}*$]|YYYY|\.\.\.|…|^https?:|^~|^/|^\.\.?/|\\|\s', p):
                continue                               # templates, globs, URLs, machine paths, prose
            rel = p.strip().rstrip('/')
            if rel.startswith(folder + '/'):
                rel = rel[len(folder) + 1:]
            if not rel or rel == folder or rel in OPTIONAL_PATHS:
                continue
            if not os.path.exists(os.path.join(v.root, rel)):
                out.append(f'{d}: names `{p}`, which does not exist in the brain')
    return out


# ── Vault Map ─────────────────────────────────────────────────────────────

PREFIX = re.compile(r'^(.+?) — ')
WILDCARD = re.compile(r'<[^<>]+>|…|\.\.\.')


def map_patterns(text):
    """Name patterns the map writes in backticks inside its tables: `Ideas — <title>`,
    `People —`, `<Topic> — <subtitle> (<Author>)`. <...> and … are wildcards. Only
    table rows count, and a pattern must hold the ` — ` separator, so a word in
    backticks (`log`) never covers a page name."""
    pats = []
    rows = '\n'.join(l for l in strip_code_blocks(text).split('\n') if l.lstrip().startswith('|'))
    for m in PATHISH.finditer(rows):
        raw = m.group(1).strip()
        if '—' not in raw:
            # A full page name with no separator (`LLM Wiki Method`) covers that
            # exact page only, so a bare word like `log` never covers a prefix.
            if not WILDCARD.search(raw) and re.search(r'\w', raw):
                pats.append(re.compile('^' + re.escape(raw) + '$'))
            continue
        parts = WILDCARD.split(raw)
        rx = '.+'.join(re.escape(x) for x in parts)
        pats.append(re.compile('^' + rx))
    return pats


def check_map(v):
    if MAP_FILE not in v.text:
        return [f'{WIKI}/{MAP_FILE} is missing: nothing tells a session where pages go']
    text = v.text[MAP_FILE]
    pats = map_patterns(text)
    out, uncovered = [], {}
    for p in v.pages:
        if p in v.system_pages or p == MAP_FILE:
            continue
        stem = p[:-3]
        m = PREFIX.match(stem)
        if not m:
            fm, _ = frontmatter(v.text[p])
            tags = as_list((fm or {}).get('tags'))
            if not (tags and tags[0] == 'system'):
                if not any(rx.match(stem) for rx in pats):
                    out.append(f'{p}: a content page with no prefix. Give it one, or list it by '
                               f'its exact name in a {MAP_FILE} table to keep it unprefixed')
            continue
        if any(rx.match(stem) for rx in pats):
            continue
        uncovered.setdefault(m.group(1) + ' —', []).append(stem)
    for prefix, stems in sorted(uncovered.items(), key=lambda x: (-len(x[1]), x[0])):
        n = len(stems)
        out.append(f'prefix "{prefix}" ({n} page{"s" if n > 1 else ""}, e.g. {stems[0]}) is not in {MAP_FILE}')
    tdir = os.path.join(v.root, 'templates')
    if os.path.isdir(tdir):
        for f in sorted(os.listdir(tdir)):
            if f.endswith('.md') and f[:-3] not in text:
                out.append(f'templates/{f} is not in the {MAP_FILE} page-type table')
    return out


def hub_threshold(v):
    """At least HUB_MIN distinct linking pages, rising with the brain's size so a
    large brain doesn't call half its pages hubs."""
    return max(HUB_MIN, round(len(v.pages) * 0.05))


def check_hubs(v, inbound):
    if MAP_FILE not in v.text:
        return []
    sec = section(v.text[MAP_FILE], r'^Hub') or ''
    listed = {t for _, _, t, _ in links_in(sec) if t}
    skip = {p[:-3] for p in v.system_pages} | {MAP_FILE[:-3]}
    ignore_linkers = {f'{WIKI}/{p}' for p in v.system_pages | {MAP_FILE}}
    out, candidates = [], []
    hub_min = hub_threshold(v)
    for stem, refs in sorted(inbound.items(), key=lambda x: (-len(x[1]), x[0])):
        n = len(refs - ignore_linkers - set(v.root_docs))
        if stem in skip:
            continue
        if n >= hub_min and stem not in listed:
            candidates.append(f'{stem}: {n} distinct pages link here. Not in the map\'s hub list')
    out += candidates[:HUB_SHOW]
    if len(candidates) > HUB_SHOW:
        out.append(f'...and {len(candidates) - HUB_SHOW} more pages above the threshold of {hub_min}')
    for stem in sorted(listed):
        if stem in inbound:
            n = len(inbound[stem] - ignore_linkers - set(v.root_docs))
            if n < HUB_QUIET:
                out.append(f'{stem}: listed as a hub, but only {n} distinct page(s) link to it')
        elif not has_placeholder(stem):
            out.append(f'{stem}: listed as a hub, but it is not a page in {WIKI}/')
    return out


# ── main ──────────────────────────────────────────────────────────────────

def main(argv=None):
    try:
        sys.stdout.reconfigure(errors='replace')
    except (AttributeError, ValueError):
        pass
    ap = argparse.ArgumentParser(description='Mechanical checks for an LLM Wiki brain. Reports, never changes.')
    ap.add_argument('--vault', default=DEFAULT_VAULT)
    ap.add_argument('--today', help='YYYY-MM-DD, for the stalled-draft check (default: today)')
    ap.add_argument('--wiki', help='name of the pages folder, if it is not "wiki" (for a check before a migration)')
    ap.add_argument('--rules', help='rules file to read, for a brain that has no `llm-wiki: rules` marker yet')
    a = ap.parse_args(argv)
    global WIKI
    WIKI = a.wiki.strip('/') if a.wiki else 'wiki'

    if a.today and not is_date(a.today):
        print(f'vault_check: --today "{a.today}" is not a YYYY-MM-DD date', file=sys.stderr)
        return 2

    root = os.path.abspath(a.vault)
    try:
        if a.rules:
            rules = [a.rules] if os.path.isfile(os.path.join(root, a.rules)) else []
        else:
            rules = find_rules_files(root) if os.path.isdir(root) else []
    except OSError as e:
        print(f'vault_check: could not read {root}: {e}', file=sys.stderr)
        return 2
    if not rules or not os.path.isfile(os.path.join(root, WIKI, 'index.md')):
        print(f'vault_check: {root} is not an LLM Wiki brain (needs a root rules file with '
              f'`llm-wiki: rules` in its frontmatter, and {WIKI}/index.md)', file=sys.stderr)
        return 2
    if len(rules) > 1:
        print(f'vault_check: more than one rules file ({", ".join(rules)}). Keep one, '
              f'and remove `llm-wiki: rules` from the others.', file=sys.stderr)
        return 2
    try:
        today = dt.date.fromisoformat(a.today) if a.today else dt.date.today()
        v = Vault(root, rules[0])
        setup = check_setup(v)
        pointers = v.rule_findings + check_pointers(v)
        fm, stalled = check_frontmatter(v, today)
        names = check_filenames(v)
        broken, case, empty, orphans, inbound = check_links(v)
        index = check_index(v)
        homes = check_rule_homes(v)
        roots = check_root_docs(v)
        vmap = check_map(v)
        hubs = check_hubs(v, inbound)
        items = check_open_items(v)
    except (OSError, ValueError) as e:
        print(f'vault_check: could not read the brain: {e}', file=sys.stderr)
        return 2

    sections = [
        ('Setup leftovers', setup),
        ('Rules file, adapters and skill names', pointers),
        ('Frontmatter', fm),
        ('Filenames', names),
        ('Broken links', broken),
        ('Link case mismatches', case),
        ('Empty links', empty),
        ('Index', index),
        ('Orphans (no inbound link from a page or the index; log.md does not count)', orphans),
        ('Stalled drafts (draft or developing, 30+ days)', stalled),
        ('Rule homes (skills carrying what the rules file or an adapter should own; judge each)', homes),
        ('Root docs naming paths that do not exist', roots),
        ('Vault Map drift (judge each)', vmap),
        (f'Hubs (pages {hub_threshold(v)}+ distinct pages link to, and quiet listed hubs; judge each)', hubs),
        ('Open items (checked items to move, or an archive pass due)', items),
    ]
    total = sum(len(items) for _, items in sections)
    name = v.brain if v.brain and not has_placeholder(v.brain) else '(not set up yet)'
    print(f'Vault check for {name}: rules file {v.rules_file}, {len(v.pages)} wiki pages, '
          f'{len(v.skill_links) if v.skills_mode == "installed" else len(v.skills)} skills'
          f'{" (installed)" if v.skills_mode == "installed" else ""}, template {v.template_version or "?"}, as of {today}. '
          f'Report only, nothing changed.')
    for title, items in sections:
        print(f'\n{title}: {len(items) if items else "none"}')
        for i in items:
            print(f'  - {i}')
    print(f'\n{total} findings. Each is a candidate for the lint report, not a verdict.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
