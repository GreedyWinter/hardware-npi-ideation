# Architecture

Hardware NPI Ideation is organized as a deployed interactive demo with a Gemini-backed structured generation path, deterministic fallback agents, a reusable NPI knowledge layer, and privacy guardrails.

```text
User
  -> Gradio UI
  -> Security Guardrails
     -> secret-like pattern redaction
     -> public export warning
  -> Agent Orchestrator
     -> Gemini structured JSON generation
     -> deterministic local fallback agents
  -> NPI Knowledge Tools
     -> in-process knowledge server for app runtime
     -> MCP-compatible server for external tool use
  -> NPI Ideation Package
     -> clarifying questions
     -> requirement brief
     -> definitions and assumptions
     -> risk register
     -> NPI timeline
     -> Markdown export
```

## Gemini Path

When `GEMINI_API_KEY` is configured, the orchestrator asks Gemini to generate the full NPI package as structured JSON. The response is parsed into typed dataclasses before being displayed in the UI.

The default model is `gemini-2.5-flash`, which is intended to be a fast and cost-conscious Gemini option. The model can be changed with `GEMINI_MODEL`.

If Gemini is unavailable, the app falls back to deterministic local agents so the public demo remains usable.

## Agent Subsystems

- `RequirementsIntakeAgent` organizes product intent into requirement categories.
- `DefinitionAssumptionAgent` turns ambiguous planning terms into measurable working definitions.
- `NPIRiskAgent` produces early NPI execution risks with severity, likelihood, phase, and mitigation.
- `TimelinePlanningAgent` maps the risk-adjusted plan into NPI phases and gates.

## MCP-Compatible Tool Service

`mcp_server.py` exposes the NPI knowledge layer through FastMCP tools:

- `get_npi_phases`
- `get_requirement_taxonomy`
- `common_ambiguous_terms`
- `lookup_definition`

The Gradio app uses the same knowledge layer in process for reliability. The MCP server demonstrates how the knowledge layer can be exposed to external agents or MCP-compatible clients.

Run it with:

```bash
python mcp_server.py
```

## Security

The first security layer is intentionally lightweight and visible in the demo:

- warns users not to enter confidential product, customer, supplier, cost, or credential data
- redacts common API-key-like and secret-like strings
- marks export safety status
- keeps all local fallback knowledge static and public

## Deployment

The app is designed for public deployment as a Gradio app, especially on Hugging Face Spaces. Deployment requires adding `GEMINI_API_KEY` as a secret only if Gemini-backed generation is desired. Without the secret, the deterministic fallback still runs.
