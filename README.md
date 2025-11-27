# Python Project with CI/CD Pipeline

This repository contains Python projects with automated CI/CD pipeline including linting, testing, and coverage reporting.

## Projects

### 1. Calculator Module
A simple calculator module with basic arithmetic operations.

### 2. Oman Events Wikipedia Generator
A CLI tool that generates Wikipedia-style articles about Oman events using OpenAI's GPT models.

**Quick Start:**
```bash
# Install dependencies
pip install -r requirements.txt

# Set up API key
cp .env.example .env
# Edit .env and add your OpenAI API key

# Generate an article
python -m src.cli article "Muscat Festival"

# Generate a complete package
python -m src.cli full "National Day of Oman" -o national_day.txt
```

**Features:**
- Full Wikipedia-style article generation
- Event summaries
- Infobox creation
- Multiple output formats
- Customizable writing styles

📖 **Full Documentation:** See [OMAN_WIKI_GENERATOR.md](OMAN_WIKI_GENERATOR.md) for detailed usage instructions.

## Installation

1. Clone the repository:
```bash
git clone https://github.com/moodi112/https-github.com-moodi112-moodi112.git
cd https-github.com-moodi112-moodi112
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. (Optional) For Oman Wiki Generator, set up your OpenAI API key:
```bash
cp .env.example .env
# Edit .env and add: OPENAI_API_KEY=your_key_here
```

## Usage Examples

### Calculator
```python
from src.calculator import Calculator

calc = Calculator()
result = calc.add(5, 3)  # Returns 8
```

### Oman Wiki Generator
```bash
# Generate article
python -m src.cli article "Muscat Festival" --style formal

# Generate summary
python -m src.cli summary "National Day of Oman" --max-length 150

# Generate infobox
python -m src.cli infobox "Salalah Tourism Festival"

# Generate complete package
python -m src.cli full "Oman Rally" --output oman_rally.txt
```

## Development

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

3. **Coverage** 📊
   - Runs tests with coverage
   - Uploads to Codecov
   - Final notifications

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

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Code Style

- Follow PEP 8 guidelines
- Use Black for formatting
- Write docstrings for all functions and classes
- Add tests for new features

## CI Badge

![Matrix Python CI](https://github.com/moodi112/https-github.com-moodi112-moodi112/workflows/Matrix%20Python%20CI/badge.svg)

## License

See [LICENSE](LICENSE) file for details.

## Support

For issues or questions:
- Open a GitHub issue
- Check the documentation files
- Review the troubleshooting sections

## Acknowledgments

- OpenAI for GPT models
- GitHub Actions for CI/CD
- All contributors to this project
