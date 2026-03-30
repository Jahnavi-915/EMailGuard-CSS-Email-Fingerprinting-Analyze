# 📧 EMailGuard – CSS Email Fingerprinting Analyzer

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

**EMailGuard** is a static analysis tool designed to detect **CSS-based fingerprinting techniques** in HTML email (`.eml`) files. Inspired by the NDSS 2025 research *Cascading Spy Sheets*, it identifies hidden tracking behaviors, correlates multi-stage attacks, and generates a **risk-scored security report with mitigation guidance**.

---

## Table of Contents

- [📧 EMailGuard – CSS Email Fingerprinting Analyzer](#-emailguard--css-email-fingerprinting-analyzer)
  - [Table of Contents](#table-of-contents)
  - [Project Overview](#project-overview)
    - [Key Capabilities](#key-capabilities)
  - [Features](#features)
    - [Detection Engine](#detection-engine)
    - [Intelligence Layer](#intelligence-layer)
    - [Interfaces](#interfaces)
    - [Security Design](#security-design)
  - [How It Works](#how-it-works)
    - [Pipeline Breakdown](#pipeline-breakdown)
  - [System Architecture](#system-architecture)
  - [Research Foundation](#research-foundation)
  - [Installation](#installation)
    - [Dependencies](#dependencies)
  - [Usage](#usage)
    - [Command Line](#command-line)
    - [Web Interface](#web-interface)
  - [Testing](#testing)
  - [Deployment](#deployment)
  - [Team \& Responsibilities](#team--responsibilities)
    - [Member A — Core Pipeline](#member-a--core-pipeline)
    - [Member B — Detection \& Output](#member-b--detection--output)
    - [Shared](#shared)
  - [Future Improvements](#future-improvements)
  - [Acknowledgments](#acknowledgments)
  - [License](#license)

---

## Project Overview

Modern HTML emails can exploit advanced CSS features to **fingerprint users without JavaScript**. EMailGuard analyzes emails **offline and safely**, detecting these techniques and surfacing privacy risks before they reach end users.

### Key Capabilities

- Detects **6 CSS fingerprinting techniques**
- Identifies **multi-stage tracking patterns**
- Assigns a **risk score (0–100)**
- Generates **detailed HTML reports**
- Provides both a **CLI and Web Interface**

---

## Features

### Detection Engine

| Technique | What It Detects |
|-----------|----------------|
| `@import` | External tracking chains |
| `@media` | Conditional resource loading |
| `@container` | Font & environment detection |
| `calc()` | Data encoding via math functions |
| `@font-face` | Remote font tracking |
| `@supports` | Browser capability probing |

### Intelligence Layer

- **Correlation Engine** — Detects combined, multi-vector attacks
- **Risk Scoring System** — Weighted and boosted scoring model
- **Attack Classification** — Safe / Moderate / High / Critical

### Interfaces

- **Command-Line Tool** — Fast, scriptable analysis
- **Flask Web App** — Interactive report UI with file upload

### Security Design

- Fully **offline** — no external requests made during analysis
- No JavaScript execution
- Safe to run on untrusted email files

---

## How It Works

```
.eml file
    ↓
Email Parser (extract HTML)
    ↓
CSS Extractor (inline, <style>, imports, links)
    ↓
Detection Engine (6 modules)
    ↓
Correlation Engine
    ↓
Risk Scorer
    ↓
Report (CLI / HTML / Web UI)
```

### Pipeline Breakdown

1. **Parse Email** — Extract HTML body from `.eml`
2. **Extract CSS** — Collect inline styles, `<style>` blocks, `@import` chains, and linked sheets
3. **Run Detectors** — Apply all 6 fingerprinting detection modules
4. **Correlate Findings** — Identify advanced multi-technique attack patterns
5. **Score Risk** — Produce a numeric score (0–100) with a severity label
6. **Generate Report** — Output human-readable results via CLI or HTML

---

## System Architecture

```
┌─────────────┐
│  .eml file  │
└──────┬──────┘
       ↓
┌─────────────────┐
│  Email Parser   │
└──────┬──────────┘
       ↓
┌─────────────────┐
│  CSS Extractor  │
└──────┬──────────┘
       ↓
┌──────────────────────────┐
│  Detection Modules (×6)  │
└──────┬───────────────────┘
       ↓
┌──────────────────┐
│  Correlation     │
└──────┬───────────┘
       ↓
┌──────────────────┐
│  Risk Scorer     │
└──────┬───────────┘
       ↓
┌──────────────────────────┐
│  Output (CLI / HTML / UI)│
└──────────────────────────┘
```

---

## Research Foundation

This project implements concepts from:

> *Cascading Spy Sheets: Exploiting the Complexity of Modern CSS for Email and Browser Fingerprinting*
> NDSS 2025

| Technique | Paper Reference |
|-----------|----------------|
| `@import` | §IV-B, §VIII-C2 |
| `@media` | §III-B, §IV-A3 |
| `@container` | §IV-A |
| `calc()` | §V-A |
| `@font-face` | §IV-C1 |
| `@supports` | §IV-B |
| Correlation Engine | Custom extension |

---

## Installation

```bash
git clone https://github.com/yourusername/emailguard.git
cd emailguard

python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

pip install -r requirements.txt
```

### Dependencies

```
beautifulsoup4
lxml
jinja2
flask
pytest
tinycss2
```

---

## Usage

### Command Line

```bash
python main.py --input sample.eml --output report.html
```

**Options:**

| Flag | Description |
|------|-------------|
| `--verbose` | Detailed console output |
| `--summary` | Show risk score only |

### Web Interface

```bash
python app.py
```

Open `http://127.0.0.1:5000`, upload an `.eml` file, and view the report instantly.

---

## Testing

```bash
pytest tests/
```

**Coverage includes:**

- Detector unit tests
- Full end-to-end pipeline tests
- Edge cases (empty and malformed emails)
- False-positive validation

---

## Deployment

Deploy on **Render** in four steps:

1. Push the repository to GitHub
2. Create a new Web Service on [Render](https://render.com)
3. Set the start command:
   ```bash
   gunicorn app:app
   ```
4. Access the live app at `https://your-app.onrender.com`

---

## Team & Responsibilities

### Member A — Core Pipeline
- Email parser & CSS extraction
- Detectors: `@import`, `@media`, `@container`
- Correlation engine
- CLI interface & integration

### Member B — Detection & Output
- Detectors: `calc()`, `@font-face`, `@supports`
- Risk scoring system
- Flask backend & HTML report generation

### Shared
- Testing, debugging, and documentation
- Final integration and presentation

---

## Future Improvements

- 📊 Visualization dashboards for scan history
- 🧾 Plain-English explanations for each finding
- 🛡 Email client filter plugin integration
- 🌐 Browser extension for real-time scanning

---

## Acknowledgments

- NDSS 2025 researchers for the foundational *Cascading Spy Sheets* work
- Course instructors for project guidance

---

## License

MIT License — see the [LICENSE](LICENSE) file for details.

---

*Built for the Computer & Network Security course project.*