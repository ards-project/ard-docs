# Connect a chatbot

You can use ARD directly from a chatbot to **find tools, skills, MCP servers, and
agents for a task** — and decide what to install. The
[ards-project/connectors](https://github.com/ards-project/connectors) repository
provides ready-made connectors for **Claude, ChatGPT, Microsoft Copilot, and
Gemini**.

The connectors are **client-side only**. A discovery service such as **Agent
Finder** exposes the search interface; the connector just points your chatbot at
an endpoint you choose. Nothing is installed automatically.

## What it does

Once connected, ask your chatbot to find a capability for a task. It will:

1. **Ask which Agent Finder endpoint(s)** to search (you stay in control of where
   results come from).
2. **Query** those endpoints.
3. **Present a ranked list** of matching resources — name, type, description,
   publisher, endpoint, and relevance score (relevance only, *not* a trust or
   safety rating).
4. **Never auto-install.** Only after you pick a result does it show you how to
   add that resource yourself.

## Two ways to connect

- **Skill** — a portable instruction bundle that drives the flow over the HTTP
  `POST /search` interface. Best for the quickest start.
- **MCP** — add an Agent Finder **remote MCP** connector so the chatbot gets a
  native search tool, paired with the Skill for the behavior above.

On **Claude Code**, the skill installs in two commands (the connectors repo is a
plugin marketplace):

```
/plugin marketplace add ards-project/connectors
/plugin install find-agentic-resources@ard-connectors
```

## Per-platform setup

Pick your platform; each links to the exact files and steps.

| Platform | Skill | MCP connector | Notes |
| --- | --- | --- | --- |
| **Claude** | [skill](https://github.com/ards-project/connectors/tree/main/skills/find-agentic-resources) | [remote MCP](https://github.com/ards-project/connectors/tree/main/mcp/claude) | Native remote connectors across claude.ai, Desktop, mobile |
| **ChatGPT** | [skill](https://github.com/ards-project/connectors/tree/main/skills/chatgpt) | [remote MCP](https://github.com/ards-project/connectors/tree/main/mcp/chatgpt) | Skills + Developer-mode MCP are plan-gated |
| **Microsoft Copilot** | [agent instructions](https://github.com/ards-project/connectors/tree/main/skills/copilot) | [remote MCP](https://github.com/ards-project/connectors/tree/main/mcp/copilot) | Copilot Studio / M365 Copilot or GitHub Copilot |
| **Gemini** | [gem](https://github.com/ards-project/connectors/tree/main/skills/gemini) | [remote MCP](https://github.com/ards-project/connectors/tree/main/mcp/gemini) | MCP via Gemini CLI / API; the consumer app has neither |

## Endpoints

There is **no built-in default** Agent Finder. You choose which discovery services
to trust by editing the connector's `agent-finders.json` — a list of endpoints it
presents and asks you to pick from. The shipped entries are placeholders; replace
them with discovery services you trust. The connector never queries an endpoint
you didn't choose.

See the [connectors repository](https://github.com/ards-project/connectors) for
the full instructions and the shared interaction contract.
