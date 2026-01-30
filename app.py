

from dotenv import load_dotenv
# Load environment variables explicitly before importing agents
load_dotenv()

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse, RedirectResponse
from pydantic import BaseModel, Field
from typing import Optional, List
import os
import asyncio
from datetime import datetime
from crew import research_crew
import json

# Initialize FastAPI application
app = FastAPI(
    title="Multi-Agent Research Assistant API",
    description="PhD-Level Research Automation with CrewAI",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# CORS Configuration - Allow frontend to communicate
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files (frontend)
app.mount("/static", StaticFiles(directory="static"), name="static")


# --- Pydantic Models ---
class ResearchRequest(BaseModel):
    topic: str = Field(..., min_length=3, max_length=500, description="Research topic to investigate")
    
    class Config:
        json_schema_extra = {
            "example": {
                "topic": "Quantum Computing Applications in Drug Discovery"
            }
        }


class ResearchResponse(BaseModel):
    status: str
    message: str
    research_id: Optional[str] = None
    timestamp: str


class ResearchStatus(BaseModel):
    research_id: str
    status: str
    progress: int
    current_agent: Optional[str] = None
    message: str


class FileDownloadResponse(BaseModel):
    filename: str
    content: str
    size_bytes: int


# --- Global State Management ---
active_research_sessions = {}


# --- API Endpoints ---

@app.get("/docs", include_in_schema=False)
async def docs_redirect():
    return RedirectResponse(url="/api/docs")


@app.get("/")
async def serve_frontend():
    """Serve the main HTML frontend"""
    return FileResponse(os.path.join("static", "index.html"))


@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    missing_keys = []
    required_keys = ['SERPER_API_KEY', 'GROQ_API_KEY']
    
    for key in required_keys:
        if not os.getenv(key):
            missing_keys.append(key)
    
    return {
        "status": "healthy" if not missing_keys else "degraded",
        "timestamp": datetime.now().isoformat(),
        "api_keys_configured": len(missing_keys) == 0,
        "missing_keys": missing_keys,
        "version": "1.0.0"
    }


@app.post("/api/research/start", response_model=ResearchResponse)
async def start_research(request: ResearchRequest):
    """
    Initiate a new research task
    Returns a research_id for tracking progress
    """
    # Validate API keys
    if not os.getenv('SERPER_API_KEY') or not os.getenv('GROQ_API_KEY'):
        raise HTTPException(
            status_code=503,
            detail="API keys not configured. Please set SERPER_API_KEY and GROQ_API_KEY in .env file"
        )
    
    # Generate unique research ID
    research_id = f"research_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    # Store in active sessions
    active_research_sessions[research_id] = {
        "topic": request.topic,
        "status": "queued",
        "progress": 0,
        "started_at": datetime.now().isoformat()
    }
    
    # Start research in background
    asyncio.create_task(execute_research(research_id, request.topic))
    
    return ResearchResponse(
        status="success",
        message="Research task initiated successfully",
        research_id=research_id,
        timestamp=datetime.now().isoformat()
    )


async def execute_research(research_id: str, topic: str):
    """
    Execute research task asynchronously
    Updates session state as it progresses
    """
    try:
        # Update status
        active_research_sessions[research_id]["status"] = "running"
        active_research_sessions[research_id]["progress"] = 10
        active_research_sessions[research_id]["current_agent"] = "Research Specialist"
        
        # Run the crew
        result = await asyncio.to_thread(
            research_crew.kickoff,
            {"topic": topic}
        )
        
        # Update completion status
        active_research_sessions[research_id]["status"] = "completed"
        active_research_sessions[research_id]["progress"] = 100
        active_research_sessions[research_id]["result"] = str(result)
        active_research_sessions[research_id]["completed_at"] = datetime.now().isoformat()
        
    except Exception as e:
        active_research_sessions[research_id]["status"] = "failed"
        active_research_sessions[research_id]["error"] = str(e)
        active_research_sessions[research_id]["failed_at"] = datetime.now().isoformat()


@app.get("/api/research/status/{research_id}", response_model=ResearchStatus)
async def get_research_status(research_id: str):
    """
    Get the current status of a research task
    """
    if research_id not in active_research_sessions:
        raise HTTPException(status_code=404, detail="Research ID not found")
    
    session = active_research_sessions[research_id]
    
    return ResearchStatus(
        research_id=research_id,
        status=session["status"],
        progress=session.get("progress", 0),
        current_agent=session.get("current_agent"),
        message=f"Research on '{session['topic']}' is {session['status']}"
    )


@app.get("/api/manuscripts")
async def list_manuscripts():
    """
    List all available research manuscripts (markdown files)
    """
    files = []
    # Identify system files to exclude
    system_files = ["README.md", "QUICKSTART.md", "SETUP_COMPLETE.md", "requirements.txt"]
    
    try:
        # Scan current directory
        for filename in os.listdir("."):
            # Filter logic: .md files OR files containing "manuscript"/"report"
            is_md = filename.lower().endswith(".md")
            is_relevant_name = "manuscript" in filename.lower() or "report" in filename.lower()
            
            if (is_md or is_relevant_name) and filename not in system_files:
                if not os.path.isfile(filename):
                     continue
                     
                stats = os.stat(filename)
                files.append({
                    "filename": filename,
                    "created_at": datetime.fromtimestamp(stats.st_mtime).isoformat(),
                    "size_bytes": stats.st_size,
                    "type": "report" if is_relevant_name else "data"
                })
        
        # Sort by modification time (newest first)
        files.sort(key=lambda x: x["created_at"], reverse=True)
        return {"manuscripts": files}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/research/results/{filename}")
async def get_research_file(filename: str):
    """
    Download research output files
    Now supports dynamic filenames generated by agents
    """
    # Security: Prevent directory traversal and system file access
    safe_filename = os.path.basename(filename)
    if safe_filename != filename:
         raise HTTPException(status_code=400, detail="Invalid filename security check")
         
    # Block downloading system/source files
    blocked_extensions = ['.py', '.pyc', '.env', '.gitignore', '.txt']
    blocked_files = ["requirements.txt", "README.md", "QUICKSTART.md", "SETUP_COMPLETE.md"]
    
    ext = os.path.splitext(safe_filename)[1].lower()
    if ext in blocked_extensions or safe_filename in blocked_files or safe_filename.startswith('.'):
         raise HTTPException(status_code=403, detail="Access denied to this file type")
    
    if not os.path.exists(safe_filename):
        raise HTTPException(status_code=404, detail="File not found.")
    
    try:
        with open(safe_filename, 'r', encoding='utf-8') as f:
            content = f.read()
        
        return FileDownloadResponse(
            filename=safe_filename,
            content=content,
            size_bytes=len(content.encode('utf-8'))
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading file: {str(e)}")


@app.get("/api/research/list")
async def list_research_sessions():
    """
    List all research sessions
    """
    return {
        "total_sessions": len(active_research_sessions),
        "sessions": [
            {
                "research_id": rid,
                "topic": session["topic"],
                "status": session["status"],
                "started_at": session["started_at"]
            }
            for rid, session in active_research_sessions.items()
        ]
    }


# --- WebSocket for Real-time Updates ---
@app.websocket("/ws/research/{research_id}")
async def websocket_research_updates(websocket: WebSocket, research_id: str):
    """
    WebSocket endpoint for real-time research progress updates
    """
    await websocket.accept()
    
    try:
        while True:
            if research_id in active_research_sessions:
                session = active_research_sessions[research_id]
                await websocket.send_json({
                    "research_id": research_id,
                    "status": session["status"],
                    "progress": session.get("progress", 0),
                    "current_agent": session.get("current_agent", ""),
                    "timestamp": datetime.now().isoformat()
                })
                
                # If completed or failed, close connection
                if session["status"] in ["completed", "failed"]:
                    await websocket.close()
                    break
            
            await asyncio.sleep(2)  # Update every 2 seconds
            
    except WebSocketDisconnect:
        print(f"WebSocket disconnected for research_id: {research_id}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
