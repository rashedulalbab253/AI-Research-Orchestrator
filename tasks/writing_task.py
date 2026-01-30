"""
Module: Writing Task Definition
PhD-Level Rigor | Industry Standard
Focus: Scholarly Manuscript Production & Technical Documentation
"""

import textwrap
from crewai import Task
from agents.content_writer import content_writer_agent
from tasks.analysis_task import analysis_task
from tasks.research_task import research_task

# --- Task Configuration ---
# Produces publication-ready manuscripts adhering to academic and industry standards
writing_task = Task(
    agent=content_writer_agent,
    description=textwrap.dedent("""
                Produce a publication-ready research manuscript on: {topic}

                Writing Protocol (Academic & Executive Standards):
                1. Synthesize research findings and analytical insights into a unified narrative
                2. Structure content following academic conventions (IMRAD: Introduction, Methods, Results, Analysis, Discussion)
                3. Ensure rhetorical clarity for dual audiences: academic peer reviewers and executive stakeholders
                4. Apply citation standards (APA/IEEE) with full bibliographic integrity
                5. Integrate visual abstracts, executive summaries, and decision-support frameworks

                Manuscript Structure (Publication-Grade):
                - **Executive Summary**: High-level synthesis for C-suite and policy makers (max 300 words)
                - **Introduction**: Problem statement, research objectives, and contextual framing
                - **Methodology**: Systematic review protocol and analytical framework employed
                - **Key Findings**: Evidence-based results with statistical validation
                - **Analysis & Discussion**: Interpretation, implications, and theoretical contributions
                - **Conclusions & Recommendations**: Strategic insights with actionable pathways
                - **References**: Full bibliographic citations with DOI/URL provenance
                """),
    expected_output="A publication-ready manuscript with executive summary, IMRAD structure, statistical validation, strategic recommendations, and full bibliographic references",
    context=[research_task, analysis_task],
    output_file="final_report.md"
)