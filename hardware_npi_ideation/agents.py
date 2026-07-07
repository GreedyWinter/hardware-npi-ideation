from __future__ import annotations

from .gemini_client import GeminiClient
from .knowledge import NPIKnowledgeServer
from .models import DefinitionSet, RequirementBrief, RiskItem, TimelinePhase


class RequirementsIntakeAgent:
    def __init__(self, knowledge: NPIKnowledgeServer, llm: GeminiClient) -> None:
        self.knowledge = knowledge
        self.llm = llm

    def run(self, context: dict[str, str]) -> RequirementBrief:
        taxonomy = self.knowledge.get_requirement_taxonomy()
        text = " ".join(context.values()).lower()

        functional = [
            f"Define core product behavior for: {context['product_idea']}",
            "Describe primary user workflow and expected system response.",
        ]
        performance = ["Set measurable targets for accuracy, latency, battery life, and reliability."]
        environmental = [f"Validate operation in: {context['operating_environment'] or 'the intended field environment'}."]
        manufacturing = ["Identify expected production volume, tooling needs, test strategy, and supplier constraints."]
        business = [f"Align NPI plan to business goal: {context['business_goals'] or 'launch a viable hardware product'}."]

        if "battery" in text:
            performance.append("Quantify battery-life target by duty cycle, temperature, and radio usage.")
        if "rugged" in text or "industrial" in text:
            environmental.append("Define ingress, drop, vibration, and temperature requirements.")
        if "cost" in text or "low" in text:
            business.append("Translate cost intent into target BOM, manufacturing cost, and margin assumptions.")

        return RequirementBrief(
            functional=functional,
            performance=performance,
            environmental=environmental,
            manufacturing=manufacturing,
            business=business,
            taxonomy=taxonomy,
        )

    def questions(self, context: dict[str, str]) -> list[str]:
        prompt = (
            "Generate five concise stakeholder questions for an early hardware NPI planning review. "
            f"Product: {context['product_idea']}. Customer: {context['target_customer']}. "
            f"Environment: {context['operating_environment']}. Constraints: {context['known_constraints']}."
        )
        generated = self.llm.generate_lines(prompt, max_lines=5)
        if generated:
            return generated
        return [
            "What measurable outcome proves the product solves the customer problem?",
            "Which requirements are fixed, and which can trade against cost or schedule?",
            "What operating temperature, ingress, drop, and vibration targets are required?",
            "What certification, safety, or regulatory paths must be planned before EVT?",
            "What production volume and launch window should drive tooling and supplier decisions?",
        ]


class DefinitionAssumptionAgent:
    def __init__(self, knowledge: NPIKnowledgeServer) -> None:
        self.knowledge = knowledge

    def run(self, context: dict[str, str]) -> DefinitionSet:
        text = " ".join(context.values()).lower()
        definitions: dict[str, str] = {}
        assumptions: list[str] = []

        for term in self.knowledge.common_ambiguous_terms():
            if term in text:
                definitions[term] = self.knowledge.lookup_definition(term)

        if not definitions:
            definitions["early NPI"] = "A planning stage that converts product intent into requirements, risks, phase gates, and execution assumptions."

        assumptions.append("Timeline is a high-level planning estimate and must be reviewed by engineering, operations, supply chain, and quality.")
        assumptions.append("No confidential customer, supplier, cost, or unreleased design data is required for this public demo.")
        return DefinitionSet(definitions=definitions, assumptions=assumptions)


class NPIRiskAgent:
    def __init__(self, knowledge: NPIKnowledgeServer) -> None:
        self.knowledge = knowledge

    def run(self, context: dict[str, str], definitions: DefinitionSet) -> list[RiskItem]:
        text = " ".join(context.values()).lower()
        risks = [
            RiskItem(
                risk="Requirements remain too qualitative for engineering execution.",
                phase="Requirements",
                severity="High",
                likelihood="Medium",
                mitigation="Convert ambiguous terms into measurable thresholds before architecture freeze.",
            ),
            RiskItem(
                risk="Supplier or tooling lead times are not represented in the launch plan.",
                phase="Architecture / EVT",
                severity="Medium",
                likelihood="Medium",
                mitigation="Identify long-lead components and tooling assumptions before EVT build planning.",
            ),
        ]

        if "battery" in text:
            risks.append(
                RiskItem(
                    risk="Battery-life target may conflict with size, radio duty cycle, and operating temperature.",
                    phase="Architecture",
                    severity="High",
                    likelihood="Medium",
                    mitigation="Run an early power budget and define duty-cycle assumptions.",
                )
            )
        if "cert" in text or "regulat" in text or "medical" in text:
            risks.append(
                RiskItem(
                    risk="Certification path may add validation scope and calendar risk.",
                    phase="DVT",
                    severity="High",
                    likelihood="Medium",
                    mitigation="Confirm regulatory category and test lab lead times before DVT.",
                )
            )
        if "rugged" in definitions.definitions or "industrial" in text:
            risks.append(
                RiskItem(
                    risk="Ruggedization requirements may affect enclosure cost, tooling complexity, and validation schedule.",
                    phase="EVT / DVT",
                    severity="Medium",
                    likelihood="High",
                    mitigation="Define ingress, drop, vibration, and thermal targets before prototype design.",
                )
            )
        return risks


class TimelinePlanningAgent:
    def __init__(self, knowledge: NPIKnowledgeServer) -> None:
        self.knowledge = knowledge

    def run(self, risks: list[RiskItem]) -> list[TimelinePhase]:
        phases = []
        for phase in self.knowledge.get_npi_phases():
            duration = phase["duration"]
            if phase["name"] in {"EVT", "DVT"} and any(r.severity == "High" for r in risks):
                duration = phase["risk_adjusted_duration"]
            phases.append(
                TimelinePhase(
                    name=phase["name"],
                    duration=duration,
                    activities=phase["activities"],
                    gate=phase["gate"],
                )
            )
        return phases
