# Connect ChatGPT

ChatGPT can use Agent Finder through a **Skill** plus a way to make the call —
either a **remote MCP connector** (Developer mode) or a custom **Action** over the
REST `POST /search`. The Skill supplies the behavior; the connector or Action
makes the request.

## Option A — Skill

ChatGPT Skills are reusable instruction sets, available on **Business,
Enterprise, Edu, and Team** plans. Unlike Claude and Copilot, a ChatGPT Skill
lives in your workspace, not in a file — you add it through the UI.

**Install.** In your ChatGPT workspace, use **Add skill** to open the Skills
editor, then create the skill from the connectors repo
([`skills/chatgpt/`](https://github.com/ards-project/connectors/tree/main/skills/chatgpt)):

- **Name:** `agentfinder`
- **Instructions:** paste the body of that file (show a menu of named Agent
  Finders, remember the choice, present the ranked results, and never auto-install).

A Skill on its own can't make network calls, so pair it with **Option B** (MCP
connector) or a custom **Action** whose OpenAPI calls
`POST https://agentfinder.github.com/api/v1/search`.

### How to invoke it

ChatGPT can use the skill automatically when it's relevant, or you can invoke it
explicitly by @-mentioning it:

> @agentfinder find me a tool for converting CSVs to charts

Either way it shows a menu of Agent Finders the first time (and remembers your
pick), runs the query via the
connector/Action, and presents the matches for you to pick from.

## Option B — Remote MCP connector (Developer mode)

ChatGPT supports **remote MCP servers** (HTTPS, Streamable HTTP / SSE) through
**Developer mode** (Plus, Pro, Business, Enterprise, Education).

1. **Settings → Apps → Advanced settings → Developer mode** (enable it).
2. **Create app** next to Advanced settings.
3. Name it `Agent Finder` and paste the remote MCP URL —
   `https://agentfinder.github.com/api/v1/mcp` (or your own discovery service).
4. Choose authentication — **No authentication** for an open Agent Finder, or
   **OAuth** if it requires sign-in.
5. Save — the `search` tool is now available in chat.

### How to invoke it

Ask ChatGPT to find a capability for your task; it calls the Agent Finder
`search` tool and lists the matches. Pair it with the Skill (Option A) so it asks
first and never auto-installs.

## Endpoint

Examples use GitHub's Agent Finder (`https://agentfinder.github.com/api/v1`); Hugging Face
Discover (`https://huggingface-hf-discover.hf.space/search`) works the same way.
Point at either — or any compliant ARD discovery service — see
[Endpoints](../connect.md#endpoints).
