from __future__ import annotations

from .agents import DefinitionAssumptionAgent, NPIRiskAgent, RequirementsIntakeAgent, TimelinePlanningAgent
from .gemini_client import GeminiClient
from .knowledge import NPIKnowledgeServer
from .models import NPIIdeationPackage
from .security import sanitize_context
from .structured_gemini import generate_structured_package


def run_npi_workflow(
    product_idea: str,
    target_customer: str,
    operating_environment: str,
    known_constraints: str,
    business_goals: str,
) -> NPIIdeationPackage:
    raw_context = {
        "product_idea": product_idea,
        "target_customer": target_customer,
        "operating_environment": operating_environment,
        "known_constraints": known_constraints,
        "business_goals": business_goals,
    }
    context, security_report = sanitize_context(raw_context)

    knowledge = NPIKnowledgeServer()
    llm = GeminiClient()

    gemini_package = generate_structured_package(context, security_report, knowledge, llm)
    if gemini_package is not None:
        return gemini_package

    requirements_agent = RequirementsIntakeAgent(knowledge, llm)
    definition_agent = DefinitionAssumptionAgent(knowledge)
    risk_agent = NPIRiskAgent(knowledge)
    timeline_agent = TimelinePlanningAgent(knowledge)

    requirement_brief = requirements_agent.run(context)
    clarifying_questions = requirements_agent.questions(context)
    definitions = definition_agent.run(context)
    risks = risk_agent.run(context, definitions)
    timeline = timeline_agent.run(risks)

    return NPIIdeationPackage(
        clarifying_questions=clarifying_questions,
        requirement_brief=requirement_brief,
        definitions=definitions,
        risks=risks,
        timeline=timeline,
        security_report=security_report,
        generation_mode="Deterministic local fallback agents",
    )
