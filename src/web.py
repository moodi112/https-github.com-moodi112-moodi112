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
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
                line-height: 1.7;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: #333;
                min-height: 100vh;
            }
            .container {
                max-width: 1100px;
                margin: 0 auto;
                padding: 60px 40px;
            }
            .hero {
                background: white;
                padding: 80px 60px;
                border-radius: 20px;
                box-shadow: 0 25px 80px rgba(0,0,0,0.3);
                margin-bottom: 40px;
            }
            .hero h1 {
                font-size: 3.5em;
                color: #667eea;
                margin-bottom: 15px;
                font-weight: 800;
                letter-spacing: -1px;
            }
            .hero .tagline {
                font-size: 1.4em;
                color: #764ba2;
                margin-bottom: 30px;
                font-weight: 600;
                font-style: italic;
            }
            .hero .description {
                font-size: 1.1em;
                color: #555;
                line-height: 1.8;
                margin-bottom: 30px;
            }
            .hero .description strong {
                color: #667eea;
            }
            .cta-box {
                background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
                color: white;
                padding: 40px;
                border-radius: 15px;
                margin: 40px 0;
                text-align: center;
            }
            .cta-box h2 {
                font-size: 2em;
                margin-bottom: 20px;
            }
            .cta-box p {
                font-size: 1.2em;
                margin-bottom: 30px;
                opacity: 0.95;
            }
            .cta-buttons {
                display: flex;
                gap: 20px;
                justify-content: center;
                flex-wrap: wrap;
            }
            .btn {
                display: inline-block;
                padding: 15px 35px;
                background: white;
                color: #764ba2;
                text-decoration: none;
                border-radius: 8px;
                font-weight: 700;
                font-size: 1.1em;
                transition: all 0.3s ease;
                box-shadow: 0 4px 15px rgba(0,0,0,0.2);
            }
            .btn:hover {
                transform: translateY(-3px);
                box-shadow: 0 6px 25px rgba(0,0,0,0.3);
            }
            .features {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                gap: 30px;
                margin: 40px 0;
            }
            .feature-card {
                background: white;
                padding: 40px;
                border-radius: 15px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.2);
                transition: transform 0.3s ease;
            }
            .feature-card:hover {
                transform: translateY(-5px);
            }
            .feature-card h3 {
                color: #667eea;
                font-size: 1.5em;
                margin-bottom: 15px;
                display: flex;
                align-items: center;
                gap: 10px;
            }
            .feature-card ul {
                list-style: none;
                padding: 0;
            }
            .feature-card li {
                padding: 8px 0;
                padding-left: 25px;
                position: relative;
            }
            .feature-card li:before {
                content: "→";
                position: absolute;
                left: 0;
                color: #764ba2;
                font-weight: bold;
            }
            .endpoint {
                font-family: 'Courier New', monospace;
                background: #f0f0f0;
                padding: 4px 10px;
                border-radius: 5px;
                font-size: 0.9em;
                color: #764ba2;
            }
            .footer {
                background: white;
                padding: 40px;
                border-radius: 15px;
                text-align: center;
                margin-top: 40px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            }
            .footer p {
                color: #666;
                font-size: 1em;
            }
            .footer .legacy {
                color: #764ba2;
                font-weight: 600;
                font-style: italic;
                margin-top: 10px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="hero">
                <h1>🇴🇲 Oman Wikipedia Generator</h1>
                <p class="tagline">Document Oman. One API call at a time.</p>
                <div class="description">
                    <p>Oman has stories worth archiving — festivals that shaped a decade, venues that defined a generation, and creators who carried the culture. This engine captures all of it.</p>
                    <br>
                    <p>Meet the <strong>AI-powered Wikipedia generator</strong> built for <strong>Oman's events, history, and cultural ecosystem</strong>. Fast. Neutral. Ministry-friendly. Encyclopedia-clean.</p>
                </div>
            </div>

            <div class="cta-box">
                <h2>Ready to Deploy?</h2>
                <p>Your legacy is one request away.</p>
                <div class="cta-buttons">
                    <a href="/docs" class="btn">📖 API Docs</a>
                    <a href="/examples" class="btn">💡 Examples</a>
                    <a href="/redoc" class="btn">📚 ReDoc</a>
                </div>
            </div>

            <div class="features">
                <div class="feature-card">
                    <h3>🚀 What It Does</h3>
                    <ul>
                        <li>Generates <strong>full Wikipedia-style articles</strong></li>
                        <li>Builds <strong>infoboxes</strong> like a seasoned archivist</li>
                        <li>Summarizes content for <strong>press, decks, media</strong></li>
                        <li>Outputs <strong>Markdown, HTML, and PDF</strong></li>
                        <li>Handles <strong>English + Arabic</strong> fluently</li>
                    </ul>
                </div>

                <div class="feature-card">
                    <h3>🧩 Who It's For</h3>
                    <ul>
                        <li>Event organizers</li>
                        <li>Venues</li>
                        <li>Government cultural departments</li>
                        <li>Archivists</li>
                        <li>Journalists</li>
                        <li>Agencies & media teams</li>
                    </ul>
                    <p style="margin-top: 20px; color: #666; font-style: italic;">If you shape the culture, this API documents it.</p>
                </div>

                <div class="feature-card">
                    <h3>📦 The Stack</h3>
                    <ul>
                        <li><span class="endpoint">/generate/article</span> → Full article</li>
                        <li><span class="endpoint">/generate/summary</span> → Executive intro</li>
                        <li><span class="endpoint">/generate/infobox</span> → Structured data</li>
                        <li><span class="endpoint">/generate/full</span> → The complete pack</li>
                        <li><span class="endpoint">/batch/generate</span> → Bulk creation</li>
                        <li><span class="endpoint">/export</span> → Clean output-ready files</li>
                    </ul>
                </div>
            </div>

            <div class="footer">
                <p>🏛️ <strong>Built with Respect</strong></p>
                <p>Omani heritage at the foundation. Modern automation at the edge.</p>
                <p class="legacy">Your narrative — preserved with precision.</p>
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
