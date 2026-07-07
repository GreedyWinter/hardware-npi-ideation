from __future__ import annotations

import os
from collections.abc import Iterator

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
) -> Iterator[tuple[str, str, str, str, str, str, str]]:
    status = "Generating the NPI ideation package. This can take 10-30 seconds when Gemini is active..."
    empty = ""
    yield status, empty, empty, empty, empty, empty, empty

    try:
        package = run_npi_workflow(
            product_idea=product_idea,
            target_customer=target_customer,
            operating_environment=operating_environment,
            known_constraints=known_constraints,
            business_goals=business_goals,
        )
    except Exception as exc:
        error = (
            "Generation failed before an NPI package could be created.\n\n"
            f"Error: `{type(exc).__name__}: {exc}`\n\n"
            "Try again with the sample scenario, or confirm the deployed service has access to the Gemini API key."
        )
        yield "Generation failed.", error, empty, empty, empty, empty, error
        return

    markdown = package_to_markdown(package)
    questions = "\n".join(f"- {item}" for item in package.clarifying_questions)
    requirements = package.requirement_brief.to_markdown()
    definitions = package.definitions.to_markdown()
    risks = package.risks_to_markdown()
    timeline = package.timeline_to_markdown()
    security = package.security_report.to_markdown()
    generation = package.generation_note()
    yield (
        f"Done. {package.generation_note()}",
        questions,
        generation + "\n\n" + requirements,
        definitions,
        risks,
        timeline,
        security + "\n\n" + markdown,
    )


with gr.Blocks(title="Hardware NPI Ideation") as demo:
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
            status_out = gr.Markdown("Ready. Click **Generate NPI Ideation Package** to run the workflow.")
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
            status_out,
            questions_out,
            requirements_out,
            definitions_out,
            risks_out,
            timeline_out,
            export_out,
        ],
    )
    demo.queue(default_concurrency_limit=4)


if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",
        server_port=int(os.environ.get("PORT", "7860")),
        theme=gr.themes.Soft(),
    )
