#!/usr/bin/env python3
"""Tests for archive_check.py. Run: python3 -B test_archive_check.py"""
import io
import os
import shutil
import sys
import tempfile
from contextlib import redirect_stderr, redirect_stdout

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import archive_check as ac                       # noqa: E402

fails, passed = [], 0


def ok(name, cond, detail=''):
    global passed
    if cond:
        passed += 1
    else:
        fails.append(f'{name}: {detail}')


SNAP = ('---\ntitle: "Open Items"\ndate_updated: 2026-10-01\n---\n\n# Open Items\n\n'
        '- [ ] **Long item.** Many words of history.\n  - a sub-bullet\n\n## Decisions log\n\n'
        '- 2026-09-01: an old decision, in full.\n')
LIVE = ('---\ntitle: "Open Items"\ndate_updated: 2026-10-20\n---\n\n# Open Items\n\n'
        '- [ ] **Long item.** Track. Next: wait for the reply.\n\n## Decisions log\n')
ARCH = ('# Open Items Archive\n\n## Live items, full text before the trim (2026-10-20)\n\n'
        '- [ ] **Long item.** Many words of history.\n  - a sub-bullet\n\n'
        '- 2026-09-01: an old decision, in full.\n')

ok('a complete pass loses nothing', ac.missing(SNAP, LIVE, ARCH) == [], ac.missing(SNAP, LIVE, ARCH))
lost = ac.missing(SNAP, LIVE, ARCH.replace('  - a sub-bullet\n', ''))
ok('a dropped line is reported', lost == ['  - a sub-bullet'], lost)
ok('a changed live date is not a loss', 'date_updated: 2026-10-01' not in ac.missing(SNAP, LIVE, ARCH))
ok('trailing spaces do not count as a change', ac.missing(SNAP.replace('history.', 'history.  '), LIVE, ARCH) == [])
reworded = ac.missing(SNAP, LIVE, ARCH.replace('Many words', 'Several words'))
ok('a reworded line is reported', len(reworded) == 1 and 'Many words' in reworded[0], reworded)


def run(argv):
    with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
        return ac.main(argv)


root = tempfile.mkdtemp(prefix='llmwiki-archive-')
try:
    os.makedirs(os.path.join(root, 'wiki'))
    snap = os.path.join(root, 'snap.md')
    for name, text in (('snap.md', SNAP), ('wiki/open-items.md', LIVE), ('wiki/open-items-archive.md', ARCH)):
        with open(os.path.join(root, name), 'w', encoding='utf-8') as f:
            f.write(text)
    ok('exit 0 when nothing is lost', run([snap, '--vault', root]) == 0)
    with open(os.path.join(root, 'wiki/open-items-archive.md'), 'w', encoding='utf-8') as f:
        f.write('# Open Items Archive\n')
    ok('exit 1 when lines are missing', run([snap, '--vault', root]) == 1)
    ok('exit 2 when the snapshot is missing', run([os.path.join(root, 'nope.md'), '--vault', root]) == 2)
finally:
    shutil.rmtree(root)

if fails:
    print(f'{len(fails)} FAILED, {passed} passed')
    for f in fails:
        print('  FAIL', f)
    sys.exit(1)
print(f'all {passed} checks passed')
