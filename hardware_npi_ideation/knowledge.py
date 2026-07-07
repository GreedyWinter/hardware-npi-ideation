from __future__ import annotations


class NPIKnowledgeServer:
    """MCP-style local knowledge tool layer for hardware NPI planning."""

    def get_requirement_taxonomy(self) -> list[str]:
        return [
            "functional",
            "performance",
            "environmental",
            "electrical",
            "mechanical",
            "manufacturing",
            "validation",
            "business",
        ]

    def get_npi_phases(self) -> list[dict[str, object]]:
        return [
            {
                "name": "Concept",
                "duration": "1-2 weeks",
                "risk_adjusted_duration": "1-2 weeks",
                "activities": ["frame problem", "identify stakeholders", "draft business intent"],
                "gate": "concept brief",
            },
            {
                "name": "Requirements",
                "duration": "2-3 weeks",
                "risk_adjusted_duration": "3-4 weeks",
                "activities": ["define measurable requirements", "resolve assumptions", "baseline PRD"],
                "gate": "requirements baseline",
            },
            {
                "name": "Architecture",
                "duration": "2-4 weeks",
                "risk_adjusted_duration": "4-6 weeks",
                "activities": ["system architecture", "make/buy decisions", "early risk burn-down"],
                "gate": "architecture review",
            },
            {
                "name": "EVT",
                "duration": "6-8 weeks",
                "risk_adjusted_duration": "8-10 weeks",
                "activities": ["engineering prototypes", "core function validation", "design issue discovery"],
                "gate": "EVT report",
            },
            {
                "name": "DVT",
                "duration": "8-10 weeks",
                "risk_adjusted_duration": "10-12 weeks",
                "activities": ["design validation", "reliability testing", "certification planning"],
                "gate": "DVT pass/fail review",
            },
            {
                "name": "PVT",
                "duration": "6-8 weeks",
                "risk_adjusted_duration": "6-9 weeks",
                "activities": ["manufacturing validation", "test coverage", "quality readiness"],
                "gate": "production readiness",
            },
            {
                "name": "Ramp",
                "duration": "4-6 weeks",
                "risk_adjusted_duration": "4-8 weeks",
                "activities": ["supplier scale-up", "yield monitoring", "launch quality checks"],
                "gate": "launch approval",
            },
        ]

    def common_ambiguous_terms(self) -> list[str]:
        return ["rugged", "low cost", "long battery life", "high volume", "fast launch"]

    def lookup_definition(self, term: str) -> str:
        definitions = {
            "rugged": "Translate into measurable ingress, drop, vibration, shock, and operating-temperature targets.",
            "low cost": "Translate into target BOM cost, manufacturing cost, gross margin, and allowed trade-offs.",
            "long battery life": "Translate into operating profile, duty cycle, battery capacity, temperature range, and service interval.",
            "high volume": "Translate into annual volume, peak weekly build rate, tooling strategy, and supplier capacity.",
            "fast launch": "Translate into target launch date, phase-gate compression, validation trade-offs, and staffing assumptions.",
        }
        return definitions.get(term, "Define the term with measurable acceptance criteria before committing schedule or cost.")
