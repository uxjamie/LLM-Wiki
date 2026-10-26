#!/usr/bin/env python3
"""Archive check: proves an archive pass on open-items lost nothing.

This file belongs to the LLM Wiki template. Template updates replace it whole,
so a brain's own checks go in extra_checks.py, never in here.

    python3 -B skills/lint/tools/archive_check.py <snapshot>                 # from the brain's root
    python3 -B skills/lint/tools/archive_check.py <snapshot> --vault <path>  # anywhere else

Take the snapshot (a copy of wiki/open-items.md) before the pass. Afterward this
checks that every non-blank line of the snapshot appears, word for word, as a line
in wiki/open-items.md or wiki/open-items-archive.md. The snapshot's frontmatter is
skipped, because the live file's dates change. It reports and changes nothing.

Exit status: 0 = nothing lost. 1 = lines missing (listed). 2 = could not read.
"""
import argparse
import os
import re
import sys

sys.dont_write_bytecode = True

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_VAULT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
WIKI = 'wiki'


def read(path):
    with open(path, encoding='utf-8', errors='replace') as f:
        return f.read()


def body_lines(text):
    m = re.match(r'﻿?---\r?\n.*?\r?\n---\r?\n?', text, re.S)
    if m:
        text = text[m.end():]
    return [line.rstrip() for line in text.splitlines() if line.strip()]


def missing(snapshot, live, archive):
    have = {line.rstrip() for line in (live + '\n' + archive).splitlines()}
    return [line for line in body_lines(snapshot) if line not in have]


def main(argv=None):
    ap = argparse.ArgumentParser(description='Prove an open-items archive pass lost nothing. Reports, never changes.')
    ap.add_argument('snapshot', help='copy of wiki/open-items.md taken before the pass')
    ap.add_argument('--vault', default=DEFAULT_VAULT)
    a = ap.parse_args(argv)
    try:
        snap = read(a.snapshot)
        live = read(os.path.join(a.vault, WIKI, 'open-items.md'))
        arch = read(os.path.join(a.vault, WIKI, 'open-items-archive.md'))
    except OSError as e:
        print(f'archive_check: could not read: {e}', file=sys.stderr)
        return 2
    lost = missing(snap, live, arch)
    total = len(body_lines(snap))
    if lost:
        print(f'{len(lost)} of {total} snapshot lines are in neither open-items nor its archive:')
        for line in lost:
            print(f'  - {line[:160]}')
        return 1
    print(f'Nothing lost: all {total} snapshot lines are in open-items or its archive, word for word.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
