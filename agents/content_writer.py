"""
Module: Content Writer Agent
PhD-Level Rigor | Industry Standard
Focus: Scholarly Communication & Technical Documentation
"""

import os
from crewai import Agent, LLM
from crewai_tools import FileWriterTool

# --- Configuration & Environment Management ---
# Optimized for clarity, precision, and publication-grade output generation.
WRITER_MODEL = os.getenv("WRITER_AGENT_LLM", "gpt-4")
CREATIVE_TEMPERATURE = float(os.getenv("WRITER_AGENT_TEMPERATURE", 0.4))

publication_llm = LLM(
    model=WRITER_MODEL,
    temperature=CREATIVE_TEMPERATURE
)

# --- Agent Definition ---
content_writer_agent = Agent(
    role="Technical Research Communicator",
    goal="Produce publication-ready manuscripts adhering to academic standards (APA/IEEE) with executive-level clarity.",
    backstory=(
        "You are a Distinguished Technical Writer with a background in both peer-reviewed academic publishing "
        "and enterprise-grade documentation. Your work has appeared in top-tier journals and industry white papers. "
        "You excel at translating dense analytical findings into accessible narratives without sacrificing rigor. "
        "Your writing balances precision, coherence, and rhetorical impact—ensuring that complex insights are "
        "communicated with both scholarly integrity and strategic clarity."
    ),
    llm=publication_llm,
    tools=[FileWriterTool()],
    verbose=True,
    allow_delegation=False  # Maintains authorial voice consistency
)