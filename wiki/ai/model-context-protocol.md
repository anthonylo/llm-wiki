---
title: Model Context Protocol (MCP)
tags: [MCP, tool-use, agentic-AI, protocol, LLM-integration]
source: "2503.23278v3 — MCP: Landscape, Security Threats, and Future Research Directions (Hou et al., 2025)"
---

## Summary

The Model Context Protocol (MCP), introduced by Anthropic in 2024, is an open standard that defines how [[large-language-models]] communicate with external tools, data sources, and services. It standardises the interface between AI models (hosts/clients) and the capabilities they can invoke (servers), extending LLMs from passive text processors to active agents capable of reading files, executing code, querying APIs, and managing persistent state.

## Explanation

### Motivation

LLMs alone can only work within their training knowledge and context window. To build useful agents, models need to:
- Read and write files
- Query databases and APIs
- Execute code
- Manage persistent state across sessions
- Discover available tools dynamically

MCP provides a standardised protocol for all of this, replacing the bespoke tool-integration code that every LLM application previously had to implement independently.

### Architecture: Host, Client, Server

```
┌──────────────────────────────────────┐
│  HOST                                │
│  (Claude Desktop, IDE, Agent App)    │
│                                      │
│   ┌─────────────────┐                │
│   │  MCP CLIENT     │◄──────────────┼──── User
│   │  (LLM + logic)  │               │
│   └────────┬────────┘               │
└────────────┼───────────────────────┘
             │  MCP Protocol (JSON-RPC 2.0)
    ┌────────┴────────┬───────────────┐
    ▼                 ▼               ▼
┌────────┐      ┌──────────┐   ┌──────────┐
│ MCP    │      │  MCP     │   │  MCP     │
│ Server │      │  Server  │   │  Server  │
│(Files) │      │  (DB)    │   │  (Code)  │
└────────┘      └──────────┘   └──────────┘
```

- **Host**: The application embedding the LLM (e.g., Claude Desktop, VS Code extension, custom agent)
- **Client**: The MCP client running inside the host, managing connections and translating LLM tool calls to MCP protocol
- **Server**: A lightweight process exposing capabilities (tools, resources, prompts) via the MCP protocol

### Four Primitive Types

| Primitive | Direction | Description |
|-----------|-----------|-------------|
| **Tools** | Client → Server | Functions the LLM can invoke (read file, query DB, run script) |
| **Resources** | Server → Client | Data the LLM can read (file contents, DB rows, API responses) |
| **Prompts** | Server → Client | Pre-defined prompt templates the server provides |
| **Sampling** | Server → Client | Server requests the LLM to generate text (server-initiated inference) |

### Lifecycle

MCP defines a 4-phase lifecycle:

1. **Creation**: Developer builds an MCP server, defines its tools/resources/prompts
2. **Deployment**: Server published (NPM, PyPI, Docker) and registered in host's config
3. **Operation**: Host discovers servers → client connects → LLM invokes tools dynamically
4. **Maintenance**: Server updates, version management, deprecation

### Transport Mechanisms

- **stdio**: Host spawns server as subprocess; communication over stdin/stdout. Low latency, local only.
- **HTTP + SSE** (Server-Sent Events): Remote servers; supports streaming responses
- Future: WebSocket for bidirectional streaming

### MCP vs RAG

| Dimension | [[retrieval-augmented-generation|RAG]] | MCP |
|-----------|------|-----|
| Primary function | Passive text retrieval | Active tool/resource invocation |
| Directionality | One-way (retrieve) | Bidirectional (read + write + execute) |
| State | Stateless index query | Stateful sessions possible |
| Standardisation | No standard protocol | MCP protocol standard |
| Scope | Knowledge retrieval | Any external capability |

MCP subsumes RAG: a RAG pipeline can be implemented as an MCP server (search tool + resources), but MCP covers many more use cases.

### Ecosystem

By 2025, hundreds of MCP servers existed covering:
- File systems, databases (PostgreSQL, SQLite, MongoDB)
- Web search and browsing
- Code execution (Python, JavaScript sandboxes)
- Version control (Git, GitHub)
- Communication tools (Slack, email)
- Cloud providers (AWS, GCP tools)

## Related Pages

- [[mcp-security-threats]] — 16 threat scenarios across the MCP lifecycle
- [[retrieval-augmented-generation]] — RAG is subsumed by MCP's tool/resource model
- [[large-language-models]] — MCP extends LLMs with active capabilities
- [[agi-definition]] — MCP closes some AGI domain gaps (knowledge retrieval, tool use) but others remain
- [[long-term-memory-in-ai]] — MCP resource primitives provide external LTM access; not intrinsic
- [[context]] — the "context" in MCP is structured (tools, resources, prompts) vs. Wan's formal typed relation

## Contradictions

> **Informal vs formal context**: MCP's name includes "context" but uses the term informally. The protocol passes structured data (tool descriptions, resource contents) — which is arguably closer to McCarthy's `ist(c, p)` notion than a raw token window — but lacks the formal typing and operators of Wan's (2009) context theory ([[context]]).

> **MCP vs RAG completeness**: The RAG survey (Paper 3) presents comprehensive passive retrieval as the primary external knowledge mechanism. MCP (Paper 4) implicitly supersedes this by supporting active operations. The papers exist in parallel — the RAG survey predates MCP's widespread adoption — but practitioners should be aware that MCP represents the next generation beyond pure RAG.
