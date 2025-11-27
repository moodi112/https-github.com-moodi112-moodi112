# 🇴🇲 Oman Wikipedia Generator

![CI Pipeline](https://github.com/moodi112/https-github.com-moodi112-moodi112/workflows/CI%20Pipeline/badge.svg)
[![codecov](https://codecov.io/gh/moodi112/https-github.com-moodi112-moodi112/branch/main/graph/badge.svg)](https://codecov.io/gh/moodi112/https-github.com-moodi112-moodi112)
![Python](https://img.shields.io/badge/python-3.9%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Docker](https://img.shields.io/badge/docker-ready-blue)
![Languages](https://img.shields.io/badge/languages-en%20%7C%20ar-orange)

> **Document Oman. One API call at a time.**

Oman has stories worth archiving — festivals that shaped a decade, venues that defined a generation, and creators who carried the culture. This engine captures all of it.

**Meet the AI-powered Wikipedia generator built for Oman's events, history, and cultural ecosystem.** Fast. Neutral. Ministry-friendly. Encyclopedia-clean.

---

## Why This Exists

Oman's cultural landscape is evolving faster than documentation can keep up. From **Muscat Festival** to **Renaissance Day**, from **Khareef Season** to emerging tech conferences — these moments deserve encyclopedia-quality coverage.

This tool generates:
- ✅ **Neutral, fact-based articles** following Wikipedia standards
- ✅ **Bilingual content** (English & Arabic) for local and international audiences  
- ✅ **Structured data** with infoboxes, summaries, and references
- ✅ **Export-ready formats** (Markdown, HTML, PDF) for publishing anywhere

Built for researchers, archivists, media professionals, and anyone documenting Oman's story.

---

## Oman Events Wikipedia Generator

The flagship project: An AI-powered CLI and web API for generating Wikipedia-style articles about Oman events using OpenAI's GPT models.

### 🚀 Quick Start

Generate your first article in 60 seconds:

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set up API key
cp .env.example .env
# Edit .env and add: OPENAI_API_KEY=your_key_here

# 3. Generate an article
python -m src.cli article "Muscat Festival"

# 4. Generate in Arabic
python -m src.cli article "مهرجان مسقط" --language ar

# 5. Export as PDF
python -m src.cli full "National Day of Oman" --format pdf -o national_day.pdf
```

### ✨ Core Capabilities

| Feature | Description | Command Example |
|---------|-------------|-----------------|
| **Full Articles** | Complete Wikipedia-style articles with sections | `article "Muscat Festival"` |
| **Summaries** | Concise overviews (50-200 words) | `summary "National Day" --max-length 150` |
| **Infoboxes** | Structured quick-facts boxes | `infobox "Salalah Tourism Festival"` |
| **Batch Processing** | Generate 10+ articles at once | `batch --file events.txt` |
| **Multi-Language** | English & Arabic support | `--language ar` |
| **Export Formats** | Markdown, HTML, PDF | `--format pdf` |
| **Web API** | REST API with interactive docs | `docker-compose up wiki-web` |

### 🎯 Example Use Cases

**Research & Academia:**
```bash
# Generate comprehensive research material
python -m src.cli full "Oman Desert Marathon" \
  --context "Annual 165km ultramarathon in Omani desert" \
  --format pdf -o research/marathon_2024.pdf
```

**Media & Publishing:**
```bash
# Batch process events for publication
python -m src.cli batch \
  --file upcoming_events.txt \
  --export-format html \
  --output-dir website/events/
```

**Government Documentation:**
```bash
# Bilingual official documentation
python -m src.cli full "Renaissance Day" \
  --language ar \
  --format pdf -o official/renaissance_ar.pdf
```

---

## Features Deep Dive

### 🌐 Multi-Language Support

Generate content in **English** and **Arabic** with culturally appropriate phrasing:

- Native Arabic prompts for authentic tone
- Proper right-to-left formatting
- Cultural context awareness
- Ministry-appropriate language

### 📦 Batch Processing

Process dozens of events efficiently:

```bash
# From file (one event per line)
python -m src.cli batch --file events.txt --output-dir ./articles

# From command line
python -m src.cli batch \
  -e "Muscat Festival" \
  -e "National Day" \
  -e "Khareef Season" \
  --type article \
  --export-format html \
  -o ./batch_output
```

### 📄 Export Formats

**Markdown** - Version control friendly
```bash
python -m src.cli article "Event" --format markdown -o event.md
```

**HTML** - Three beautiful themes
```bash
# Wikipedia style (classic)
# Modern style (gradient design)
# Minimal style (clean reading)
python -m src.cli full "Event" --format html -o event.html
```

**PDF** - Print-ready documents
```bash
python -m src.cli full "Event" --format pdf -o event.pdf
```

### 🌐 Web API

Start the FastAPI server:

```bash
# Local development
uvicorn src.web:app --reload

# Docker
docker-compose up wiki-web

# Visit http://localhost:8000 for interactive UI
# API docs at http://localhost:8000/docs
```

**API Endpoints:**
- `POST /generate/article` - Full article generation
- `POST /generate/summary` - Quick summaries
- `POST /generate/infobox` - Structured data
- `POST /batch/generate` - Bulk processing
- `POST /export` - Format conversion

### 🎨 Image Prompts

Generate DALL-E compatible image descriptions:

```bash
python -m src.cli image-prompt "Muscat Festival" \
  --context "Colorful cultural celebration with traditional Omani dancers"
```

Output includes both article and ready-to-use DALL-E prompt for visual content.

---

## Installation

1. **Clone the repository:**
```bash
git clone https://github.com/moodi112/https-github.com-moodi112-moodi112.git
cd https-github.com-moodi112-moodi112
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Set up OpenAI API key:**
```bash
cp .env.example .env
# Edit .env and add: OPENAI_API_KEY=your_key_here
```

4. **Verify installation:**
```bash
python -m src.cli --help
```

---

## Usage Examples

### CLI Commands

**Generate Article:**
```bash
# English article
python -m src.cli article "Muscat Festival" \
  --style formal \
  --output muscat_festival.txt

# Arabic article with context
python -m src.cli article "اليوم الوطني" \
  --language ar \
  --context "احتفال سنوي في 18 نوفمبر" \
  --format html \
  -o national_day_ar.html
```

**Generate Summary:**
```bash
# Quick 150-word summary
python -m src.cli summary "Salalah Tourism Festival" --max-length 150

# Arabic summary
python -m src.cli summary "مهرجان صلالة" --language ar
```

**Generate Infobox:**
```bash
python -m src.cli infobox "Oman Rally" --language en
```

**Complete Package:**
```bash
# Generate article + summary + infobox
python -m src.cli full "Khareef Season" \
  --context "Annual monsoon festival in Dhofar region" \
  --format pdf \
  -o khareef_complete.pdf
```

**Batch Processing:**
```bash
# Process multiple events
python -m src.cli batch \
  -e "Muscat Festival" \
  -e "National Day" \
  -e "Renaissance Day" \
  -e "Oman Desert Marathon" \
  --type article \
  --language en \
  --export-format html \
  --output-dir ./oman_events
```

### Python API

```python
from src.wiki_generator import WikiGenerator

# Initialize
generator = WikiGenerator(model="gpt-4")

# Generate article
article = generator.generate_wiki_article(
    event_name="Muscat Festival",
    context="Annual cultural and shopping festival",
    style="formal",
    language="en"
)

# Generate in Arabic
article_ar = generator.generate_wiki_article(
    event_name="مهرجان مسقط",
    language="ar"
)

# Batch processing
events = [
    "Muscat Festival",
    "National Day of Oman", 
    "Salalah Tourism Festival"
]

results = generator.batch_generate(
    event_names=events,
    output_type="article",
    language="en"
)

for event, content in results.items():
    print(f"Generated: {event}")
```

### REST API

```bash
# Start server
docker-compose up wiki-web

# Generate article
curl -X POST "http://localhost:8000/generate/article" \
  -H "Content-Type: application/json" \
  -d '{
    "event_name": "Muscat Festival",
    "language": "en",
    "style": "formal"
  }'

# Batch generation
curl -X POST "http://localhost:8000/batch/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "event_names": ["Muscat Festival", "National Day"],
    "output_type": "article",
    "language": "en"
  }'
```

---

## Example Oman Events

Perfect candidates for documentation:

### National Events
- 🇴🇲 **National Day of Oman** - November 18th celebration
- 🎖️ **Renaissance Day** - July 23rd commemoration  
- 🏛️ **Flag Day** - National symbol celebration

### Festivals & Culture
- 🎭 **Muscat Festival** - Annual cultural and shopping extravaganza
- 🌴 **Salalah Tourism Festival** - Khareef season celebration
- 🎪 **Oman Traditional Crafts Festival** - Heritage showcase
- 📚 **Muscat International Book Fair** - Literary gathering

### Sports & Adventure
- 🏃 **Oman Desert Marathon** - 165km ultramarathon challenge
- ⛵ **Al Mouj Golf Tournament** - International championship
- 🚗 **Oman Rally** - Off-road motorsport event

### Seasonal Events
- 🌊 **Khareef Season** - Monsoon transformation in Dhofar
- 🏖️ **Muscat Marathon** - Coastal running event
- 🎣 **Fishing Festivals** - Coastal community celebrations

---


## Architecture & Technology

### Tech Stack

**Core:**
- 🐍 Python 3.9+ (Type hints, async support)
- 🤖 OpenAI GPT-4 (Article generation engine)
- 🎨 Click (CLI framework with autocomplete)

**Web Framework:**
- ⚡ FastAPI (High-performance async API)
- 📦 Pydantic (Data validation)
- 🔄 Uvicorn (ASGI server)

**Export & Formatting:**
- 📝 Markdown, Jinja2 (Template rendering)
- 🎨 WeasyPrint (PDF generation)
- 🌐 HTML with 3 custom themes

**DevOps:**
- 🐳 Docker & Docker Compose
- 🔄 GitHub Actions CI/CD
- 🔒 Bandit & Safety (Security scanning)
- ✅ pytest, Black, Flake8 (Quality tools)

### Project Structure

```
oman-wiki-generator/
├── src/
│   ├── wiki_generator.py    # Core AI generation engine
│   ├── cli.py                # Command-line interface  
│   ├── web.py                # FastAPI REST API
│   └── exporters.py          # Format converters (MD/HTML/PDF)
├── tests/
│   ├── test_wiki_generator.py
│   └── test_calculator.py
├── .github/workflows/
│   └── ci.yml                # Complete CI/CD pipeline
├── docs/
│   ├── FEATURES.md           # Feature documentation
│   ├── DEPLOYMENT.md         # Deployment guides
│   └── UPDATE_SUMMARY.md     # Version history
├── Dockerfile                # Multi-stage container
├── docker-compose.yml        # Service orchestration
├── requirements.txt          # Python dependencies
└── README.md                 # You are here
```

---

### Running Tests
```bash
pytest
```

### Running Tests with Coverage
```bash
pytest --cov=./
```

### Code Formatting
```bash
black .
```

### Linting
```bash
flake8 .
```

### Security Scanning
```bash
# Run Bandit
bandit -r src/

# Check dependencies
safety check
```

### Docker

Build and run with Docker:
```bash
# Build image
docker build -t oman-wiki-generator .

# Run CLI command
docker run --rm -v $(pwd)/output:/app/output oman-wiki-generator \
  python -m src.cli article "Muscat Festival"

# Run tests in container
docker-compose run test

# Start web interface
docker-compose up wiki-web
```

## CI/CD Pipeline

This project uses GitHub Actions for continuous integration:

### Pipeline Jobs

1. **Lint** 📝
   - Runs Black formatter check
   - Runs Flake8 linter
   - Notifies Slack and Teams

2. **Test** 🧪
   - Matrix testing across multiple OS and Python versions
   - OS: Ubuntu, macOS, Windows
   - Python: 3.9, 3.10, 3.11
   - Generates JUnit XML reports
   - Caches pip dependencies

3. **Security** 🔒
   - Runs Bandit security scanner
   - Checks dependencies with Safety
   - Generates security reports

4. **Coverage** 📊
   - Runs tests with coverage
   - Uploads to Codecov
   - Final notifications

5. **Docker** 🐳
   - Builds Docker images
   - Runs tests in containers
   - Validates containerization

### Notifications

The pipeline sends notifications to:
- Slack (via webhook)
- Microsoft Teams (via webhook)

Set up webhooks in repository secrets:
- `SLACK_WEBHOOK_URL`
- `TEAMS_WEBHOOK_URL`
- `CODECOV_TOKEN`

See [WEBHOOK_SETUP.md](WEBHOOK_SETUP.md) for webhook configuration details.

## Project Structure

```
.
├── src/
│   ├── __init__.py
│   ├── calculator.py          # Calculator module
│   ├── wiki_generator.py      # Wikipedia generator core
│   ├── cli.py                 # CLI interface
│   └── __main__.py            # Module entry point
├── tests/
│   ├── __init__.py
│   └── test_calculator.py     # Calculator tests
├── .github/
│   └── workflows/
│       └── ci.yml             # CI/CD pipeline
├── .env.example               # Environment variables template
├── .gitignore
├── .flake8                    # Flake8 configuration
├── requirements.txt           # Python dependencies
├── README.md                  # This file
├── OMAN_WIKI_GENERATOR.md     # Wiki generator documentation
├── WEBHOOK_SETUP.md           # Webhook setup guide
└── LICENSE
```

## Requirements

### Core Dependencies
- Python 3.9+

### Testing & Code Quality
- pytest>=7.4.0
- pytest-cov>=4.1.0
- black>=23.0.0
- flake8>=6.0.0
- codecov>=2.1.13

### Oman Wiki Generator
- openai>=1.0.0
- python-dotenv>=1.0.0
- click>=8.1.0
- requests>=2.31.0

## Contributing

We welcome contributions that improve Oman's digital documentation ecosystem!

### How to Contribute

1. **Fork** the repository
2. **Create** a feature branch
   ```bash
   git checkout -b feature/add-new-event-type
   ```
3. **Commit** your changes  
   ```bash
   git commit -m 'feat: add support for heritage site documentation'
   ```
4. **Push** to your branch
   ```bash
   git push origin feature/add-new-event-type
   ```
5. **Open** a Pull Request with clear description

### Contribution Ideas

- 🌍 Add new language support (French, Hindi, Urdu)
- 📊 Improve citation validation algorithms
- 🎨 Create new HTML export themes
- 📝 Expand event type templates
- 🧪 Add more test coverage
- 📚 Translate documentation to Arabic
- 🔌 Build integrations (WordPress, Ghost CMS, etc.)

### Code Standards

- ✅ Follow PEP 8 guidelines
- ✅ Use Black for formatting (`black .`)
- ✅ Pass all tests (`pytest`)
- ✅ Pass security scans (`bandit -r src/`)
- ✅ Write docstrings for public functions
- ✅ Add tests for new features
- ✅ Update documentation

### Pre-commit Hooks

We use pre-commit hooks to maintain code quality:

```bash
pip install pre-commit
pre-commit install
pre-commit run --all-files  # Test before committing
```

---

## Documentation

📖 **Comprehensive Guides:**
- **[FEATURES.md](FEATURES.md)** - Complete feature documentation with examples
- **[DEPLOYMENT.md](DEPLOYMENT.md)** - Platform-specific deployment guides  
- **[OMAN_WIKI_GENERATOR.md](OMAN_WIKI_GENERATOR.md)** - Original tool documentation
- **[WEBHOOK_SETUP.md](WEBHOOK_SETUP.md)** - CI/CD notification setup
- **[UPDATE_SUMMARY.md](UPDATE_SUMMARY.md)** - Version history and changelog

📱 **API Documentation:**
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

---

## License

MIT License - See [LICENSE](LICENSE) file for details.

Free for commercial and non-commercial use. Attribution appreciated but not required.

---

## Support & Community

### Get Help

- 📖 **Documentation**: Check the guides above
- 🐛 **Bug Reports**: [Open an issue](https://github.com/moodi112/https-github.com-moodi112-moodi112/issues)
- 💡 **Feature Requests**: [Start a discussion](https://github.com/moodi112/https-github.com-moodi112-moodi112/discussions)
- 🔒 **Security Issues**: Email maintainer directly

### Roadmap

Upcoming features in consideration:
- 🎥 Video content integration
- 🗺️ Interactive map generation for events
- 📊 Analytics dashboard for generated content
- 🔄 WordPress/CMS plugins
- 🌐 Public API with rate limiting
- 👥 Multi-user collaboration features
- 📱 Mobile app for on-site event documentation

---

## Acknowledgments

Built with incredible open-source tools:

- 🤖 **[OpenAI](https://openai.com)** - GPT-4 language models
- ⚡ **[FastAPI](https://fastapi.tiangulo.com)** - Modern Python web framework  
- 🐳 **[Docker](https://docker.com)** - Containerization platform
- 🔄 **[GitHub Actions](https://github.com/features/actions)** - CI/CD automation
- 🎨 **[WeasyPrint](https://weasyprint.org)** - HTML to PDF conversion
- 📝 **[Click](https://click.palletsprojects.com)** - CLI framework
- 🔒 **[Bandit](https://bandit.readthedocs.io)** - Security linting
- ✅ **[pytest](https://pytest.org)** - Testing framework

Special thanks to the Python and open-source communities.

---

## About

**Purpose**: Preserve and document Oman's cultural, historical, and contemporary events with encyclopedia-quality content.

**Vision**: Create the most comprehensive, accessible, and maintainable archive of Oman's evolving story.

**Mission**: Make professional documentation accessible to everyone — from government ministries to independent researchers.

**Built by**: Contributors passionate about Oman's heritage and digital transformation.

---

<div align="center">

**🇴🇲 Documenting Oman's Story — One Article at a Time**

Made with ❤️ for Oman

[⭐ Star this repo](https://github.com/moodi112/https-github.com-moodi112-moodi112) • [🍴 Fork](https://github.com/moodi112/https-github.com-moodi112-moodi112/fork) • [📖 Docs](FEATURES.md) • [🚀 Deploy](DEPLOYMENT.md)

</div>
