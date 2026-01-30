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

## 🐳 Docker Support

You can also run the MARA Framework using Docker for a consistent, containerized environment.

### 1. Using Docker Compose (Recommended)
This will automatically build the image and start the container with your `.env` file configurations.

```bash
docker-compose up --build
```

### 2. Using Docker Build
If you prefer to build and run the image manually:

```bash
# Build the image
docker build -t mara-framework .

# Run the container
docker run -p 8000:8000 --env-file .env mara-framework
```

Visit **http://localhost:8000** to access the application.

---

## 🚀 CI/CD with GitHub Actions

This project includes a GitHub Action workflow to automatically build and push the Docker image to Docker Hub whenever you push to `main` or `master`.

### Setup Instructions:
1.  **Docker Hub**: Ensure you have an account at [hub.docker.com](https://hub.docker.com).
2.  **GitHub Secrets**: In your GitHub repository, go to **Settings > Secrets and variables > Actions** and add the following:
    -   `DOCKERHUB_USERNAME`: `rashedulalbab1234`
    -   `DOCKERHUB_TOKEN`: Your Docker Hub Personal Access Token (PAT).
3.  **Push**: Once configured, every push to the repository will trigger a build and push to `rashedulalbab1234/ai-research-orchestrator`.

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
