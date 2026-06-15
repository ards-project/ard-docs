# Reference Implementations

## Hugging Face Discover Tool

The Hugging Face [Discover Tool](https://github.com/huggingface/hf-discover) provides search access to thousands of Skills, ML Applications and MCP Servers. 

Install standalone (`uv tool install hf-discover`), or use directly from the [**hf cli**](https://github.com/huggingface/huggingface_hub):

```bash

# Search for resources to train a model
hf discover search "Fine tune a language model"

# Find MCP Servers to generate an image
hf discover search "Generate an image" --json --kind mcp

# Search other registries
hf discover search "Purchase aeroplane tickets" --registry-url <catalog-url>
```

Navigate mode supports locating AI Catalogs from URL's, and navigating federated registries.

Access our REST API via `https://huggingface.co/.well-known/ai-catalog.json` or call direct at `https://evalstate-hf-discover.hf.space/search`
