# Connect a chatbot

Use ARD directly from a chatbot to **find tools, skills, MCP servers, and agents
for a task** — and decide what to install. The
[connectors](https://github.com/ards-project/connectors) repository provides
ready-made setups for **Claude, ChatGPT, GitHub Copilot, Microsoft Copilot, and
Gemini**.

The connectors are **client-side only**. A discovery service — such as GitHub's
**[Agent Finder](https://github.com/agentfinder)** or **[Hugging Face
Discover](https://github.com/huggingface/hf-discover)** — exposes the search
interface; the connector just points your chatbot at an endpoint you choose.
Nothing is installed automatically.

## What these connectors do

Once connected, ask your chatbot to find a capability for a task. These
ready-made connectors will:

1. **Ask which Agent Finder endpoint** to search (you stay in control of where
   results come from).
2. **Query** it.
3. **Present a ranked list** of matching resources — name, type, description,
   publisher, endpoint, and relevance score (relevance only, *not* a trust or
   safety rating).
4. **Never auto-install.** Only after you pick a result does it show you how to
   add that resource yourself.

**GitHub Copilot is the exception.** Its skill defaults to GitHub's Agent Finder,
so it skips step 1 and searches GitHub directly. The other four ask which finder
to use.

### This is one design among several

That flow is a deliberate choice — the most conservative one — **not** something
ARD requires. ARD is just the discovery layer underneath; a connector can sit
anywhere on a spectrum of autonomy:

- **(a) Find on request, then install on approval** — *what these connectors do.*
  You ask it to find tools, it presents matches, and you choose what to install.
  A human is in the loop at both ends.
- **(b) Auto-discover, then install on approval** — the chatbot decides on its
  own to query an Agent Finder when it hits a missing capability mid-task, but
  still asks before installing anything.
- **(c) Auto-discover and auto-install** — the chatbot queries *and* installs
  without prompting. The most autonomous; appropriate only with a trusted,
  curated finder and a sandboxed environment.

These connectors ship as **(a)** for maximum user control, but you can build your
own at any of these levels.

## Two ways to connect

| Method | What it is | Best when |
| --- | --- | --- |
| **Skill** | A portable instruction bundle — a Claude Skill, ChatGPT Skill, Gemini Gem, or Copilot agent — that drives the flow over the HTTP `POST /search` interface. | Quickest start; works wherever the assistant can make an HTTP / Action call. |
| **MCP** | Add Agent Finder as a **remote MCP connector** so the chatbot gets a native `search` tool. | You want a first-class tool and your client supports MCP connectors. |

Most setups use **both**: the MCP connector (or an Action) makes the actual call,
and the Skill/instructions supply the "ask first, present, never auto-install"
behavior.

How you add the Skill itself differs by client, and there is rarely a single
"install" button:

- **Claude and GitHub Copilot** — a `SKILL.md` file you drop into a skills folder (`~/.claude/skills/`, `~/.copilot/skills/`), or install with a command.
- **ChatGPT** — a Skill you add in the workspace UI (Business / Enterprise / Edu / Team plans).
- **Gemini** — a Gem you create in the Gemini app.
- **Microsoft Copilot** — an agent you build in Copilot Studio.

Each page below says exactly where it goes.

## Pick your platform

Each page has the full install steps **and** how to invoke it, for both the Skill
and the MCP connector:

- **[Claude](connect/claude.md)** — Skill (Claude Code plugin) + remote MCP connector
- **[ChatGPT](connect/chatgpt.md)** — Skill (beta) + remote MCP (Developer mode)
- **[GitHub Copilot](connect/github-copilot.md)** — Agent Skill (`SKILL.md`) + remote MCP (VS Code `mcp.json`)
- **[Microsoft Copilot](connect/microsoft-copilot.md)** — declarative agent + remote MCP (Copilot Studio)
- **[Gemini](connect/gemini.md)** — Gem + remote MCP (Gemini CLI)

## Endpoints

Most connectors have **no built-in default** Agent Finder — you choose which
discovery services to trust, and they ask which to query (keep a list in
`agent-finders.json`). **GitHub Copilot is the exception:** its skill defaults to
GitHub's Agent Finder. The per-platform examples use two real discovery services
interchangeably:

| Discovery service | Search endpoint |
| --- | --- |
| GitHub Agent Finder | `https://agentfinder.github.com/api/v1/search` |
| Hugging Face Discover | `https://huggingface-hf-discover.hf.space/search` |

Point at either of these — or any compliant ARD discovery service — when a step
asks for an endpoint. The connector never queries an endpoint you didn't choose.
