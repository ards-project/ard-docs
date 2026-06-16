# Connect a chatbot

Use ARD directly from a chatbot to **find tools, skills, MCP servers, and agents
for a task** — and decide what to install. The
[connectors](https://github.com/ards-project/connectors) repository provides
ready-made setups for **Claude, ChatGPT, Microsoft Copilot, and Gemini**.

The connectors are **client-side only**. A discovery service such as
**[Agent Finder](https://github.com/agentfinder)** exposes the search interface;
the connector just points your chatbot at an endpoint you choose. Nothing is
installed automatically.

## What it does

Once connected, ask your chatbot to find a capability for a task. It will:

1. **Ask which Agent Finder endpoint** to search (you stay in control of where
   results come from).
2. **Query** it.
3. **Present a ranked list** of matching resources — name, type, description,
   publisher, endpoint, and relevance score (relevance only, *not* a trust or
   safety rating).
4. **Never auto-install.** Only after you pick a result does it show you how to
   add that resource yourself.

## Two ways to connect

| Method | What it is | Best when |
| --- | --- | --- |
| **Skill** | A portable instruction bundle — a Claude Skill, ChatGPT Skill, Gemini Gem, or Copilot agent — that drives the flow over the HTTP `POST /search` interface. | Quickest start; works wherever the assistant can make an HTTP / Action call. |
| **MCP** | Add Agent Finder as a **remote MCP connector** so the chatbot gets a native `search` tool. | You want a first-class tool and your client supports MCP connectors. |

Most setups use **both**: the MCP connector (or an Action) makes the actual call,
and the Skill/instructions supply the "ask first, present, never auto-install"
behavior.

## Pick your platform

Each page has the full install steps **and** how to invoke it, for both the Skill
and the MCP connector:

- **[Claude](connect/claude.md)** — Skill (Claude Code plugin) + remote MCP connector
- **[ChatGPT](connect/chatgpt.md)** — Skill (beta) + remote MCP (Developer mode)
- **[Microsoft Copilot](connect/copilot.md)** — agent instructions + remote MCP (Copilot Studio / VS Code)
- **[Gemini](connect/gemini.md)** — Gem + remote MCP (Gemini CLI)

## Endpoints

There is **no built-in default** Agent Finder — you choose which discovery
services to trust. The connector asks which to query, and you can keep a list in
its `agent-finders.json`. The per-platform examples use two real discovery
services interchangeably:

| Discovery service | Search endpoint |
| --- | --- |
| GitHub Agent Finder | `agentfinder.github.com` |
| Hugging Face Discover | `https://evalstate-hf-discover.hf.space/search` |

Point at either of these — or any compliant ARD discovery service — when a step
asks for an endpoint. The connector never queries an endpoint you didn't choose.
