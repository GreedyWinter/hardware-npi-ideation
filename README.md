# Hardware NPI Ideation

Agentic engineering for requirement gathering, definitions, risk analysis, and high-level timeline planning in hardware New Product Introduction.

## Overview

Hardware NPI Ideation is an interactive agentic planning assistant for early-stage hardware product development. It helps product, engineering, manufacturing, and operations stakeholders turn an incomplete hardware concept into a structured NPI ideation package.

Early hardware programs often begin with vague goals such as "rugged," "low cost," "long battery life," or "fast launch." Those phrases are useful conversation starters, but they are not enough to guide engineering execution. When ambiguity survives too long, teams can lose time to late requirement changes, supplier delays, validation gaps, certification surprises, tooling rework, and schedule slips.

This project uses a multi-agent workflow to make that early ambiguity visible. The system gathers requirements, proposes measurable definitions, records assumptions, identifies NPI risks, and generates a high-level phase timeline that can be reviewed before expensive development work begins.

## Kaggle Submission Context

This repository supports the Kaggle **AI Agents: Intensive Vibe Coding Capstone Project** submission:

- **Title:** Hardware NPI Ideation
- **Subtitle:** Agentic engineering the requirement gathering with definitions into a high-level timeline of a hardware NPI
- **Track:** Agents for Business

The submission is focused on a practical enterprise workflow: improving early planning quality for hardware development programs.

## V1 Interactive Demo

The first version is a Gradio application. It is suitable for a public Hugging Face Space or a similar free demo host.

The demo lets a user enter an early hardware product idea and optional constraints, such as:

- target user or customer segment
- operating environment
- product function
- cost target
- expected volume
- power or battery constraints
- launch timing
- compliance or certification needs

The system then generates an NPI ideation package containing:

- clarifying questions
- structured requirement brief
- definitions and assumptions
- early risk register
- high-level NPI timeline
- exportable Markdown summary

## Gemini Model Path

V1 uses Gemini when `GEMINI_API_KEY` is available. The default model is:

```text
gemini-2.5-flash
```

The model can be changed with `GEMINI_MODEL`. The app also includes deterministic fallback behavior so the demo remains usable without an API key.

## Run Locally

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python app.py
```

Set `GEMINI_API_KEY` in your environment or `.env` when you want Gemini-backed question generation.

## Planned Architecture

The solution is organized around a small multi-agent system and a reusable NPI knowledge tool layer.

```text
User
  -> Interactive Demo UI
  -> Agent Orchestrator
     -> Requirements Intake Agent
     -> Definition and Assumption Agent
     -> NPI Risk Agent
     -> Timeline Planning Agent
     -> Report Export Agent
  -> MCP-style NPI Knowledge Server
  -> Security and Privacy Guardrails
  -> NPI Ideation Package
```

### Core Agents

**Requirements Intake Agent**

Organizes a rough product idea into functional, performance, environmental, electrical, mechanical, manufacturing, validation, and business requirement categories.

**Definition and Assumption Agent**

Detects ambiguous terms and proposes measurable working definitions. It also records assumptions that require stakeholder confirmation.

**NPI Risk Agent**

Evaluates the structured requirements and assumptions against common hardware NPI risk patterns, including supplier availability, certification, thermal constraints, reliability testing, firmware readiness, tooling lead time, and manufacturing test coverage.

**Timeline Planning Agent**

Maps requirements and risks into a high-level NPI timeline with phases such as Concept, Requirements, Architecture, EVT, DVT, PVT, Pilot, Ramp, and Launch.

**Report Export Agent**

Consolidates the workflow output into a judge-friendly and stakeholder-friendly package.

## MCP-Style Knowledge Layer

The project includes a tool layer inspired by MCP concepts. This layer exposes structured hardware NPI knowledge to the agents, such as:

- NPI phase definitions
- requirement taxonomy
- risk checklist
- validation templates
- phase-gate expectations
- definition lookup for common hardware terms

This keeps domain knowledge explicit and reusable instead of hiding it entirely inside prompts.

## Security and Privacy Intent

Hardware planning data can contain confidential product, customer, supplier, or cost information. The demo includes lightweight guardrails that:

- warn users not to paste confidential information
- detect and redact API-key-like or secret-like strings
- provide a safe export review
- avoid committing credentials or private data
- document local and deployed data-handling assumptions

## Key Course Concepts Demonstrated

The implementation is scoped to demonstrate at least these concepts:

- multi-agent system
- MCP-style tool server
- security and privacy guardrails
- deployable public interactive demo
- documented agent-assisted development workflow

## Project Status

V1 includes:

- Gradio interactive app
- multi-agent workflow classes
- MCP-style local NPI knowledge server
- optional Gemini client
- secret redaction and safe export messaging
- sample hardware NPI scenario

Next steps:

1. deploy the public Gradio app
2. add richer Gemini-backed structured generation
3. add architecture media assets to the repo
4. finalize Kaggle writeup and demo video

## License

License to be selected before the first public release.
