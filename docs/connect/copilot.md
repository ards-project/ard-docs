# Connect Microsoft Copilot

Copilot doesn't use "Skills" by that name — the equivalent is a **declarative
agent** (Microsoft 365 Copilot / Copilot Studio) or **custom instructions**
(GitHub Copilot). Either way you add Agent Finder as a **remote MCP** tool and
give the agent the "ask first, never auto-install" instructions.

## Option A — Agent instructions

**Install.** Create (or open) your agent and paste the instructions from the
connectors repo
([`skills/copilot/`](https://github.com/ards-project/connectors/tree/main/skills/copilot)):

- **Microsoft 365 Copilot / Copilot Studio** — add them as the agent's
  instructions.
- **GitHub Copilot** — add them as repository custom instructions
  (`.github/copilot-instructions.md`).

The instructions tell Copilot to ask which Agent Finder to query, present the
ranked results, and never install anything automatically. Pair them with the MCP
tool below so Copilot can actually make the call.

### How to invoke it

Ask Copilot in plain language — e.g. *"Find me an agent that can triage GitHub
issues."* It asks which Agent Finder to search, queries it, and lists the matches.

## Option B — Remote MCP connector

> **Default endpoint:** GitHub's Agent Finder at `http://agentfinder.github.com`.
> Replace it to use a different discovery service.

**Microsoft 365 Copilot / Copilot Studio**

1. In **Copilot Studio**, open your agent → **Tools → Add a tool → Model Context
   Protocol**.
2. Add a **custom connector** using the **Streamable** MCP transport and the
   remote MCP URL above.
3. Configure authentication if required, then add the tool to your agent.

**GitHub Copilot (VS Code)** — add the server to your workspace `.vscode/mcp.json`:

```json
{
  "servers": {
    "agent-finder": {
      "type": "http",
      "url": "http://agentfinder.github.com"
    }
  }
}
```

### How to invoke it

Open **Copilot Chat in Agent mode**; the `agent-finder` `search` tool is
available. Ask it to find a capability and it runs the search and lists matches.
Pair with the instructions (Option A) so it asks first and never auto-installs.

## Endpoint

Examples use GitHub's Agent Finder (`agentfinder.github.com`); Hugging Face
Discover (`https://evalstate-hf-discover.hf.space/search`) works the same way.
Point at either — or any compliant ARD discovery service — see
[Endpoints](../connect.md#endpoints).
