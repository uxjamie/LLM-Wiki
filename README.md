# LLM Wiki

A ready-made starting point for a personal knowledge base your AI assistant writes and keeps up to date for you.

You collect things worth knowing: articles, notes, meeting transcripts, documents, ideas. You hand them to your AI. The AI reads each one, writes short, tidy pages that summarize it, links those pages to what you already have, and keeps everything current as you add more. Over time you build a personal wiki you can question, and it grows more useful with every item you add.

You decide what goes in. The AI does the rest.

People use a brain like this for a research topic, a design system, how their team works, a new job, a side business, or their own career. Setup asks what yours is for and shapes it to fit.

## It lives on your computer

Your brain is an ordinary folder of plain text files on your computer. You can open any page in a text editor and read it.

- **Nothing to install.** The AI's instructions are text files inside the folder, and the AI reads them when it starts work.
- **Nothing runs online by itself.** This template contains no app and no service. Your AI tool reads and writes the files while you work with it, the same way it reads anything else you share with it.
- **You own every file.** Copy it, back it up, or move it like any other folder.

## What you need

- **An AI tool that works inside a folder on your computer.** It needs to read and write the files there. Examples:
  - the Claude desktop app, working in a folder you choose
  - Claude Code
  - Codex, or another AI agent that works with local files

  A chat window without access to your files won't work.
- **About 10 minutes** for setup.

These are optional. Setup asks about each one.

- **Obsidian**, a free app for reading and browsing the brain, with clickable links and a map of how pages connect.
- **Python 3**, for a built-in health check. Without it, the AI does the same checks by reading.
- **git**, a tool that keeps a history of every change so you can go back. If you don't know it, skip it. The brain keeps its own log of changes either way.

## Get started

1. **Download it.** On this page, click the green **Code** button, then **Download ZIP**. (If you use GitHub, **Use this template** makes your own copy instead.)
2. **Unzip it and put the folder where you keep your documents.** Rename the folder to anything you like.
3. **Open the folder in your AI tool.**
   - **Claude desktop app:** start a task and choose this folder as the place to work, or create a project from the folder. The app's buttons change from time to time, so look for the option to pick a folder.
   - **Claude Code:** open a terminal in the folder and run `claude`.
   - **Other AI tools:** open the folder as your workspace.
4. **Type:** `Run SETUP.md`
5. **Answer a few questions.** The AI asks what to call your brain, what it's for, and how you'd like pages grouped. Then it shows you the plan and waits for your yes before changing anything.
6. **Add your first item.** Drop a file into the `raw` folder, or paste some text into the chat, and say "ingest this."

## Already have a brain?

If you built a wiki from Karpathy's idea file, or set one up some other way, you can bring it up to this template without starting over. Open your existing brain in your AI tool and type:

> Follow the migration guide at https://github.com/uxjamie/LLM-Wiki/blob/main/MIGRATE.md

Your AI looks through your brain first and changes nothing. It shows you one plan that keeps your own way of doing things wherever it works, makes a full backup copy, and then makes the changes in three steps you approve. Your pages, sources, and decisions stay.

## Everyday use

You talk to your AI in plain words. These phrases work, and so do your own versions of them.

| You say | What happens |
|---|---|
| "ingest this", "save this", "file this" | The AI saves the original, writes or updates the pages it touches, and links them up. |
| Any question | The AI looks through your pages and answers, pointing to where each answer came from. A good answer gets saved as a page. |
| "lint" or "health check" | The AI checks the brain for broken links, outdated facts, and gaps, points out pages that should be connected, then suggests fixes and waits for your yes. Every couple of weeks is plenty. Setup can schedule it to run on its own; you still approve every fix. |
| "share this" | The AI makes a clean copy of a page for someone who doesn't have your brain, with private details removed. |
| "check for template updates" | The AI looks here for improvements to this template and offers to add them to your brain. |

## What's in the folder

| Name | What it is |
|---|---|
| `raw/` | Your originals: the files and notes you add. The AI reads them and never changes them. |
| `wiki/` | The pages the AI writes, plus a few it keeps for itself (more below). |
| `outputs/` | Finished things the AI makes for you, like a report or a shareable copy of a page. |
| `skills/` | Step-by-step instructions the AI follows for adding items, health checks, and sharing. |
| `templates/` | Starting shapes for common pages: a person, a meeting, a project, an idea, a summary of an article. |
| `BRAIN.md` | The rules for your brain. Setup renames it after your brain, for example `ATLAS.md`. |
| `CLAUDE.md`, `AGENTS.md` | Short notes AI tools read when they start. They point to the rules and list when to use each skill. `CLAUDE.md` is for Claude, `AGENTS.md` for other tools. |
| `SETUP.md` | The setup interview for a new brain. Filed away once setup is done. |
| `MIGRATE.md` | The guide for bringing an existing brain up to this template. A new brain doesn't need it. |
| `scripts/` | An optional helper for people who use git. |
| `.obsidian/` | Ready-made settings for Obsidian. A hidden folder. Ignore it if you don't use Obsidian. |

The AI keeps five pages in `wiki/` for itself:

- **index:** a list of every page, one line each.
- **log:** a running record of every change and why.
- **open-items:** decisions you've made and work still to do, so nothing gets lost between sessions.
- **open-items-archive:** where finished items go the moment they're done, so open-items stays short and cheap to read every session.
- **Vault Map:** a guide to how the brain is organized and where new pages go.

## How this extends Karpathy's idea

This template is built on Andrej Karpathy's [LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f), a short document he calls an "idea file": you paste it into your AI, and the two of you build the details together. It describes the pattern and, in his words, is "intentionally abstract." This template keeps his whole pattern and adds the details that months of running brains this way every day showed were needed.

### What comes from Karpathy

These parts of the template are his idea, used as he describes them:

- **Your sources** kept as originals the AI reads but never changes (the `raw` folder).
- **A wiki** of pages the AI writes and keeps up to date (the `wiki` folder).
- **An instructions file** that tells the AI how the brain works (`CLAUDE.md` and `AGENTS.md`).
- **Three everyday jobs:** add a source, ask a question, run a health check.
- **An index** listing every page, and **a log** of every change.
- **Obsidian** as an optional way to read and browse it all.

### What this template adds

**New** means Karpathy's idea file doesn't cover it. **Expanded** means Karpathy's idea file mentions it, and this template builds it out.

| Addition | New or expanded | What it gives you |
|---|---|---|
| Setup interview | New | The AI asks what your brain is for, names it, builds it, and checks its own work. You never edit a configuration file. |
| Page templates | New | Starting shapes for common pages (a person, a meeting, a project, an idea, a summary of an article), so similar pages look alike and nothing important gets left out. |
| A map of the brain | New | A guide to how the brain is organized and where each new page goes: one naming pattern for every kind of page, and groups that sort pages by what kind they are. |
| Page details | Expanded | Karpathy's idea file suggests the AI could add details like tags and dates to the top of each page. Here every page carries the same set of details, each with a defined meaning: what kind of page it is, how finished it is, who it can be shared with, the people and project it involves, and how many sources back it. |
| Step-by-step skills | Expanded | Karpathy's idea file describes the three everyday jobs. Here each one is written out as instructions the AI follows the same way every time, plus a fourth job: making a clean, shareable copy of a page for someone else. |
| Stronger trust | Expanded | Karpathy's idea file asks for answers with citations and for health checks to spot contradictions. Here every number, quote, and claim about other people records where it came from and how sure the brain is, and when two sources disagree, both sides are kept and flagged for you. |
| Decisions remembered | New | A running list of your decisions and open work, so a choice you made last week still holds and nothing gets dropped between sessions. |
| Built-in checker | New | A small script that checks the whole brain for broken links, missing page details, missing index entries, and inconsistent names. It reports and never changes anything on its own. |
| Template updates | New | Say "check for template updates" and the AI offers improvements made to this template since you set up. |

Some of the problems behind these additions:

- Two reports with different numbers got blended into one wrong number.
- A person page was nearly written for someone who didn't exist, because a transcript misheard a name twice.
- One page name was spelled two ways, so some links to it broke without anyone noticing.
- Decisions made in one session were forgotten by the next.
- Pages were tagged with the brain's own subject, which sorted nothing.

## Viewing in Obsidian

Optional. Obsidian is a free app that shows your brain with clickable links, a graph of how pages connect, and a list of what links to each page.

1. Install Obsidian from [obsidian.md](https://obsidian.md). Choose **Open folder as vault** and pick your brain's folder. The included settings are already pointed at the right folders.
2. Optional: install the **Dataview** plugin from Obsidian's community plugins. It turns `wiki/queries.md` into live tables: open items, recent changes, pages that need attention.

You can edit pages in Obsidian yourself. Mention it to your AI next time, so it can note the change and check the links.

## Words you'll see

- **Markdown:** the plain text format the pages are written in. A `#` at the start of a line makes a heading.
- **Link:** text in double square brackets, like `[[People — Ada Lovelace]]`, points to another page.
- **Source:** anything you add for the brain to learn from.
- **Ingest:** add a source, and have the AI file it into pages.
- **Lint:** a health check of the whole brain.

## Questions

**Do I need to know how to code?** No. You talk to the AI in plain words. The AI handles the files.

**Can I have more than one brain?** Yes. Download another copy for each topic. If you want them to work together, ask your AI to help you set that up.

**What if I change my mind about a setup answer?** Tell your AI. It updates the rules and records the decision.

**Where do my files go?** They stay in the folder on your computer. Your AI tool reads them while you work together, under that tool's own privacy terms, the same as anything else you share with it.

## Credits

Based on Andrej Karpathy's [LLM Wiki idea file](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f). Built by [Jamie Hall](https://github.com/uxjamie).

## License

[MIT](LICENSE). Free to use and adapt.
