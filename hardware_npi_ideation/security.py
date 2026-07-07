from __future__ import annotations

import re

from .models import SecurityReport


SECRET_PATTERNS = [
    re.compile(r"AIza[0-9A-Za-z\-_]{20,}"),
    re.compile(r"sk-[0-9A-Za-z\-_]{20,}"),
    re.compile(r"ghp_[0-9A-Za-z]{20,}"),
    re.compile(r"(?i)(api[_ -]?key|password|secret)\s*[:=]\s*\S+"),
]


def sanitize_context(context: dict[str, str]) -> tuple[dict[str, str], SecurityReport]:
    sanitized: dict[str, str] = {}
    redacted_fields: list[str] = []
    warnings = [
        "Do not paste confidential customer names, supplier pricing, unreleased product details, passwords, or API keys into the public demo.",
    ]

    for field, value in context.items():
        cleaned = value or ""
        redacted = False
        for pattern in SECRET_PATTERNS:
            if pattern.search(cleaned):
                cleaned = pattern.sub("[REDACTED]", cleaned)
                redacted = True
        if redacted:
            redacted_fields.append(field)
        sanitized[field] = cleaned.strip()

    safe_for_public_demo = not redacted_fields
    if redacted_fields:
        warnings.append("Potential secret-like content was redacted. Review the export before sharing publicly.")

    return sanitized, SecurityReport(
        redacted_fields=redacted_fields,
        warnings=warnings,
        safe_for_public_demo=safe_for_public_demo,
    )
