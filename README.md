# Spec-Driven Development (SDD) Repository

A structured repository for Spec-Driven Development using MCP (Model Context Protocol) to guide AI-assisted implementation from specifications.

## What is Spec-Driven Development?

Spec-Driven Development is a workflow where:
1. **Specs come first** — features, APIs, and architecture are fully defined before code is written
2. **AI reads the specs** — MCP exposes specs to AI agents (Claude, Cursor, etc.) as context
3. **Code follows the spec** — implementation is validated against the specification

---

## Repository Structure

```
sdd-repo/
├── .mcp/
│   └── config.json          # MCP server configuration
├── specs/
│   ├── features/            # Feature specs (what the system does)
│   ├── architecture/        # Architecture specs (how the system is built)
│   └── api/                 # API specs (contracts & interfaces)
├── docs/                    # Supporting documentation
├── templates/               # Reusable spec templates
└── README.md
```

---

## Getting Started

### 1. Clone the repo
```bash
git clone <your-repo-url>
cd sdd-repo
```

### 2. Configure MCP
Edit `.mcp/config.json` to point to your MCP server or local filesystem server.

### 3. Write a spec
Use a template from `templates/` to write your first feature spec in `specs/features/`.

### 4. Connect your AI tool
Point Claude, Cursor, or another MCP-compatible AI tool at this repo. The AI will read your specs and generate compliant code.

---

## Spec Writing Guidelines

- **Be explicit** — avoid ambiguity in requirements
- **Use acceptance criteria** — define what "done" looks like
- **Version your specs** — use git history to track spec changes
- **Link related specs** — cross-reference features, APIs, and architecture docs

---

## MCP Integration

This repo is designed to work as an MCP resource server. AI tools can:
- Read specs as context before generating code
- Validate generated code against spec requirements
- Suggest spec updates when implementation diverges

See `.mcp/config.json` for configuration details.
