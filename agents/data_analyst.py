"""
Module: Data Analyst Agent
PhD-Level Rigor | Industry Standard
Focus: Statistical Synthesis & Pattern Recognition
"""

import os
from crewai import Agent, LLM
from crewai_tools import FileReadTool

# --- Configuration & Environment Management ---
# Leveraging environment-driven configuration for analytical precision and reproducibility.
ANALYST_MODEL = os.getenv("ANALYST_AGENT_LLM", "gpt-4")
ANALYTICAL_TEMPERATURE = float(os.getenv("ANALYST_AGENT_TEMPERATURE", 0.3))

analytical_llm = LLM(
    model=ANALYST_MODEL,
    temperature=ANALYTICAL_TEMPERATURE
)

# --- Agent Definition ---
data_analyst_agent = Agent(
    role="Senior Quantitative Analyst",
    goal="Synthesize multi-source data into statistically significant insights with causal inference validation.",
    backstory=(
        "You are a Principal Data Scientist with dual expertise in computational statistics and domain research. "
        "Your analytical framework integrates Bayesian reasoning, meta-analytical techniques, and systematic review "
        "protocols. You transform raw research artifacts into structured knowledge graphs, identifying latent patterns, "
        "contradictions, and emergent themes with rigorous methodological transparency."
    ),
    llm=analytical_llm,
    tools=[FileReadTool()],
    verbose=True,
    allow_delegation=False  # Ensures focused analytical integrity
)