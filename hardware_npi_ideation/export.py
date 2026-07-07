from __future__ import annotations

from .models import NPIIdeationPackage


def package_to_markdown(package: NPIIdeationPackage) -> str:
    return "\n\n".join(
        [
            "# NPI Ideation Package",
            "## Clarifying Questions\n" + "\n".join(f"- {q}" for q in package.clarifying_questions),
            package.requirement_brief.to_markdown(),
            package.definitions.to_markdown(),
            package.risks_to_markdown(),
            package.timeline_to_markdown(),
            package.security_report.to_markdown(),
        ]
    )
