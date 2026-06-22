# Reference Implementations

## Hugging Face Discover Tool

The Hugging Face [Discover Tool](https://github.com/huggingface/hf-discover) provides search access to thousands of Skills, ML Applications, and MCP Servers — on Hugging Face - or any other ARD compliant service.

### Hugging Face CLI (`hf`)

`discover` is built into the [Hugging Face CLI](https://github.com/huggingface/huggingface_hub) (`hf`). To get started:

```bash
# Install the Hugging Face CLI tool:
uv tool install huggingface_hub

# Search for resources to train a model
hf discover search "Fine tune a language model"

# Find MCP Servers to generate an image
hf discover search "Generate an image" --json --kind mcp

# Search other registries
hf discover search "Purchase aeroplane tickets" --registry-url <catalog-url>

# Navigate a federated catalog from a website
hf discover navigate <web-url> "Research biomedical datasets"
```

### REST and MCP API Access

Query the Hugging Face catalog service directly via:

  - The REST API at: `https://huggingface-hf-discover.hf.space/search`
  - MCP at: `https://huggingface-hf-discover.hf.space/mcp`

## GitHub Agent Finder

GitHub's Agent Finder is a discovery service for agentic resources — Skills, tools, and MCP servers — reachable over HTTPS at `https://agentfinder.github.com/api/v1`.

### GitHub Copilot

GitHub Copilot can search it directly: add Agent Finder as a remote MCP tool (or as custom instructions), then ask Copilot to find a capability for your task and it returns ranked matches you choose to install. See [Connect GitHub Copilot](connect/github-copilot.md) for the full setup — it uses this same endpoint as its example.

### HTTP API

Call search directly at `POST https://agentfinder.github.com/api/v1/search`. The MCP endpoint is `https://agentfinder.github.com/api/v1/mcp`.

## Cisco AI Catalog

The [AGNTCY Agent Directory](https://dir.agntcy.org) reference implementation of ARD is deployed by the Cisco [AI Catalog](https://ai-catalog.outshift.io).
The catalog can be pulled from [`ai-catalog.outshift.io/.well-known/ai-catalog.json`](https://ai-catalog.outshift.io/.well-known/ai-catalog.json).
It supports secure verification through trust manifests, so clients can validate publisher identity and resource integrity before use.

### 1. Pull the catalog manifest

```bash
curl -sS https://ai-catalog.outshift.io/.well-known/ai-catalog.json | jq '.specVersion, .host.displayName'
```

### 2. Discover A2A cards

```bash
curl -sS 'https://ai-catalog.outshift.io/v1/agents?filter=type%3Dapplication%2Fa2a-agent-card%2Bjson' \
	| jq -r '.results[] | "\(.displayName)\t\(.data.card_data.url // .identifier)"'
```

### 3. Search by card type and extract trust details

```bash
curl -sS 'https://ai-catalog.outshift.io/v1/agents?filter=type%3Dapplication%2Fmcp-server-card%2Bjson' \
	| jq -r '.results[] | {displayName, identity: .trustManifest.identity, identityType: .trustManifest.identityType, cardUrl: .data.card_data.url} | @json'
```

## Tiza

[Tiza](https://tiza.cc) is a hosted discovery service that continuously crawls and
live-protocol-probes public agentic resources — MCP servers, A2A agent cards,
Skills, and APIs — then ranks them for relevance and readiness. It implements ARD
as both a host and a federatable registry. The catalog can be pulled from
[`tiza.cc/.well-known/ai-catalog.json`](https://tiza.cc/.well-known/ai-catalog.json).

### HTTP API

Search the registry directly at `POST https://tiza.cc/api/ard/v1/search`:

```bash
curl -sS -X POST https://tiza.cc/api/ard/v1/search \
  -H 'content-type: application/json' \
  -d '{"query":{"text":"MCP server for GitHub issues"},"pageSize":5}' \
  | jq -r '.results[] | "\(.displayName)\t\(.url)"'
```

Results are standard ARD `CatalogEntry` objects with `urn:air:` identifiers and
the standard `application/{mcp-server-card,a2a-agent-card,ai-registry}+json` types.

### MCP and A2A

Tiza is also reachable as a hosted, no-auth MCP server at `https://tiza.cc/mcp`
and as an A2A agent at `https://tiza.cc/.well-known/agent-card.json`.
