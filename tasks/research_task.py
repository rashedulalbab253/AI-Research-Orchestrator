"""
Module: Research Task Definition
PhD-Level Rigor | Industry Standard
Focus: Systematic Literature Review & Empirical Data Acquisition
"""

import textwrap
from crewai import Task
from agents.research_specialist import research_specialist_agent

# --- Task Configuration ---
# Defines the systematic research protocol following PRISMA-like methodology
research_task = Task(
    agent=research_specialist_agent,
    description=textwrap.dedent("""
                Execute a systematic literature review and empirical data acquisition on: {topic}

                Research Protocol (Methodological Rigor):
                1. Conduct multi-database searches (academic journals, industry reports, authoritative repositories)
                2. Apply source triangulation to cross-verify factual claims
                3. Extract quantitative metrics, qualitative insights, and expert consensus
                4. Organize findings using structured knowledge frameworks (taxonomies, ontologies)
                5. Validate temporal relevance and methodological soundness of all sources

                Deliverable Requirements (Publication-Grade):
                - **Key Findings**: Evidence-backed claims with citation trails
                - **Statistical Evidence**: Quantitative data with confidence intervals where applicable
                - **Expert Consensus**: Peer-reviewed opinions and industry thought leadership
                - **Temporal Analysis**: Recent developments, emerging trends, and trajectory forecasts
                - **Source Provenance**: Full bibliographic references with credibility assessment
                """),
    expected_output="A systematic research synthesis with empirical evidence, statistical validation, expert consensus, temporal analysis, and full source provenance",
    output_file="research_findings.md"
)