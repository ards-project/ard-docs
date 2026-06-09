---
title: Agentic Resource Discovery Specification
hide:
  - toc
---

# Agentic Resource Discovery Specification

ARDS is an open discovery protocol for agentic resources. It allows an AI client to ask: *"What is available for this task?"* and lets a discovery service answer with matching resources.

ARDS sits entirely before invocation. It helps the client find the right resource; the resource is then invoked through its own native protocol.

## What is an agentic resource?

An agentic resource is any external capability an AI client can call on to do a task — an agent, MCP server, Skill, API, workflow, AI Catalog entry, or anything similar.

## What ARDS is not

**It is not an execution runtime:** ARDS is not MCP, A2A, Skills, AI Catalog, or an API runtime, and it does not replace them.

**It is not a central catalog:** Different discovery services can index different resources, serve different communities, and apply varying trust, ranking, and access policies.

## Who is behind ARDS?

ARDS is being developed by a working group with participants from Microsoft, Google, Hugging Face, GoDaddy, and others. This work is part of a broader effort to create an open discovery layer for AI-native resources.

To understand the motivation and design, start with the [Introduction](introduction.md).
