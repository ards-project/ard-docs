# Connect GitHub Copilot

GitHub Copilot is the AI coding assistant in VS Code, the other IDEs, the CLI,
and on github.com. Connect it to an Agent Finder either as an **Agent Skill** (a
`SKILL.md` Copilot discovers and activates on its own) or a **remote MCP
connector**. They work well together — the MCP connector gives Copilot the
`search` tool; the Skill makes it **default to GitHub's Agent Finder**, present
the results, and never auto-install.

## Option A — Agent Skill

A Copilot skill is a `SKILL.md` file on disk — there is no "install from a
store" button. Copilot uses the same `SKILL.md` format and skill folders as
Claude. Use the `github-copilot` skill, which **defaults to GitHub's Agent
Finder** so there's nothing to configure. Add it one of three ways:

**Drop in the folder.** Copy the skill into a directory Copilot scans —
`~/.copilot/skills/` (personal) or `.github/skills/<name>/` (project):

```
cp -r connectors/skills/github-copilot ~/.copilot/skills/
```

Copilot also reads `~/.claude/skills/` and `.claude/skills/`, so a skill you
already installed for Claude is picked up automatically.

**Use the CLI.** `gh skill` (in GitHub CLI) can search, install, and update
skills straight from a GitHub repo.

**Create it in the editor.** In Copilot Chat, open **Configure Chat** (the gear
icon) → the **Skills** tab → **New Skill (User)** / **New Skill (Workspace)** —
this scaffolds an *empty* `SKILL.md` for you to paste the connectors repo's
[`SKILL.md`](https://github.com/ards-project/connectors/blob/main/skills/github-copilot/SKILL.md)
into. (This editor UI is only in recent VS Code / Visual Studio 2026 builds.)

### How to invoke it

Copilot won't fire this Skill automatically — invoke it explicitly with its
slash command. In **Copilot Chat (Agent mode)**, type `/agentfinder` followed by
what you need:

> `/agentfinder` find me an MCP server for querying Postgres

It searches GitHub's Agent Finder, queries it, and lists the matches. Pair it
with the MCP connector (Option B) so it can make the call and never auto-installs.

## Option B — Remote MCP connector (VS Code)

> **Default endpoint:** GitHub's Agent Finder at `https://agentfinder.github.com/api/v1/mcp`.
> Replace it to use a different discovery service.

Add the server to your workspace `.vscode/mcp.json`:

```json
{
  "servers": {
    "agent-finder": {
      "type": "http",
      "url": "https://agentfinder.github.com/api/v1/mcp"
    }
  }
}
```

### How to invoke it

Open **Copilot Chat in Agent mode**; the `agent-finder` `search` tool is
available. Ask it to find a capability and it runs the search and lists matches.
Pair with the Skill (Option A) so it presents results and never auto-installs.

## Endpoint

Examples use GitHub's Agent Finder (`https://agentfinder.github.com/api/v1`); Hugging Face
Discover (`https://huggingface-hf-discover.hf.space/search`) works the same way.
Point at either — or any compliant ARD discovery service — see
[Endpoints](../connect.md#endpoints).
