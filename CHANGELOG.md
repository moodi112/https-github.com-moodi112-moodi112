# Changelog

All notable changes to the Oman Wikipedia Generator project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Full automated publishing pipeline
- GitHub Pages documentation deployment
- Automatic Docker image builds
- PyPI package publishing on tags
- Automated version bumping based on commit messages
- Auto-generated release notes

## [0.1.0] - 2025-11-29

### Added
- Initial release of Oman Wikipedia Generator
- AI-powered Wikipedia article generation using OpenAI GPT models
- Command-line interface (CLI) with multiple commands
- REST API with FastAPI
- Multi-language support (English and Arabic)
- Multiple export formats (Markdown, HTML, PDF)
- Batch processing capabilities
- Docker support with docker-compose
- Comprehensive test suite with pytest
- CI/CD pipeline with GitHub Actions
- Security scanning with Bandit
- Code quality tools (Black, Flake8)
- Documentation and deployment guides
- OpenAI connection test utility

### Features
- Generate full Wikipedia-style articles
- Generate concise summaries
- Generate structured infoboxes
- Batch generation from file or command line
- Image prompt generation for DALL-E
- Three HTML export themes
- PDF export with WeasyPrint
- Interactive API documentation (Swagger UI)

### Infrastructure
- Multi-stage Docker builds
- GitHub Actions CI/CD
- Matrix testing (Ubuntu, macOS, Windows)
- Python 3.9, 3.10, 3.11 support
- Codecov integration
- Slack and Teams notifications

## How Versions Work

This project uses semantic versioning (MAJOR.MINOR.PATCH):

- **MAJOR** version: Breaking changes (incompatible API changes)
  - Commit message: `BREAKING CHANGE:` or `feat!:`
- **MINOR** version: New features (backwards compatible)
  - Commit message: `feat:` or `feature:`
- **PATCH** version: Bug fixes and minor changes
  - Commit message: `fix:`, `docs:`, `chore:`, etc.

### Automatic Version Bumping

Versions are automatically bumped based on your commit messages:

```bash
# Patch bump (0.1.0 → 0.1.1)
git commit -m "fix: resolve API connection issue"
git commit -m "docs: update README"

# Minor bump (0.1.0 → 0.2.0)
git commit -m "feat: add new export format"

# Major bump (0.1.0 → 1.0.0)
git commit -m "feat!: redesign CLI interface"
git commit -m "BREAKING CHANGE: remove deprecated endpoints"
```

### Release Process

1. Push commits to main branch
2. Version automatically bumps based on commit type
3. Tag is created (e.g., v0.2.0)
4. GitHub Release is created with changelog
5. Documentation is deployed to GitHub Pages
6. Docker image is built and pushed
7. Package is published to PyPI (if token configured)

[Unreleased]: https://github.com/moodi112/https-github.com-moodi112-moodi112/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/moodi112/https-github.com-moodi112-moodi112/releases/tag/v0.1.0
