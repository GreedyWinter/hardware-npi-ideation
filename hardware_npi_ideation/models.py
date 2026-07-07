from __future__ import annotations

from dataclasses import dataclass


@dataclass
class RequirementBrief:
    functional: list[str]
    performance: list[str]
    environmental: list[str]
    manufacturing: list[str]
    business: list[str]
    taxonomy: list[str]

    def to_markdown(self) -> str:
        sections = {
            "Functional": self.functional,
            "Performance": self.performance,
            "Environmental": self.environmental,
            "Manufacturing": self.manufacturing,
            "Business": self.business,
        }
        parts = ["## Requirement Brief"]
        for title, items in sections.items():
            parts.append(f"### {title}")
            parts.extend(f"- {item}" for item in items)
        return "\n".join(parts)


@dataclass
class DefinitionSet:
    definitions: dict[str, str]
    assumptions: list[str]

    def to_markdown(self) -> str:
        parts = ["## Definitions and Assumptions", "### Working Definitions"]
        parts.extend(f"- **{term}:** {definition}" for term, definition in self.definitions.items())
        parts.append("### Assumptions")
        parts.extend(f"- {item}" for item in self.assumptions)
        return "\n".join(parts)


@dataclass
class RiskItem:
    risk: str
    phase: str
    severity: str
    likelihood: str
    mitigation: str


@dataclass
class TimelinePhase:
    name: str
    duration: str
    activities: list[str]
    gate: str


@dataclass
class SecurityReport:
    redacted_fields: list[str]
    warnings: list[str]
    safe_for_public_demo: bool

    def to_markdown(self) -> str:
        status = "Yes" if self.safe_for_public_demo else "Review required"
        parts = ["## Security and Privacy Review", f"- Safe for public demo export: **{status}**"]
        if self.redacted_fields:
            parts.append("- Redacted fields: " + ", ".join(self.redacted_fields))
        if self.warnings:
            parts.append("### Warnings")
            parts.extend(f"- {warning}" for warning in self.warnings)
        return "\n".join(parts)


@dataclass
class NPIIdeationPackage:
    clarifying_questions: list[str]
    requirement_brief: RequirementBrief
    definitions: DefinitionSet
    risks: list[RiskItem]
    timeline: list[TimelinePhase]
    security_report: SecurityReport

    def risks_to_markdown(self) -> str:
        rows = ["## Risk Register", "| Risk | Phase | Severity | Likelihood | Mitigation |", "|---|---|---|---|---|"]
        for risk in self.risks:
            rows.append(
                f"| {risk.risk} | {risk.phase} | {risk.severity} | {risk.likelihood} | {risk.mitigation} |"
            )
        return "\n".join(rows)

    def timeline_to_markdown(self) -> str:
        rows = ["## High-Level NPI Timeline", "| Phase | Duration | Activities | Gate |", "|---|---:|---|---|"]
        for phase in self.timeline:
            rows.append(
                f"| {phase.name} | {phase.duration} | {', '.join(phase.activities)} | {phase.gate} |"
            )
        return "\n".join(rows)
