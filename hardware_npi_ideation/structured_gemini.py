from __future__ import annotations

import json
from typing import Any

from .gemini_client import GeminiClient
from .knowledge import NPIKnowledgeServer
from .models import DefinitionSet, NPIIdeationPackage, RequirementBrief, RiskItem, SecurityReport, TimelinePhase


def generate_structured_package(
    context: dict[str, str],
    security_report: SecurityReport,
    knowledge: NPIKnowledgeServer,
    llm: GeminiClient,
) -> NPIIdeationPackage | None:
    if not llm.enabled:
        return None

    prompt = _build_prompt(context, knowledge)
    data = llm.generate_json(prompt)
    if not data:
        return None

    try:
        return _package_from_dict(data, security_report, llm.model_name)
    except (KeyError, TypeError, ValueError):
        return None


def _build_prompt(context: dict[str, str], knowledge: NPIKnowledgeServer) -> str:
    knowledge_payload = {
        "requirement_taxonomy": knowledge.get_requirement_taxonomy(),
        "npi_phases": knowledge.get_npi_phases(),
        "ambiguous_terms": {term: knowledge.lookup_definition(term) for term in knowledge.common_ambiguous_terms()},
    }
    schema = {
        "clarifying_questions": ["string"],
        "requirement_brief": {
            "functional": ["string"],
            "performance": ["string"],
            "environmental": ["string"],
            "manufacturing": ["string"],
            "business": ["string"],
        },
        "definitions": {"definitions": {"term": "definition"}, "assumptions": ["string"]},
        "risks": [
            {
                "risk": "string",
                "phase": "string",
                "severity": "Low | Medium | High",
                "likelihood": "Low | Medium | High",
                "mitigation": "string",
            }
        ],
        "timeline": [
            {
                "name": "string",
                "duration": "string",
                "activities": ["string"],
                "gate": "string",
            }
        ],
    }
    return (
        "You are a senior hardware NPI planning agent. Generate a practical early NPI ideation package. "
        "Use the provided NPI knowledge, keep the output specific to the product, and do not invent confidential facts. "
        "Return only valid JSON matching the schema.\n\n"
        f"Context:\n{json.dumps(context, indent=2)}\n\n"
        f"NPI knowledge tools output:\n{json.dumps(knowledge_payload, indent=2)}\n\n"
        f"Required JSON schema:\n{json.dumps(schema, indent=2)}"
    )


def _package_from_dict(data: dict[str, Any], security_report: SecurityReport, model_name: str) -> NPIIdeationPackage:
    brief = data["requirement_brief"]
    definition_block = data["definitions"]
    requirement_brief = RequirementBrief(
        functional=_list_of_strings(brief.get("functional")),
        performance=_list_of_strings(brief.get("performance")),
        environmental=_list_of_strings(brief.get("environmental")),
        manufacturing=_list_of_strings(brief.get("manufacturing")),
        business=_list_of_strings(brief.get("business")),
        taxonomy=["functional", "performance", "environmental", "manufacturing", "business"],
    )
    definitions = DefinitionSet(
        definitions={str(k): str(v) for k, v in dict(definition_block.get("definitions", {})).items()},
        assumptions=_list_of_strings(definition_block.get("assumptions")),
    )
    risks = [
        RiskItem(
            risk=str(item["risk"]),
            phase=str(item["phase"]),
            severity=str(item["severity"]),
            likelihood=str(item["likelihood"]),
            mitigation=str(item["mitigation"]),
        )
        for item in list(data["risks"])
    ]
    timeline = [
        TimelinePhase(
            name=str(item["name"]),
            duration=str(item["duration"]),
            activities=_list_of_strings(item.get("activities")),
            gate=str(item["gate"]),
        )
        for item in list(data["timeline"])
    ]
    return NPIIdeationPackage(
        clarifying_questions=_list_of_strings(data["clarifying_questions"]),
        requirement_brief=requirement_brief,
        definitions=definitions,
        risks=risks,
        timeline=timeline,
        security_report=security_report,
        generation_mode=f"Gemini structured JSON ({model_name})",
    )


def _list_of_strings(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(item) for item in value if str(item).strip()]
