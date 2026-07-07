# Five-Minute Demo Script

## Goal

Show that Hardware NPI Ideation turns an unclear hardware product concept into a structured NPI planning package using Gemini, agents, MCP-compatible tools, and security guardrails.

## Demo Flow

### 0:00-0:30 - Problem

Hardware NPI projects often begin with vague phrases such as "rugged," "low cost," "long battery life," and "fast launch." Those phrases are not enough to drive engineering, supplier, validation, and manufacturing decisions.

### 0:30-1:00 - Input

Use the preloaded cold-chain sensor scenario:

> A rugged wireless cold-chain sensor that monitors temperature and door-open events for refrigerated pharmaceutical shipments.

Point out the target customer, operating environment, constraints, and business goal fields.

### 1:00-1:45 - Agent Workflow

Click **Generate NPI Ideation Package**.

Explain that the orchestrator first runs security checks, then uses Gemini structured JSON generation when `GEMINI_API_KEY` is configured. If Gemini is unavailable, deterministic local fallback agents keep the public demo usable.

### 1:45-2:30 - Requirements and Definitions

Open **Requirement Brief** and **Definitions**.

Highlight how vague terms become actionable:

- rugged -> ingress, drop, vibration, and temperature targets
- long battery life -> duty cycle, temperature, radio usage, service interval
- low cost -> BOM, manufacturing cost, margin trade-offs

### 2:30-3:20 - Risk Register

Open **Risk Register**.

Highlight risks that would matter to a hardware business:

- qualitative requirements delaying execution
- supplier and tooling lead-time exposure
- battery-life conflict with size and radio duty cycle
- ruggedization impact on enclosure cost and validation schedule

### 3:20-4:10 - NPI Timeline

Open **NPI Timeline**.

Explain how the plan moves through Concept, Requirements, Architecture, EVT, DVT, PVT, Ramp, and Launch. Point out that high-risk projects can adjust EVT/DVT duration assumptions.

### 4:10-4:40 - Security and Export

Open **Export**.

Show the security review, the generated Markdown package, and the note that users should not enter confidential customer, supplier, cost, product, or credential data.

### 4:40-5:00 - Business Value

Close with the value proposition:

Hardware NPI Ideation helps teams ask better questions earlier, align stakeholders before capital-intensive development, and reduce costly ambiguity before architecture, tooling, validation, and launch commitments.
