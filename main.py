"""
EduGenie: Google Gemini Powered Learning Assistant
Main FastAPI Backend Server
Provides RESTful endpoints connecting the interactive frontend to generative AI modules.
"""

import os
from typing import Any, Dict, Optional
from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

# Import AI modules
import qna
import explanation_module
import quiz_module
import summary_module
import learning_path
import gemini_client

# Initialize FastAPI application
app = FastAPI(
    title="EduGenie AI Learning Assistant",
    description="A lightweight AI-powered educational assistant leveraging Google Gemini & LaMini models.",
    version="1.0.0"
)

# Enable CORS for cross-origin integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure static and template directories exist
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
STATIC_DIR = os.path.join(BASE_DIR, "static")

os.makedirs(TEMPLATES_DIR, exist_ok=True)
os.makedirs(STATIC_DIR, exist_ok=True)

# Mount static files and setup Jinja2 template engine
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
templates = Jinja2Templates(directory=TEMPLATES_DIR)


# Universal Request Model accepting various parameter names seamlessly
class EduGenieRequest(BaseModel):
    prompt: Optional[str] = Field(None, description="Generic input prompt or question")
    text: Optional[str] = Field(None, description="Passage or text input")
    question: Optional[str] = Field(None, description="Academic question")
    concept: Optional[str] = Field(None, description="Concept to explain")
    topic: Optional[str] = Field(None, description="Topic for quiz or learning path")

    def resolve_text(self) -> str:
        """Extract whichever field contains input text."""
        for val in (self.prompt, self.text, self.question, self.concept, self.topic):
            if val is not None and str(val).strip():
                return str(val).strip()
        return ""


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Serve the primary interactive frontend web application."""
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "app_name": "EduGenie",
            "api_configured": gemini_client.is_api_key_configured(),
            "model_name": os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
        }
    )


@app.get("/health")
async def health_check():
    """Health check endpoint displaying system and AI provider configuration."""
    api_key_set = gemini_client.is_api_key_configured()
    use_local_lamini = os.getenv("USE_LOCAL_LAMINI", "false").lower() in ("true", "1", "yes")

    return {
        "status": "healthy",
        "app": "EduGenie Learning Assistant",
        "api_key_configured": api_key_set,
        "gemini_model": os.getenv("GEMINI_MODEL", "gemini-1.5-flash"),
        "explanation_mode": "local (LaMini-Flan-T5)" if use_local_lamini else "cloud (Gemini simplified)",
        "modules": ["qa", "explain", "quiz", "summarize", "learn/recommendations"]
    }


# ==========================================
# 1. Academic Question Answering (QnA)
# ==========================================
@app.post("/qa")
@app.post("/qna")
async def handle_qna(req: EduGenieRequest):
    """Answer general knowledge and academic questions."""
    query = req.resolve_text()
    if not query:
        raise HTTPException(status_code=400, detail="Please provide a question to answer.")
    
    result = qna.answer_question(query)
    return {"query": query, "result": result, "module": "qa"}


# ==========================================
# 2. Concept Explanation Module
# ==========================================
@app.post("/explain")
async def handle_explain(req: EduGenieRequest):
    """Provide simplified, beginner-friendly explanations for complex concepts."""
    concept = req.resolve_text()
    if not concept:
        raise HTTPException(status_code=400, detail="Please provide a concept or topic to explain.")
    
    result = explanation_module.explain_concept(concept)
    return {"concept": concept, "result": result, "module": "explain"}


# ==========================================
# 3. Quiz Generation Module
# ==========================================
@app.post("/quiz")
async def handle_quiz(req: EduGenieRequest):
    """Generate 3 multiple-choice questions (4 options each) in structured JSON."""
    material = req.resolve_text()
    if not material:
        raise HTTPException(status_code=400, detail="Please provide a passage or topic to generate a quiz.")
    
    quiz_data = quiz_module.generate_quiz(material)
    return quiz_data


# ==========================================
# 4. Educational Passage Summarization
# ==========================================
@app.post("/summarize")
async def handle_summarize(req: EduGenieRequest):
    """Condense long educational passages into concise revision summaries."""
    text_content = req.resolve_text()
    if not text_content:
        raise HTTPException(status_code=400, detail="Please provide educational text to summarize.")
    
    result = summary_module.summarize_text(text_content)
    return {"input_length": len(text_content), "result": result, "module": "summarize"}


# ==========================================
# 5. Learning Path Recommendations
# ==========================================
@app.post("/learn/recommendations")
@app.post("/learning-path")
async def handle_learning_path(req: EduGenieRequest):
    """Generate structured beginner-to-advanced learning roadmaps with resources."""
    topic = req.resolve_text()
    if not topic:
        raise HTTPException(status_code=400, detail="Please provide a skill or topic for learning path.")
    
    result = learning_path.get_learning_recommendations(topic)
    return {"topic": topic, "result": result, "module": "learning_path"}


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run("main:app", host="127.0.0.1", port=port, reload=True)
