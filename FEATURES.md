# Features Documentation

Comprehensive guide to all features in the Oman Wikipedia Generator.

## Table of Contents

- [Multi-Language Support](#multi-language-support)
- [Batch Processing](#batch-processing)
- [Export Formats](#export-formats)
- [Image Generation](#image-generation)
- [Citation Validation](#citation-validation)
- [Web Interface](#web-interface)
- [CI/CD Pipeline](#cicd-pipeline)
- [Security Features](#security-features)
- [Docker Support](#docker-support)

## Multi-Language Support

Generate Wikipedia articles in multiple languages.

### Supported Languages

- **English (en)** - Default language
- **Arabic (ar)** - Native Omani language

### Usage

**CLI:**
```bash
# English article
python -m src.cli article "Muscat Festival" --language en

# Arabic article  
python -m src.cli article "مهرجان مسقط" --language ar

# Summary in Arabic
python -m src.cli summary "اليوم الوطني" --language ar --max-length 150
```

**API:**
```python
from src.wiki_generator import WikiGenerator

generator = WikiGenerator()

# English
article_en = generator.generate_wiki_article("Muscat Festival", language="en")

# Arabic
article_ar = generator.generate_wiki_article("مهرجان مسقط", language="ar")
```

**Web API:**
```bash
curl -X POST "http://localhost:8000/generate/article" \
  -H "Content-Type: application/json" \
  -d '{"event_name": "Muscat Festival", "language": "ar"}'
```

## Batch Processing

Generate content for multiple events in a single operation.

### Features

- Process multiple events from command line
- Load events from file
- Support all content types (article, summary, infobox)
- Export in various formats
- Progress tracking

### Usage

**From command line:**
```bash
python -m src.cli batch \
  -e "Muscat Festival" \
  -e "National Day" \
  -e "Salalah Tourism Festival" \
  --type article \
  --language en \
  --output-dir ./batch_output \
  --export-format html
```

**From file:**
```bash
# Create events.txt with one event per line
echo "Muscat Festival" > events.txt
echo "National Day of Oman" >> events.txt
echo "Renaissance Day" >> events.txt

# Process batch
python -m src.cli batch \
  --file events.txt \
  --type summary \
  --output-dir ./summaries \
  --export-format markdown
```

**API:**
```python
from src.wiki_generator import WikiGenerator

generator = WikiGenerator()

events = ["Muscat Festival", "National Day", "Salalah Festival"]
results = generator.batch_generate(
    event_names=events,
    output_type="article",
    language="en"
)

for event, content in results.items():
    print(f"Generated: {event}")
```

## Export Formats

Export generated articles in multiple formats.

### Supported Formats

1. **Text** - Plain text format
2. **Markdown** - With proper formatting and structure
3. **HTML** - Three style themes (Wikipedia, Modern, Minimal)
4. **PDF** - Professional documents with formatting

### Usage

**Text Export:**
```bash
python -m src.cli article "Muscat Festival" \
  --format text \
  --output article.txt
```

**Markdown Export:**
```bash
python -m src.cli article "National Day" \
  --format markdown \
  --output article.md
```

**HTML Export:**
```bash
python -m src.cli full "Muscat Festival" \
  --format html \
  --output article.html
```

**PDF Export:**
```bash
python -m src.cli full "Salalah Festival" \
  --format pdf \
  --output article.pdf
```

### HTML Themes

**Wikipedia Style:**
- Classic Wikipedia appearance
- Familiar reading experience
- Professional layout

**Modern Style:**
- Gradient backgrounds
- Modern typography
- Colorful design

**Minimal Style:**
- Clean and simple
- Maximum readability
- Distraction-free

**API Usage:**
```python
from src.exporters import ExportFormatter

# HTML with custom theme
html = ExportFormatter.to_html(
    article="Article content...",
    title="Muscat Festival",
    style="modern"  # or "wikipedia", "minimal"
)

# PDF
ExportFormatter.to_pdf(
    article="Article content...",
    title="Muscat Festival",
    output_path="output.pdf",
    infobox="Infobox content...",
    summary="Summary content..."
)
```

## Image Generation

Generate DALL-E image prompts for events.

### Features

- Automatic image prompt generation
- Culturally appropriate descriptions
- Optimized for DALL-E
- Multi-language support

### Usage

**CLI:**
```bash
python -m src.cli image-prompt "Muscat Festival" \
  --context "Annual cultural and shopping event" \
  --language en
```

**API:**
```python
from src.wiki_generator import WikiGenerator

generator = WikiGenerator()
result = generator.generate_with_image(
    event_name="Muscat Festival",
    context="Major winter festival",
    language="en"
)

print("Image Prompt:", result["image_prompt"])
print("Article:", result["article"])
```

### Using with DALL-E

Take the generated image prompt and use it with DALL-E:

```python
from openai import OpenAI

client = OpenAI()

# Get image prompt
generator = WikiGenerator()
result = generator.generate_with_image("Muscat Festival")

# Generate image with DALL-E
response = client.images.generate(
    model="dall-e-3",
    prompt=result["image_prompt"],
    size="1024x1024",
    quality="standard",
    n=1
)

image_url = response.data[0].url
```

## Citation Validation

Extract and validate citations from generated articles.

### Features

- Automatic citation extraction
- Basic validation checks
- Reference section parsing
- Multi-language support

### Usage

**Extract Citations:**
```python
from src.wiki_generator import WikiGenerator

generator = WikiGenerator()
article = generator.generate_wiki_article("Muscat Festival")

# Extract citations
citations = generator.extract_citations(article)
for citation in citations:
    print(citation)
```

**Validate Citations:**
```python
# Validate extracted citations
validation = generator.validate_citations(citations)

for citation, is_valid in validation.items():
    status = "✓ Valid" if is_valid else "✗ Invalid"
    print(f"{status}: {citation[:100]}...")
```

### Validation Checks

- Has year reference (4-digit number)
- Proper punctuation
- Minimum length (substantial content)
- Quote marks present

## Web Interface

FastAPI-based web interface with REST API.

### Features

- Interactive API documentation
- RESTful endpoints
- Real-time generation
- CORS support
- Health checks
- Example events

### Starting the Server

**Development:**
```bash
uvicorn src.web:app --reload --host 0.0.0.0 --port 8000
```

**Production:**
```bash
uvicorn src.web:app --host 0.0.0.0 --port 8000 --workers 4
```

**Docker:**
```bash
docker-compose up wiki-web
```

### API Endpoints

**Homepage:**
- `GET /` - Interactive homepage

**Generation:**
- `POST /generate/article` - Generate full article
- `POST /generate/summary` - Generate summary
- `POST /generate/infobox` - Generate infobox
- `POST /generate/full` - Generate complete package

**Batch:**
- `POST /batch/generate` - Batch generation

**Export:**
- `POST /export` - Export to formats

**Utilities:**
- `GET /health` - Health check
- `GET /languages` - Supported languages
- `GET /examples` - Example events

### API Documentation

Access interactive docs at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Example Request

```bash
curl -X POST "http://localhost:8000/generate/article" \
  -H "Content-Type: application/json" \
  -d '{
    "event_name": "Muscat Festival",
    "context": "Annual cultural event",
    "style": "formal",
    "language": "en"
  }'
```

## CI/CD Pipeline

Automated testing, security scanning, and deployment.

### Pipeline Jobs

1. **Lint** 📝
   - Black formatting check
   - Flake8 linting
   - Code quality verification

2. **Test** 🧪
   - Matrix testing (Ubuntu, macOS, Windows)
   - Python 3.9, 3.10, 3.11
   - JUnit XML reports
   - Artifact uploads

3. **Security** 🔒
   - Bandit security scanning
   - Safety dependency checks
   - Vulnerability reports

4. **Coverage** 📊
   - Test coverage analysis
   - Codecov integration
   - Coverage reports

5. **Docker** 🐳
   - Docker build verification
   - Container testing

### Workflow Triggers

- Push to any branch
- Pull requests
- Manual workflow dispatch

### Notifications

Automated notifications to:
- Slack webhooks
- Microsoft Teams webhooks

### Setup Requirements

Configure in GitHub Secrets:
- `SLACK_WEBHOOK_URL`
- `TEAMS_WEBHOOK_URL`
- `CODECOV_TOKEN`

## Security Features

Comprehensive security measures.

### Pre-commit Hooks

Automated checks before commit:
- Code formatting (Black)
- Linting (Flake8)
- Security scanning (Bandit)
- Import sorting (isort)
- Syntax upgrades (pyupgrade)
- File checks (trailing whitespace, large files, etc.)

**Setup:**
```bash
pip install pre-commit
pre-commit install
```

**Run manually:**
```bash
pre-commit run --all-files
```

### Security Scanning

**Bandit - Code Security:**
```bash
bandit -r src/
```

**Safety - Dependency Vulnerabilities:**
```bash
safety check
```

### Security Best Practices

- Environment variable for API keys
- No hardcoded secrets
- CORS configuration
- Input validation
- Error handling
- Secure defaults

## Docker Support

Full containerization support for all components.

### Available Images

**CLI Application:**
```bash
docker run oman-wiki-generator python -m src.cli article "Event"
```

**Web Interface:**
```bash
docker run -p 8000:8000 oman-wiki-generator:web
```

**Test Runner:**
```bash
docker-compose run test
```

### Docker Compose Services

- `wiki-generator` - CLI application
- `wiki-web` - Web interface
- `test` - Test runner

### Features

- Multi-stage builds for optimization
- Non-root user for security
- Health checks
- Volume mounts for output
- Environment variable support
- Network isolation

### Usage Examples

**Build:**
```bash
docker build -t oman-wiki-generator .
```

**Run with environment:**
```bash
docker run --rm \
  -e OPENAI_API_KEY=your_key \
  -e OPENAI_MODEL=gpt-4 \
  -v $(pwd)/output:/app/output \
  oman-wiki-generator \
  python -m src.cli article "Muscat Festival" -o /app/output/article.txt
```

**Docker Compose:**
```bash
# Start all services
docker-compose up

# Run specific service
docker-compose up wiki-web

# Run in background
docker-compose up -d

# View logs
docker-compose logs -f

# Stop all
docker-compose down
```

## Advanced Features

### Custom Models

Use different OpenAI models:

```bash
# GPT-4 (default, best quality)
python -m src.cli article "Event" --model gpt-4

# GPT-4 Turbo (faster)
python -m src.cli article "Event" --model gpt-4-turbo

# GPT-3.5 Turbo (economical)
python -m src.cli article "Event" --model gpt-3.5-turbo
```

### Writing Styles

Choose appropriate style:

- **formal** - Encyclopedia style, professional
- **casual** - Conversational, accessible
- **detailed** - Comprehensive, in-depth

```bash
python -m src.cli article "Muscat Festival" --style detailed
```

### Context Enhancement

Provide additional context for better results:

```bash
python -m src.cli article "Muscat Festival" \
  --context "Held annually in January-February, features cultural performances, shopping, and international visitors"
```

## Performance Tips

1. **Use appropriate models** - gpt-3.5-turbo for speed, gpt-4 for quality
2. **Batch processing** - Generate multiple articles efficiently
3. **Cache results** - Store frequently generated content
4. **Docker caching** - Leverage Docker layer caching
5. **Async operations** - Use web API for concurrent requests

## Troubleshooting

### Common Issues

**Import Errors:**
```bash
pip install -r requirements.txt
```

**API Key Errors:**
```bash
# Check .env file
cat .env

# Verify environment variable
echo $OPENAI_API_KEY
```

**Docker Issues:**
```bash
# Rebuild without cache
docker build --no-cache -t oman-wiki-generator .

# Check logs
docker logs <container-id>
```

**Web Server Won't Start:**
```bash
# Check port availability
lsof -i :8000  # Unix
netstat -ano | findstr :8000  # Windows

# Use different port
uvicorn src.web:app --port 8080
```

## Future Enhancements

Planned features:

- Multimedia integration (audio, video)
- Interactive maps
- Timeline generation
- Fact-checking integration
- Collaborative editing
- Version history
- API rate limiting
- Caching layer
- Database integration
- User authentication
- Analytics dashboard

## Support

For feature requests or issues:
- Open GitHub issue
- Check documentation
- Review examples
- Test locally first
- Provide detailed error messages
