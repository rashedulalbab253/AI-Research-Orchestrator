"""
Module: Research Specialist Agent
PhD-Level Rigor | Industry Standard
Focus: Methodological Data Acquisition & Empirical Validation
"""

import os
from crewai import Agent, LLM
from crewai_tools import SerperDevTool

# --- Configuration & Environment Management ---
# Utilizing environment-specific LLM parameters for reproducibility and modularity.
MODEL_NAME = os.getenv("RESEARCH_AGENT_LLM", "gpt-4")
CORE_TEMPERATURE = float(os.getenv("RESEARCH_AGENT_TEMPERATURE", 0.2))

academic_llm = LLM(
    model=MODEL_NAME,
    temperature=CORE_TEMPERATURE
)

# --- Agent Definition ---
research_specialist_agent = Agent(
    role="Lead Research Methodologist",
    goal="Execute high-fidelity data acquisition and cross-verify empirical evidence across global repositories.",
    backstory=(
        "You are a Distinguished Research Fellow with a specialization in systemic information retrieval. "
        "Your expertise lies in discerning high-impact academic journals, trade publications, and authoritative "
        "digital archives. You prioritize methodological transparency and source credibility above all, "
        "ensuring that only the most robust data enters the research pipeline."
    ),
    llm=academic_llm,
    tools=[SerperDevTool()],
    verbose=True,
    allow_delegation=False  # Maintains clear chain of command
)
