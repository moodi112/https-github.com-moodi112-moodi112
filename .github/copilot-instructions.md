# GitHub Copilot Instructions

## Project Overview
This repository documents a GitHub Actions CI/CD pipeline configuration for Python projects. The README contains a complete workflow template for matrix-based testing with notifications.

## CI/CD Pipeline Architecture

### Workflow Jobs Structure
The pipeline follows a three-stage approach documented in `README.md`:

1. **Lint Job** - Code quality checks using Black and Flake8
2. **Test Job** - Matrix testing across multiple OS and Python versions
3. **Coverage Job** - Depends on test completion, uploads to Codecov

### Matrix Testing Strategy
Tests run across:
- **OS**: Ubuntu, macOS, Windows (with exclusions for Windows + Python 3.9)
- **Python versions**: 3.9, 3.10, 3.11
- Uses `fail-fast: true` to stop immediately on first failure

### Key Workflow Patterns

**Caching Strategy:**
```yaml
path: ~/.cache/pip
key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}
```

**Test Execution:**
```bash
pytest --maxfail=1 --disable-warnings --junitxml=results/junit-${{ matrix.os }}-${{ matrix.python-version }}.xml
```

**Coverage Generation:**
```bash
pytest --cov=./ --cov-report=xml
```

## Notifications
Every job includes dual notification system:
- **Slack**: Using `8398a7/action-slack@v3`
- **Teams**: Using `Ilshidur/action-msteams@v2`

Both notifications trigger on `if: always()` to report success and failures.

## Required Secrets
Configure these in repository settings:
- `SLACK_WEBHOOK_URL` - Slack notifications
- `TEAMS_WEBHOOK_URL` - Microsoft Teams notifications
- `CODECOV_TOKEN` - Coverage reporting

## Dependencies Management
- Lint tools: `black`, `flake8`
- Testing: `pytest`, `pytest-cov`, `codecov`
- Project deps: `requirements.txt` (expected at repository root)

### Minimal requirements.txt Template
```
# Testing & Code Quality
pytest>=7.0.0
pytest-cov>=4.0.0
black>=23.0.0
flake8>=6.0.0
codecov>=2.1.0

# Your project dependencies below
# example:
# requests>=2.28.0
# numpy>=1.24.0
```

### Managing Dependencies
```bash
# Generate from current environment
pip freeze > requirements.txt

# Install from requirements.txt
pip install -r requirements.txt

# Update specific package
pip install --upgrade pytest
pip freeze | grep pytest >> requirements.txt

# Separate dev and prod dependencies (optional)
# requirements.txt - production only
# requirements-dev.txt - testing and linting
```

## Development Standards
- Code formatting enforced by Black (`black --check .`)
- Linting enforced by Flake8
- Standard Python version: 3.11 for non-matrix jobs
- Test artifacts uploaded as JUnit XML for each matrix combination

## Workflow File Location
The workflow configuration in `README.md` should be placed at:
```
.github/workflows/ci.yml
```

## Project Structure Expectations
```
project-root/
├── .github/
│   └── workflows/
│       └── ci.yml          # Place the workflow here
├── requirements.txt        # Required: Python dependencies
├── tests/                  # pytest will auto-discover test_*.py
├── src/ or lib/           # Your application code
└── README.md
```

## Testing Locally Before CI
Before pushing, verify the pipeline will pass:

```bash
# Install dev dependencies
pip install black flake8 pytest pytest-cov

# Run linting (matches CI lint job)
black --check .  # Exit code 0 = formatted, 1 = needs formatting
flake8 .         # Exit code 0 = no issues

# Run tests (matches CI test job)
pytest --maxfail=1 --disable-warnings
# --maxfail=1: Stop on first failure (fail-fast)
# --disable-warnings: Cleaner output

# Generate coverage report (matches CI coverage job)
pytest --cov=./ --cov-report=xml        # For Codecov upload
pytest --cov=./ --cov-report=html       # For local viewing
pytest --cov=./ --cov-report=term       # Terminal output
```

## Local Debugging Workflow
```bash
# Fix formatting issues found by Black
black .  # Auto-formats all files

# Run single test file
pytest tests/test_specific.py -v

# Run with full output (no capture)
pytest -s

# Run with detailed failure info
pytest -vv --tb=long

# Run only failed tests from last run
pytest --lf
```

## Artifact Outputs
- **JUnit XML**: `results/junit-{os}-{python-version}.xml` (per matrix combination)
- **Coverage XML**: `coverage.xml` (root level, uploaded to Codecov)
- **Artifacts stored**: 30 days retention (GitHub Actions default)

**Accessing Artifacts:**
1. Go to Actions tab → Select workflow run
2. Scroll to "Artifacts" section at bottom
3. Download zip files (e.g., `junit-ubuntu-latest-3.11.zip`)

**Analyzing JUnit XML locally:**
```bash
# Install JUnit viewer (optional)
pip install junit2html
junit2html results/junit-*.xml report.html
```

## Matrix Exclusions Pattern
When adding new OS/Python combinations:
```yaml
exclude:
  - os: windows-latest
    python-version: 3.9  # Example: Windows + Python 3.9 excluded
```

## Notification Customization
Both Slack and Teams notifications use:
- Job name (emoji prefix: 📝 Lint, 🧪 Test, 📊 Coverage)
- Job status (`${{ job.status }}` - success/failure/cancelled)
- Repository context (`${{ github.repository }}`)
- Matrix dimensions for test jobs

## Adding New Jobs
New jobs should follow the pattern:
1. Descriptive name with emoji
2. Appropriate `runs-on` or `needs` dependencies
3. Both Slack and Teams notifications with `if: always()`
4. Consistent field reporting in notifications

## Common Workflow Modifications

**Add Python 3.12 to matrix:**
```yaml
python-version: [3.9, 3.10, 3.11, 3.12]
```

**Remove macOS to speed up pipeline:**
```yaml
os: [ubuntu-latest, windows-latest]
```

**Add environment variables:**
```yaml
- name: Run tests
  env:
    DATABASE_URL: sqlite:///test.db
    DEBUG: true
  run: pytest --maxfail=1
```

**Skip CI on specific commits:**
```bash
git commit -m "docs: update README [skip ci]"
```

**Run jobs only on main branch:**
```yaml
lint:
  if: github.ref == 'refs/heads/main'
  runs-on: ubuntu-latest
```

## Pipeline Execution Order
```
lint (standalone)
  ↓
test (matrix, independent from lint)
  ↓
coverage (depends on: test)
```
Note: `lint` and `test` jobs run in parallel by default (no dependency).

## Troubleshooting Common Issues

### Cache miss: `Cache not found for input keys`
- **Cause**: `requirements.txt` changed or first run
- **Solution**: Expected behavior, cache will rebuild

### Windows + Python 3.9 skipped
- **Cause**: Intentional exclusion in matrix
- **Solution**: Check `exclude:` section if you need this combination

### Coverage upload fails: `Error uploading to Codecov`
- **Cause**: Missing or invalid `CODECOV_TOKEN`
- **Solution**: Settings → Secrets → Add `CODECOV_TOKEN` from codecov.io

### Notification errors: `Error: Webhook returned 400`
- **Cause**: Expired or invalid webhook URL
- **Solution**: Regenerate webhooks in Slack/Teams, update secrets

### Test failures only in CI, not locally
- **Check timezone/locale**: CI runs in UTC
- **Check file paths**: Use `os.path.join()` or `pathlib.Path`
- **Check dependencies**: Ensure `requirements.txt` is complete

### `ModuleNotFoundError` in CI
- **Solution**: Add missing package to `requirements.txt`
- **Or**: Install in workflow: `pip install package-name`

### Black formatting errors
- **Local fix**: Run `black .` to auto-format
- **Check version**: Ensure same Black version locally and in CI

### Flake8 errors (E501, W503, etc.)
- **Configure**: Create `.flake8` file:
  ```ini
  [flake8]
  max-line-length = 88
  extend-ignore = E203, W503
  ```

### Matrix job stuck or slow
- **Windows jobs**: Often slower (2-3x) than Linux
- **Solution**: Use `timeout-minutes: 30` per job if needed

### Artifacts not uploading
- **Check path**: Ensure `results/` directory exists
- **Create in test**: Add `mkdir -p results` before pytest

### Codecov not commenting on PRs
- **Cause**: Missing GitHub App installation
- **Solution**: Install Codecov GitHub App from codecov.io

## Environment Variables & Secrets
**Required Repository Secrets** (Settings → Secrets and variables → Actions):
- `SLACK_WEBHOOK_URL` - Slack incoming webhook for notifications
- `TEAMS_WEBHOOK_URL` - Microsoft Teams webhook URL
- `CODECOV_TOKEN` - Codecov project upload token

**Available GitHub Context Variables:**
- `${{ github.repository }}` - Full repo name (owner/repo)
- `${{ github.ref }}` - Branch/tag reference
- `${{ runner.os }}` - OS of the runner (Linux, Windows, macOS)
- `${{ matrix.os }}` / `${{ matrix.python-version }}` - Current matrix values
- `${{ job.status }}` - Job result (success, failure, cancelled)

## Security Best Practices
- **Never hardcode tokens** - Always use GitHub Secrets
- **Webhook URLs are sensitive** - Don't expose in logs or error messages
- **Pin action versions** - Using `@v3` or `@v4` (as in workflow) is acceptable but consider SHA pinning for production
- **Review third-party actions** - Actions used: `actions/checkout`, `actions/setup-python`, `actions/cache`, `actions/upload-artifact`, `8398a7/action-slack`, `Ilshidur/action-msteams`, `codecov/codecov-action`
- **Secrets in notifications** - Notifications configured with `if: always()` ensure visibility but don't expose secret values

## Integration Guidelines

### Initial Setup Checklist
- [ ] Create `.github/workflows/` directory
- [ ] Copy workflow from `README.md` to `.github/workflows/ci.yml`
- [ ] Create `requirements.txt` with all dependencies (including test tools)
- [ ] Add secrets to repository: `SLACK_WEBHOOK_URL`, `TEAMS_WEBHOOK_URL`, `CODECOV_TOKEN`
- [ ] Verify tests run locally: `pytest --maxfail=1 --disable-warnings`
- [ ] Verify linting passes: `black --check . && flake8 .`
- [ ] Create `results/` directory or let pytest create it
- [ ] Push to branch and verify workflow triggers
- [ ] Check Actions tab for first run results

### Adding to Existing Python Projects
1. Copy workflow from `README.md` to `.github/workflows/ci.yml`
2. Create `requirements.txt` in project root with dependencies
3. Configure the three required secrets in repository settings
4. Ensure tests are pytest-compatible
5. Push to trigger first pipeline run

### Verification Steps After Setup
```bash
# 1. Verify workflow file syntax (optional: install act locally)
cat .github/workflows/ci.yml

# 2. Test all commands locally
black --check .
flake8 .
pytest --maxfail=1 --disable-warnings
pytest --cov=./ --cov-report=xml

# 3. Push and monitor
git add .github/workflows/ci.yml requirements.txt
git commit -m "ci: add GitHub Actions pipeline"
git push

# 4. Check Actions tab in GitHub
# Watch for: lint (green), test matrix (green), coverage (green)
```

### Adapting for Different Project Structures
**Monorepo/subdirectory projects:**
```yaml
- name: Install dependencies
  run: |
    cd path/to/python/project
    pip install -r requirements.txt
```

**Multiple test directories:**
```bash
pytest tests/ integration/ --maxfail=1 --disable-warnings
```

**Custom coverage paths:**
```bash
pytest --cov=src/ --cov=lib/ --cov-report=xml
```

### Extending the Pipeline
**Add deployment job:**
```yaml
deploy:
  name: 🚀 Deploy
  needs: coverage
  runs-on: ubuntu-latest
  if: github.ref == 'refs/heads/main'
  steps:
    # Deployment steps
```

**Add security scanning:**
```yaml
security:
  name: 🔒 Security Scan
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v3
    - name: Run Bandit
      run: |
        pip install bandit
        bandit -r . -f json -o bandit-report.json
```

## Quick Reference Commands

**Setup new environment:**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1  # Windows PowerShell
pip install -r requirements.txt
```

**Pre-commit validation:**
```bash
black --check . && flake8 . && pytest --maxfail=1
```

**View coverage locally:**
```bash
pytest --cov=./ --cov-report=html
# Open htmlcov/index.html in browser
```

**Test specific matrix combination locally:**
```bash
# Simulate Ubuntu + Python 3.11
pytest --maxfail=1 --disable-warnings --junitxml=results/junit-ubuntu-latest-3.11.xml
```

## Badge Integration
Add to your actual project README (not this template repo):
```markdown
![CI Pipeline](https://github.com/moodi112/<repo-name>/workflows/CI%20Pipeline/badge.svg)
[![codecov](https://codecov.io/gh/moodi112/<repo-name>/branch/main/graph/badge.svg)](https://codecov.io/gh/moodi112/<repo-name>)
```

## Performance Optimization
- **Pip caching** saves ~30-60s per matrix job
- **fail-fast: true** stops other matrix jobs on first failure (faster feedback)
- **Parallel jobs** - lint and test jobs run simultaneously
- **Artifact retention** - Default 30 days; adjust with `retention-days` if needed

### Expected Timing (approximate)
- **Lint job**: 1-2 minutes
- **Test job (per matrix)**: 2-5 minutes
- **Coverage job**: 2-3 minutes
- **Total pipeline**: 5-10 minutes (with caching)

### Optimization Strategies
```yaml
# 1. Reduce matrix size for faster feedback
matrix:
  os: [ubuntu-latest]  # Only Linux for speed
  python-version: [3.11]  # Only latest version

# 2. Add timeouts to prevent hung jobs
jobs:
  test:
    timeout-minutes: 15

# 3. Use conda for faster dependency resolution (alternative)
- name: Setup Python with Miniconda
  uses: conda-incubator/setup-miniconda@v2
  with:
    python-version: ${{ matrix.python-version }}
    mamba-version: "*"

# 4. Cache more aggressively
- uses: actions/cache@v3
  with:
    path: |
      ~/.cache/pip
      ~/.cache/pytest
      .pytest_cache
    key: ${{ runner.os }}-python-${{ matrix.python-version }}-${{ hashFiles('**/requirements.txt') }}
```

## CI/CD Workflow Triggers
Current configuration triggers on:
- **Push** to any branch
- **Pull request** to any branch

To limit triggers:
```yaml
on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]
```
