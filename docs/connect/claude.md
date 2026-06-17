# Connect Claude

Connect Claude to an Agent Finder either as a **Skill** (Claude Code) or a
**remote MCP connector** (claude.ai, Desktop, mobile). They work well together —
the MCP connector gives Claude the search tool; the Skill gives it the
"ask first, never auto-install" behavior.

## Option A — Skill (Claude Code)

Custom skills are currently **Claude Code only** — the claude.ai web app and
Claude Desktop don't support uploading your own skills yet.

**Install (recommended).** The connectors repo is a Claude Code plugin
marketplace, so it's two commands:

```
/plugin marketplace add ards-project/connectors
/plugin install agentfinder@ard-connectors
```

**Install (manual).** Copy the skill folder from the connectors repo into your
skills directory — `~/.claude/skills/` (personal) or `.claude/skills/` (project):

```
cp -r connectors/skills/agentfinder ~/.claude/skills/
```

### How to invoke it

Just ask Claude in plain language — the skill triggers on intent:

> "Find me an MCP server for querying Postgres."
>
> "What skills are available for making PowerPoint decks?"

The first time, Claude shows a **menu of Agent Finders** — GitHub Agent Finder,
Hugging Face Discover, or your own — and **remembers your pick** (saved in
`~/.agentfinder/finders.json`). After that it searches your saved finder directly;
say *switch agent finder* to change. It presents a numbered list of matches; pick
one and it shows how to install **that** resource — it never installs anything on
its own.

## Option B — Remote MCP connector

This gives Claude a native `search` tool across claude.ai, Desktop, and mobile.

1. **Settings → Connectors → Add custom connector.**
2. Name it `Agent Finder` and paste the remote MCP URL — GitHub's Agent Finder is
   `https://agentfinder.github.com/api/v1/mcp` (or use your own discovery service).
3. If the server requires sign-in, complete the OAuth flow when prompted.

**Older Claude Desktop** (no native remote connectors)? Bridge it with
`mcp-remote` in `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "agent-finder": {
      "command": "npx",
      "args": ["-y", "mcp-remote", "https://agentfinder.github.com/api/v1/mcp"]
    }
  }
}
```

### How to invoke it

Ask Claude to find a capability and it calls the connector's `search` tool, then
presents the results. Pair it with the **Skill** (Option A) so it offers the
Agent Finder menu, remembers your choice, and never auto-installs.

## Endpoint

Examples use GitHub's Agent Finder (`https://agentfinder.github.com/api/v1`); Hugging Face
Discover (`https://huggingface-hf-discover.hf.space/search`) works the same way.
Point at either — or any compliant ARD discovery service — see
[Endpoints](../connect.md#endpoints).
