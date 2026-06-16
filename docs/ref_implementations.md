# Reference Implementations

## Hugging Face Discover Tool

The Hugging Face [Discover Tool](https://github.com/huggingface/hf-discover) provides search access to thousands of Skills, ML Applications, and MCP Servers — on Hugging Face and across other ARD discovery services.

### Hugging Face CLI (`hf`)

`discover` is built into the [Hugging Face CLI](https://github.com/huggingface/huggingface_hub) (`hf`). Install it standalone with `uv tool install hf-discover`, or use the `hf` CLI directly:

```bash
# Search for resources to train a model
hf discover search "Fine tune a language model"

# Find MCP Servers to generate an image
hf discover search "Generate an image" --json --kind mcp

# Search other registries
hf discover search "Purchase aeroplane tickets" --registry-url <catalog-url>
```

Navigate mode locates AI Catalogs from URLs and traverses federated registries.

### REST API

Reach the same data over HTTP — the catalog at `https://huggingface.co/.well-known/ai-catalog.json`, or call search directly at `https://evalstate-hf-discover.hf.space/search`.
