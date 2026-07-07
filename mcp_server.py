from __future__ import annotations

from mcp.server.fastmcp import FastMCP

from hardware_npi_ideation.knowledge import NPIKnowledgeServer


mcp = FastMCP("hardware-npi-knowledge")
knowledge = NPIKnowledgeServer()


@mcp.tool()
def get_npi_phases() -> list[dict[str, object]]:
    """Return hardware NPI phases, typical durations, activities, and gate outputs."""
    return knowledge.get_npi_phases()


@mcp.tool()
def get_requirement_taxonomy() -> list[str]:
    """Return requirement categories used by the NPI intake workflow."""
    return knowledge.get_requirement_taxonomy()


@mcp.tool()
def common_ambiguous_terms() -> list[str]:
    """Return early hardware planning terms that should be made measurable."""
    return knowledge.common_ambiguous_terms()


@mcp.tool()
def lookup_definition(term: str) -> str:
    """Return a measurable working-definition strategy for an ambiguous term."""
    return knowledge.lookup_definition(term)


if __name__ == "__main__":
    mcp.run()
