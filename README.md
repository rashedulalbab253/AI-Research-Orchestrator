# 🔬 MARA-Framework: Multi-Agent Research Assistant

A modular, multi-agent research pipeline powered by [CrewAI](https://github.com/joaomdmoura/crewAI). This project automates systematic literature reviews, data synthesis, and publication-ready report generation—each handled by a specialist AI agent for PhD-level rigor and industry-standard output.

---

## 🚀 Key Features

- **Automated, Multi-Step Research Workflow**: From initial discovery to final manuscript.
- **PhD-Level Specialist Agents**: Custom-built personas for Research, Data Analysis, and Technical Writing.
- **Modern Premium UI**: Stunning Glassmorphism interface for real-time tracking.
- **RESTful API & WebSockets**: Production-ready FastAPI backend.
- **Methodological Rigor**: Built-in adherence to PRISMA and IMRAD standards.

---

## 🗂️ Project Structure

```
.
├── agents/             # PhD-level agent definitions
├── tasks/              # Systematic task protocols
├── static/             # Modern UI assets (HTML, CSS, JS)
├── app.py              # FastAPI Backend Server
├── crew.py             # Multi-agent orchestration
├── main.py             # CLI Entrypoint
├── QUICKSTART.md       # Interactive setup guide
└── SETUP_COMPLETE.md   # System architecture & documentation
```

---

## ⚙️ Quick Start

### 1. Installation
```bash
pip install -r requirements.txt
```

### 2. Configure Environment
Copy `env_template.txt` to `.env` and add your `GROQ_API_KEY` and `SERPER_API_KEY`.

### 3. Launch the Platform
```bash
python app.py
```
Visit **http://localhost:8000** to start your systematic research.

---

## 🕵️ AI Agent Squad

1. **🔍 Lead Research Methodologist**: Executes high-fidelity data acquisition and empirical validation.
2. **📊 Senior Quantitative Analyst**: Performs meta-analytical synthesis and statistical validation.
3. **✍️ Technical Research Communicator**: Produces publication-ready manuscripts with executive-level clarity.

---

## 📄 Scholarly Outputs

- `research_findings.md` — Systematic literature review
- `analysis_report.md` — Meta-analytical review
- `final_report.md` — Polished, IMRAD-structured manuscript

---

## 🛠️ Built With

- **CrewAI** - Agent Orchestration
- **FastAPI** - Backend Framework
- **Groq** - LLM Inference
- **Vanilla CSS** - Design System

---

## 🤝 Credits

Project developed by [rashedulalbab253](https://github.com/rashedulalbab253)

*Empowering researchers with autonomous agentic intelligence.*
