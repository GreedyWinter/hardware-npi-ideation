from __future__ import annotations

import gradio as gr

from hardware_npi_ideation.export import package_to_markdown
from hardware_npi_ideation.orchestrator import run_npi_workflow
from hardware_npi_ideation.samples import DEMO_SCENARIO


def analyze(
    product_idea: str,
    target_customer: str,
    operating_environment: str,
    known_constraints: str,
    business_goals: str,
) -> tuple[str, str, str, str, str, str]:
    package = run_npi_workflow(
        product_idea=product_idea,
        target_customer=target_customer,
        operating_environment=operating_environment,
        known_constraints=known_constraints,
        business_goals=business_goals,
    )

    markdown = package_to_markdown(package)
    questions = "\n".join(f"- {item}" for item in package.clarifying_questions)
    requirements = package.requirement_brief.to_markdown()
    definitions = package.definitions.to_markdown()
    risks = package.risks_to_markdown()
    timeline = package.timeline_to_markdown()
    security = package.security_report.to_markdown()
    generation = package.generation_note()
    return questions, generation + "\n\n" + requirements, definitions, risks, timeline, security + "\n\n" + markdown


with gr.Blocks(title="Hardware NPI Ideation", theme=gr.themes.Soft()) as demo:
    gr.Markdown(
        """
        # Hardware NPI Ideation

        Agentic requirement gathering, definitions, risk analysis, and timeline planning for hardware NPI.
        The app uses Gemini structured JSON generation when `GEMINI_API_KEY` is configured and deterministic fallback agents otherwise.
        """
    )

    with gr.Row():
        with gr.Column(scale=1):
            product_idea = gr.Textbox(
                label="Hardware product idea",
                lines=4,
                value=DEMO_SCENARIO["product_idea"],
            )
            target_customer = gr.Textbox(
                label="Target customer or user",
                value=DEMO_SCENARIO["target_customer"],
            )
            operating_environment = gr.Textbox(
                label="Operating environment",
                value=DEMO_SCENARIO["operating_environment"],
            )
            known_constraints = gr.Textbox(
                label="Known constraints",
                lines=4,
                value=DEMO_SCENARIO["known_constraints"],
            )
            business_goals = gr.Textbox(
                label="Business goals",
                lines=3,
                value=DEMO_SCENARIO["business_goals"],
            )
            run_button = gr.Button("Generate NPI Ideation Package", variant="primary")

        with gr.Column(scale=2):
            with gr.Tab("Clarifying Questions"):
                questions_out = gr.Markdown()
            with gr.Tab("Requirement Brief"):
                requirements_out = gr.Markdown()
            with gr.Tab("Definitions"):
                definitions_out = gr.Markdown()
            with gr.Tab("Risk Register"):
                risks_out = gr.Markdown()
            with gr.Tab("NPI Timeline"):
                timeline_out = gr.Markdown()
            with gr.Tab("Export"):
                export_out = gr.Markdown()

    run_button.click(
        analyze,
        inputs=[
            product_idea,
            target_customer,
            operating_environment,
            known_constraints,
            business_goals,
        ],
        outputs=[
            questions_out,
            requirements_out,
            definitions_out,
            risks_out,
            timeline_out,
            export_out,
        ],
    )


if __name__ == "__main__":
    demo.launch()
