"""
FastAPI web interface for Oman Wikipedia Generator.
"""
from fastapi import FastAPI, HTTPException, BackgroundTasks, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse
from pydantic import BaseModel, Field
from typing import Optional, List, Dict
import os
import tempfile
from src.wiki_generator import WikiGenerator
from src.exporters import ExportFormatter, BatchExporter


app = FastAPI(
    title="Oman Wikipedia Generator API",
    description="Generate Wikipedia-style articles about Oman events using AI",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize generator
generator = None


def get_generator():
    """Get or create WikiGenerator instance."""
    global generator
    if generator is None:
        generator = WikiGenerator()
    return generator


# Pydantic models
class ArticleRequest(BaseModel):
    event_name: str = Field(..., description="Name of the Oman event")
    context: Optional[str] = Field(None, description="Additional context about the event")
    style: str = Field("formal", description="Writing style: formal, casual, or detailed")
    language: str = Field("en", description="Output language: en (English) or ar (Arabic)")


class SummaryRequest(BaseModel):
    event_name: str = Field(..., description="Name of the Oman event")
    max_length: int = Field(200, description="Maximum words in summary")
    language: str = Field("en", description="Output language: en or ar")


class InfoboxRequest(BaseModel):
    event_name: str = Field(..., description="Name of the Oman event")
    language: str = Field("en", description="Output language: en or ar")


class BatchRequest(BaseModel):
    event_names: List[str] = Field(..., description="List of event names")
    output_type: str = Field("article", description="Type: article, summary, or infobox")
    language: str = Field("en", description="Output language")


class ExportRequest(BaseModel):
    article: str = Field(..., description="Article content to export")
    title: str = Field(..., description="Article title")
    format: str = Field("html", description="Export format: markdown, html, or pdf")
    infobox: Optional[str] = None
    summary: Optional[str] = None
    style: str = Field("wikipedia", description="HTML style theme")


# Routes
@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve homepage."""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Oman Wikipedia Generator</title>
        <style>
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
                max-width: 1200px;
                margin: 0 auto;
                padding: 40px 20px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: #333;
            }
            .container {
                background: white;
                padding: 60px;
                border-radius: 15px;
                box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            }
            h1 {
                color: #667eea;
                font-size: 3em;
                margin-bottom: 10px;
            }
            .subtitle {
                color: #666;
                font-size: 1.2em;
                margin-bottom: 40px;
            }
            .card {
                background: #f8f9fa;
                padding: 25px;
                margin: 20px 0;
                border-radius: 10px;
                border-left: 4px solid #667eea;
            }
            .endpoint {
                font-family: 'Courier New', monospace;
                background: #e9ecef;
                padding: 3px 8px;
                border-radius: 4px;
            }
            a {
                color: #667eea;
                text-decoration: none;
            }
            a:hover {
                text-decoration: underline;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🇴🇲 Oman Wikipedia Generator</h1>
            <p class="subtitle">AI-powered Wikipedia article generation for Oman events</p>
            
            <div class="card">
                <h3>📖 API Documentation</h3>
                <p>Interactive API documentation: <a href="/docs">/docs</a></p>
                <p>Alternative docs: <a href="/redoc">/redoc</a></p>
            </div>
            
            <div class="card">
                <h3>🚀 Available Endpoints</h3>
                <ul>
                    <li><strong>POST</strong> <span class="endpoint">/generate/article</span> - Generate full article</li>
                    <li><strong>POST</strong> <span class="endpoint">/generate/summary</span> - Generate summary</li>
                    <li><strong>POST</strong> <span class="endpoint">/generate/infobox</span> - Generate infobox</li>
                    <li><strong>POST</strong> <span class="endpoint">/generate/full</span> - Generate complete package</li>
                    <li><strong>POST</strong> <span class="endpoint">/batch/generate</span> - Batch generation</li>
                    <li><strong>POST</strong> <span class="endpoint">/export</span> - Export to formats</li>
                </ul>
            </div>
            
            <div class="card">
                <h3>🌐 Supported Languages</h3>
                <p>English (en) • Arabic (ar)</p>
            </div>
            
            <div class="card">
                <h3>📦 Export Formats</h3>
                <p>Markdown • HTML • PDF</p>
            </div>
        </div>
    </body>
    </html>
    """


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "oman-wiki-generator"}


@app.post("/generate/article")
async def generate_article(request: ArticleRequest):
    """Generate a Wikipedia-style article."""
    try:
        gen = get_generator()
        article = gen.generate_wiki_article(
            event_name=request.event_name,
            context=request.context,
            style=request.style,
            language=request.language
        )
        return {
            "success": True,
            "event_name": request.event_name,
            "article": article,
            "language": request.language
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/generate/summary")
async def generate_summary(request: SummaryRequest):
    """Generate a summary of an event."""
    try:
        gen = get_generator()
        summary = gen.generate_summary(
            event_name=request.event_name,
            max_length=request.max_length,
            language=request.language
        )
        return {
            "success": True,
            "event_name": request.event_name,
            "summary": summary,
            "language": request.language
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/generate/infobox")
async def generate_infobox(request: InfoboxRequest):
    """Generate an infobox for an event."""
    try:
        gen = get_generator()
        infobox = gen.generate_infobox(
            event_name=request.event_name,
            language=request.language
        )
        return {
            "success": True,
            "event_name": request.event_name,
            "infobox": infobox,
            "language": request.language
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/generate/full")
async def generate_full(request: ArticleRequest):
    """Generate complete package: article, summary, and infobox."""
    try:
        gen = get_generator()
        
        article = gen.generate_wiki_article(
            event_name=request.event_name,
            context=request.context,
            style=request.style,
            language=request.language
        )
        
        summary = gen.generate_summary(
            event_name=request.event_name,
            language=request.language
        )
        
        infobox = gen.generate_infobox(
            event_name=request.event_name,
            language=request.language
        )
        
        return {
            "success": True,
            "event_name": request.event_name,
            "article": article,
            "summary": summary,
            "infobox": infobox,
            "language": request.language
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/batch/generate")
async def batch_generate(request: BatchRequest, background_tasks: BackgroundTasks):
    """Generate content for multiple events in batch."""
    try:
        gen = get_generator()
        
        results = gen.batch_generate(
            event_names=request.event_names,
            output_type=request.output_type,
            language=request.language
        )
        
        return {
            "success": True,
            "output_type": request.output_type,
            "language": request.language,
            "count": len(results),
            "results": results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/export")
async def export_article(request: ExportRequest):
    """Export article to specified format."""
    try:
        if request.format == "markdown":
            content = ExportFormatter.to_markdown(
                article=request.article,
                title=request.title,
                infobox=request.infobox,
                summary=request.summary
            )
            return {
                "success": True,
                "format": "markdown",
                "content": content
            }
        
        elif request.format == "html":
            content = ExportFormatter.to_html(
                article=request.article,
                title=request.title,
                infobox=request.infobox,
                summary=request.summary,
                style=request.style
            )
            return {
                "success": True,
                "format": "html",
                "content": content
            }
        
        elif request.format == "pdf":
            # Create temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
                pdf_path = tmp.name
            
            ExportFormatter.to_pdf(
                article=request.article,
                title=request.title,
                output_path=pdf_path,
                infobox=request.infobox,
                summary=request.summary
            )
            
            return FileResponse(
                pdf_path,
                media_type="application/pdf",
                filename=f"{request.title}.pdf"
            )
        
        else:
            raise HTTPException(status_code=400, detail=f"Unsupported format: {request.format}")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/languages")
async def get_languages():
    """Get supported languages."""
    gen = get_generator()
    return {
        "supported_languages": gen.SUPPORTED_LANGUAGES
    }


@app.get("/examples")
async def get_examples():
    """Get example Oman events for generation."""
    examples = [
        {"name": "Muscat Festival", "description": "Annual cultural and shopping festival"},
        {"name": "Salalah Tourism Festival", "description": "Summer festival in Dhofar"},
        {"name": "National Day of Oman", "description": "November 18th celebration"},
        {"name": "Renaissance Day", "description": "July 23rd commemoration"},
        {"name": "Oman Desert Marathon", "description": "Annual desert running event"},
        {"name": "Muscat International Book Fair", "description": "Literary event"},
        {"name": "Khareef Season", "description": "Monsoon season in Salalah"},
        {"name": "Oman Traditional Crafts Festival", "description": "Handicrafts showcase"},
    ]
    return {"examples": examples}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
