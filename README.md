# https-github.com-moodi112-moodi112
Ok # In your README.md, at the top:

name: CI Pipeline

on:
  push:
  pull_request:

jobs:

  lint:
    name: 📝 Lint
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install lint tools
        run: pip install black flake8

      - name: Run linters
        run: |
          black --check .
          flake8 .

      # Notifications
      - name: Notify Slack (lint)
        if: always()
        uses: 8398a7/action-slack@v3
        with:
          status: ${{ job.status }}
          fields: repo,commit,author,workflow,job
        env:
          SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK_URL }}

      - name: Notify Teams (lint)
        if: always()
        uses: Ilshidur/action-msteams@v2
        with:
          webhook-uri: ${{ secrets.TEAMS_WEBHOOK_URL }}
          title: "Lint • ${{ job.status }} • ${{ github.repository }}"
          summary: "Lint job ${{ job.status }}"

  test:
    name: 🧪 Test (matrix)
    runs-on: ${{ matrix.os }}
    strategy:
      fail-fast: true
      matrix:
        os: [ubuntu-latest, macos-latest, windows-latest]
        python-version: [3.9, 3.10, 3.11]
        exclude:
          - os: windows-latest
            python-version: 3.9

    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Cache pip
        uses: actions/cache@v3
        with:
          path: ~/.cache/pip
          key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}
          restore-keys: |
            ${{ runner.os }}-pip-

      - name: Setup Python ${{ matrix.python-version }} on ${{ matrix.os }}
        uses: actions/setup-python@v4
        with:
          python-version: ${{ matrix.python-version }}

      - name: Install dependencies
        run: |
          pip install --upgrade pip
          pip install -r requirements.txt

      - name: Run tests & generate JUnit XML
        run: pytest --maxfail=1 --disable-warnings --junitxml=results/junit-${{ matrix.os }}-${{ matrix.python-version }}.xml

      - name: Upload JUnit results
        uses: actions/upload-artifact@v3
        with:
          name: junit-${{ matrix.os }}-${{ matrix.python-version }}
          path: results/junit-${{ matrix.os }}-${{ matrix.python-version }}.xml

      # Notifications
      - name: Notify Slack (test)
        if: always()
        uses: 8398a7/action-slack@v3
        with:
          status: ${{ job.status }}
          fields: repo,commit,author,workflow,job,matrix
        env:
          SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK_URL }}

      - name: Notify Teams (test)
        if: always()
        uses: Ilshidur/action-msteams@v2
        with:
          webhook-uri: ${{ secrets.TEAMS_WEBHOOK_URL }}
          title: "Test • ${{ job.status }} • ${{ github.repository }}"
          summary: "OS: ${{ matrix.os }} | Python: ${{ matrix.python-version }}"

  coverage:
    name: 📊 Coverage & Report
    needs: test
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Setup Python 3.11
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install coverage tools
        run: pip install pytest-cov codecov

      - name: Run tests with coverage
        run: pytest --cov=./ --cov-report=xml

      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v3
        with:
          token: ${{ secrets.CODECOV_TOKEN }}
          files: coverage.xml

      # Final Notifications
      - name: Notify Slack (coverage)
        if: always()
        uses: 8398a7/action-slack@v3
        with:
          status: ${{ job.status }}
          fields: repo,commit,author,workflow,job
        env:
          SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK_URL }}

      - name: Notify Teams (coverage)
        if: always()
        uses: Ilshidur/action-msteams@v2
        with:
          webhook-uri: ${{ secrets.TEAMS_WEBHOOK_URL }}
          title: "Coverage • ${{ job.status }} • ${{ github.repository }}"
          summary: "Coverage job ${{ job.status }}"

![Matrix Python CI](https://github.com/<moodi112>/<.org>/workflows/Matrix%20Python%20CI/badge.svg)

