---
name: courier
description: Produce a self-contained, sanitized copy of a {{BRAIN_NAME}} page for someone outside the brain. Applies only when working inside the {{BRAIN_NAME}} folder, an LLM Wiki brain. Use on "share this", "make this shareable", "sanitize this", "send this to the team", or when the owner wants to hand brain material to someone who doesn't have the brain. Summarizes every linked page inline so the copy stands alone, strips private detail to the audience tier, holds the trust layer, and writes to outputs/shared/, never changing the original or raw/.
---

# Courier

Turn one wiki page into something a person without the brain can read. Wiki pages are full of `[[links]]` that won't resolve outside the brain, and private context that shouldn't leave it. Courier handles both. It **collates** (summarizes linked pages inline) and **sanitizes** (removes or flags private detail) for the audience the owner names.

## Guard, first, always

Confirm you are inside the {{BRAIN_NAME}} brain: the folder's root holds the rules file (the file `CLAUDE.md` and `AGENTS.md` tell you to read first), its frontmatter carries `llm-wiki: rules` and `brain: "{{BRAIN_NAME}}"`, and `wiki/index.md` exists. If not, say this skill belongs to the {{BRAIN_NAME}} brain and stop. Courier reads `wiki/` and writes only to `outputs/shared/`. It never changes the original page or anything in `raw/`.

## Procedure

1. **Target and audience.** Identify the page to share and the audience tier from the rules file's Audiences table. If the tier is unclear, ask once. It sets how much to strip and which voice to write in.
2. **Collate.** Read the page. For every `[[wikilink]]` in the body, add a two-to-four-sentence summary of the linked page so the reader loses nothing essential. Summaries, not full pages. Replace each live link with the plain title. Note which pages were collated.
3. **Sanitize** to the tier. Remove or flag: private detail about people (people pages hold the owner's candid read and never leave the brain), pages about the owner, internal-only context, financial and confidential figures, anything marked `confidential`, `internal`, `needs-review`, or do-not-share, and unresolved conflicts. For a wider tier, also lift the prose to plain language: spell out acronyms, drop internal codes and trust labels from the text. If the owner has a working-style page, follow it for voice.
4. **Hold the trust layer.** Never export a Hypothesis as fact. Keep its hedge or soften the claim. Drop or flag any third-party or quantitative claim not traceable to a source in the brain.
5. **Write the copy** to `outputs/shared/<slug>-WIP.md`, following the output lifecycle in the rules file. Open it with one line naming the audience tier and the date. The original stays untouched. When the copy goes out, rename it `-SHARED-YYYY-MM-DD` and record where it went.
6. **Report.** One short summary: which pages were collated, what was removed or flagged, the tier, and where the copy landed. Name anything you removed that the owner might want to keep.

## Reminders

- The original never changes. Courier only writes a fresh copy.
- Summaries of linked pages, not full pages: self-contained but lean.
- When in doubt, flag rather than cut silently, and say so.
- The full rules are in the rules file.
