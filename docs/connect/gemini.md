# Connect Gemini

Gemini's equivalent of a Skill is a **Gem** (custom instructions). To actually run
searches you need a way to make HTTP/MCP calls — that's **Gemini CLI** or the
**Gemini API**. The **consumer Gemini app** can't call custom MCP servers or
arbitrary HTTP, so a Gem there can only describe the behavior, not execute it.

## Option A — Gem

**Install.** Create a new Gem and paste the instructions from the connectors repo
([`skills/gemini/`](https://github.com/ards-project/connectors/tree/main/skills/gemini)):

- **Name:** `find-agentic-resources`
- **Instructions:** copy the body of that file — it tells Gemini to ask which
  Agent Finder to query, present the ranked results, and never auto-install.

Pair the Gem with the **Gemini CLI** MCP setup below (or the Gemini API) so it can
make the call.

### How to invoke it

With the Gem selected (and the CLI/API able to call Agent Finder), ask in plain
language — *"Find me a tool that summarizes long PDFs."* Gemini asks which Agent
Finder to search, queries it, and lists the matches.

## Option B — Remote MCP connector (Gemini CLI)

Add the server to your Gemini CLI `settings.json`:

```json
{
  "mcpServers": {
    "agent-finder": {
      "httpUrl": "http://agentfinder.github.com"
    }
  }
}
```

Use `httpUrl` for a Streamable-HTTP server, `url` for SSE, or `command`/`args` for
a local/stdio server. Restart the CLI; the Agent Finder `search` tool is then
available. (The Gemini **API** can connect to remote MCP servers directly, or you
can expose `POST /search` as a function.)

### How to invoke it

In the Gemini CLI, ask it to find a capability for your task; it calls the
`search` tool and lists matches. Pair with the Gem (Option A) so it asks first and
never auto-installs.

## Endpoint

Examples use GitHub's Agent Finder (`agentfinder.github.com`); Hugging Face
Discover (`https://evalstate-hf-discover.hf.space/search`) works the same way.
Point at either — or any compliant ARD discovery service — see
[Endpoints](../connect.md#endpoints).
