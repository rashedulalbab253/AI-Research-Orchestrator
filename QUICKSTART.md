# 🚀 Quick Start Guide - MARA Framework

## Multi-Agent Research Assistant - FastAPI + Modern UI

### Prerequisites
- Python 3.9+
- API Keys: GROQ_API_KEY, SERPER_API_KEY

---

## 📦 Installation

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables
```bash
# Copy the template
cp env_template.txt .env

# Edit .env and add your API keys
GROQ_API_KEY=your-groq-api-key-here
SERPER_API_KEY=your-serper-api-key-here
RESEARCH_AGENT_LLM=groq/llama-3.3-70b-versatile
RESEARCH_AGENT_TEMPERATURE=0.1
ANALYST_AGENT_LLM=groq/llama-3.3-70b-versatile
ANALYST_AGENT_TEMPERATURE=0.3
WRITER_AGENT_LLM=groq/llama-3.3-70b-versatile
WRITER_AGENT_TEMPERATURE=0.4
```

---

## 🎯 Running the Application

### Option 1: Web UI (Recommended)
```bash
# Start the FastAPI server
python app.py

# Or with uvicorn directly
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

Then open your browser to: **http://localhost:8000**

### Option 2: Command Line
```bash
python main.py
```

---

## 🌐 API Endpoints

### Health Check
```bash
GET /api/health
```

### Start Research
```bash
POST /api/research/start
Content-Type: application/json

{
  "topic": "Quantum Computing Applications in Drug Discovery"
}
```

### Check Research Status
```bash
GET /api/research/status/{research_id}
```

### Download Results
```bash
GET /api/research/results/research_findings.md
GET /api/research/results/analysis_report.md
GET /api/research/results/final_report.md
```

### WebSocket (Real-time Updates)
```bash
WS /ws/research/{research_id}
```

---

## 📚 API Documentation

Once the server is running, visit:
- **Swagger UI**: http://localhost:8000/api/docs
- **ReDoc**: http://localhost:8000/api/redoc

---

## 🎨 Features

✅ **Modern, Premium UI** - Glassmorphism, gradients, animations  
✅ **Real-time Progress** - WebSocket updates  
✅ **RESTful API** - Production-grade FastAPI backend  
✅ **PhD-Level Research** - Systematic literature review methodology  
✅ **Multi-Agent System** - 3 specialist AI agents  
✅ **Publication-Ready Output** - IMRAD structure, APA/IEEE citations  

---

## 🤖 The Three Agents

1. **🔍 Research Specialist** - Systematic literature review & empirical data acquisition
2. **📊 Data Analyst** - Meta-analysis & statistical synthesis
3. **✍️ Technical Writer** - Publication-ready manuscript production

---

## 📄 Output Files

After research completes, you'll get:

- `research_findings.md` - Systematic research synthesis
- `analysis_report.md` - Meta-analytical report
- `final_report.md` - Publication-ready manuscript

---

## 🛠️ Troubleshooting

### API Keys Not Configured
Make sure your `.env` file has both:
- `GROQ_API_KEY`
- `SERPER_API_KEY`

### Port Already in Use
```bash
# Use a different port
uvicorn app:app --port 8001
```

### WebSocket Connection Failed
- Check firewall settings
- Ensure the server is running
- Try polling fallback (automatic)

---

## 🎓 Built With

- **CrewAI** - Multi-agent orchestration
- **FastAPI** - Modern Python web framework
- **Groq** - High-speed LLM inference
- **Serper** - Web search API
- **HTML/CSS/JS** - Premium frontend

---

**Ready to start?** Run `python app.py` and open http://localhost:8000 🚀
