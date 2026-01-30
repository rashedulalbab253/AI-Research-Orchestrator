"""
Module: Analysis Task Definition
PhD-Level Rigor | Industry Standard
Focus: Meta-Analysis & Statistical Synthesis
"""

import textwrap
from crewai import Task
from agents.data_analyst import data_analyst_agent
from tasks.research_task import research_task

# --- Task Configuration ---
# Implements advanced analytical protocols: pattern recognition, causal inference, and meta-synthesis
analysis_task = Task(
    agent=data_analyst_agent,
    description=textwrap.dedent("""
                Perform meta-analytical synthesis and statistical validation on: {topic}

                Analytical Protocol (Quantitative & Qualitative Rigor):
                1. Ingest and parse structured research artifacts from the prior systematic review
                2. Apply pattern recognition algorithms to identify latent themes and emergent structures
                3. Conduct trend analysis with temporal decomposition (historical context → future trajectories)
                4. Evaluate causal relationships and correlation matrices across multi-source data
                5. Synthesize findings into a coherent knowledge framework with hierarchical insights

                Deliverable Requirements (Analytical Excellence):
                - **Pattern Identification**: Recurring themes, anomalies, and structural relationships
                - **Trend Dynamics**: Historical evolution, current state, and predictive forecasting
                - **Causal Inference**: Mechanistic explanations and dependency mapping
                - **Statistical Validation**: Confidence metrics, effect sizes, and significance testing
                - **Strategic Implications**: Actionable insights with risk-benefit analysis
                """),
    expected_output="A rigorous meta-analytical report with pattern identification, trend dynamics, causal inference, statistical validation, and strategic implications",
    context=[research_task],
    output_file="analysis_report.md"
)