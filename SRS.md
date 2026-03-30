# Software Requirements Specification (SRS)

## CSS Email Fingerprinting Analyzer – EMailGuard

**Version:** 1.0  
**Team:** 2 Members  
**Date:** March 30, 2026  
**Based on:** *Cascading Spy Sheets: Exploiting the Complexity of Modern CSS for Email and Browser Fingerprinting* (NDSS 2025) by Trampert et al.

---

## Table of Contents

- [Software Requirements Specification (SRS)](#software-requirements-specification-srs)
  - [CSS Email Fingerprinting Analyzer – EMailGuard](#css-email-fingerprinting-analyzer--emailguard)
  - [Table of Contents](#table-of-contents)
  - [1. Introduction](#1-introduction)
    - [1.1 Purpose](#11-purpose)
    - [1.2 Document Conventions](#12-document-conventions)
    - [1.3 Intended Audience](#13-intended-audience)
    - [1.4 Product Scope](#14-product-scope)
    - [1.5 References](#15-references)
  - [2. Overall Description](#2-overall-description)
    - [2.1 Product Perspective](#21-product-perspective)
    - [2.2 User Classes and Characteristics](#22-user-classes-and-characteristics)
    - [2.3 Operating Environment](#23-operating-environment)
    - [2.4 Design and Implementation Constraints](#24-design-and-implementation-constraints)
    - [2.5 Assumptions and Dependencies](#25-assumptions-and-dependencies)
  - [3. System Features and Requirements](#3-system-features-and-requirements)
    - [3.1 Input Processing (Parser)](#31-input-processing-parser)
      - [3.1.1 .eml Parsing](#311-eml-parsing)
      - [3.1.2 HTML Extraction](#312-html-extraction)
      - [3.1.3 CSS Extraction](#313-css-extraction)
    - [3.2 Detectors](#32-detectors)
      - [3.2.1 Detector: @import Chain](#321-detector-import-chain)
      - [3.2.2 Detector: @media Conditional](#322-detector-media-conditional)
      - [3.2.3 Detector: @container Query](#323-detector-container-query)
      - [3.2.4 Detector: calc() Expression](#324-detector-calc-expression)
      - [3.2.5 Detector: @font-face Remote](#325-detector-font-face-remote)
      - [3.2.6 Detector: @supports Probe](#326-detector-supports-probe)
      - [3.2.7 Finding Object Structure](#327-finding-object-structure)
    - [3.3 Correlation Engine](#33-correlation-engine)
    - [3.4 Risk Scoring](#34-risk-scoring)
    - [3.5 Command‑Line Interface (CLI)](#35-commandline-interface-cli)
    - [3.6 Web Interface (Flask)](#36-web-interface-flask)
    - [3.7 Reporting](#37-reporting)
  - [4. External Interface Requirements](#4-external-interface-requirements)
    - [4.1 User Interfaces](#41-user-interfaces)
    - [4.2 Hardware Interfaces](#42-hardware-interfaces)
    - [4.3 Software Interfaces](#43-software-interfaces)
    - [4.4 Communications Interfaces](#44-communications-interfaces)
  - [5. Non‑Functional Requirements](#5-nonfunctional-requirements)
  - [6. Other Requirements](#6-other-requirements)
    - [6.1 Legal / Regulatory](#61-legal--regulatory)
    - [6.2 Testing Requirements](#62-testing-requirements)
    - [6.3 Documentation Requirements](#63-documentation-requirements)
    - [6.4 Project Deliverables](#64-project-deliverables)
  - [Appendix A: Traceability Matrix](#appendix-a-traceability-matrix)
  - [Appendix B: Glossary](#appendix-b-glossary)
  - [Appendix C: Team Role Distribution](#appendix-c-team-role-distribution)
  - [Appendix D: Implementation Timeline (4 Weeks)](#appendix-d-implementation-timeline-4-weeks)

---

## 1. Introduction

### 1.1 Purpose
The purpose of this Software Requirements Specification (SRS) is to provide a complete, detailed description of the **EMailGuard** system—a static analysis tool that detects CSS‑based fingerprinting techniques in HTML email files (`.eml`). The document defines the functional and non‑functional requirements, design constraints, and external interfaces. It serves as the primary reference for development, testing, and evaluation.

### 1.2 Document Conventions
- **RFC** – Request for Comments (Internet standards)
- **CSS** – Cascading Style Sheets
- **MIME** – Multipurpose Internet Mail Extensions
- **NDSS** – Network and Distributed System Security Symposium
- **CLI** – Command‑Line Interface
- **UI** – User Interface
- **REQ‑X** – Requirement identifier

### 1.3 Intended Audience
This SRS is intended for:
- **Development team** (2 members) – to guide implementation.
- **Project evaluators** – to understand the scope and rigor.
- **Security researchers** – to validate the tool’s alignment with academic work.

### 1.4 Product Scope
EMailGuard is a Python‑based tool that:
- Reads `.eml` files and extracts HTML and CSS content.
- Detects six distinct CSS fingerprinting techniques documented in the referenced paper.
- Correlates findings to identify multi‑stage fingerprinting attempts.
- Assigns a risk score (0–100) with a label: Safe, Moderate, High, or Critical.
- Produces a self‑contained HTML report with detailed findings, paper references, and mitigation suggestions.
- Offers two interfaces: a command‑line tool and a Flask web application for upload and report viewing.

The tool does **not** render or execute CSS or JavaScript; it performs only static pattern analysis.

### 1.5 References
- **Trampert et al., 2025** – *Cascading Spy Sheets: Exploiting the Complexity of Modern CSS for Email and Browser Fingerprinting*. In Proceedings of the Network and Distributed System Security Symposium (NDSS).  
  [Official repository: https://github.com/cispa/cascading-spy-sheets]

Specific sections cited throughout this SRS:
- **Section III‑B** – CSS At‑Rules (overview of at‑rules, including @media, @import, @font‑face, @supports)
- **Section III‑E** – Exfiltration Channels (use of url() to exfiltrate data)
- **Section IV‑A** – Container Queries (font detection via container queries, font‑relative units)
- **Section IV‑A1** – Font Detection (using ch, ex, ic, cap units)
- **Section IV‑B** – Other Rules (@import, @page, support queries)
- **Section V‑A** – CSS calc() Expressions (trigonometric functions, OS/architecture differences)
- **Section VIII‑C2** – Case Study: Email‑specific Threat Vectors (import bypass, CVE‑2024‑24510)
- **Section IX‑B** – Email Privacy Proxy (mitigations: style attribute conversion, inlining resources)

---

## 2. Overall Description

### 2.1 Product Perspective
EMailGuard is a new, self‑contained system. It does not replace any existing product but complements email security tools by providing specialized detection of CSS fingerprinting. It operates completely offline (no network requests) and does not execute any content.

### 2.2 User Classes and Characteristics
| User Class | Characteristics |
|------------|-----------------|
| **Security Researcher** | Comfortable with CLI; may analyze many emails in batch. Values detailed reports and traceability to academic research. |
| **Email Administrator** | May integrate tool into email filtering pipeline; needs simple output (risk score) and clear recommendations. |
| **Privacy‑conscious User** | Prefers web interface; wants an intuitive explanation of risks without technical details. |

### 2.3 Operating Environment
- **Operating Systems:** Windows 10/11, Ubuntu 22.04 LTS, macOS 12+.
- **Runtime:** Python 3.9 or higher.
- **Web Deployment:** Any platform supporting Python WSGI (Render, Railway, or local Flask server).

### 2.4 Design and Implementation Constraints
- **C1:** No network requests allowed during analysis (all static).
- **C2:** No JavaScript execution; the tool does not evaluate dynamic content.
- **C3:** Only pattern‑based detection; no CSS rendering engine.
- **C4:** Must handle standard MIME‑encoded `.eml` files.

### 2.5 Assumptions and Dependencies
- **A1:** Users have legal rights to analyze the provided emails.
- **A2:** Python environment with required libraries is installed.
- **A3:** Input `.eml` files conform to RFC 5322 and 2045–2049.
- **D1:** Relies on `beautifulsoup4` for HTML parsing.
- **D2:** Uses `jinja2` for HTML report templating.

---

## 3. System Features and Requirements

### 3.1 Input Processing (Parser)

#### 3.1.1 .eml Parsing
| ID | Requirement | Description | Paper Reference |
|----|-------------|-------------|-----------------|
| REQ‑1 | **File reading** | The system shall read a file provided via CLI or uploaded via web, validate it is a valid `.eml` file. | – |
| REQ‑2 | **MIME decoding** | It shall parse the MIME structure using Python’s `email` module, handling multipart and nested parts. | – |
| REQ‑3 | **Encoding support** | It shall decode `base64` and `quoted‑printable` content‑transfer‑encoding. | – |
| REQ‑4 | **Metadata extraction** | It shall extract `Subject`, `From`, `Date` headers for inclusion in reports. | – |

#### 3.1.2 HTML Extraction
| ID | Requirement | Description | Paper Reference |
|----|-------------|-------------|-----------------|
| REQ‑5 | **HTML body** | It shall locate the `text/html` MIME part and extract its content as a string. | – |

#### 3.1.3 CSS Extraction
| ID | Requirement | Description | Paper Reference |
|----|-------------|-------------|-----------------|
| REQ‑6 | `<style>` tags | It shall extract content from all `<style>` tags in the HTML. | – |
| REQ‑7 | **Inline styles** | It shall extract values of `style=""` attributes from any HTML element. | – |
| REQ‑8 | `<link>` detection | It shall detect `<link rel="stylesheet">` tags and record the `href` URL (without fetching). | – |
| REQ‑9 | `@import` detection | It shall scan all extracted CSS and HTML for `@import` statements and record the URL (external or data). | Section IV‑B, VIII‑C2 |

### 3.2 Detectors

Each detector implements a specific fingerprinting technique. Detectors are independent modules that take a list of CSS snippets and return a list of `Finding` objects (see 3.2.7).

#### 3.2.1 Detector: @import Chain
| ID | Requirement | Description | Paper Reference |
|----|-------------|-------------|-----------------|
| REQ‑10 | **Pattern** | Detects `@import` with a URL that is not a data: URL (i.e., external). | Section IV‑B, VIII‑C2 |
| REQ‑11 | **Risk** | Assigns **Critical** risk. | – |
| REQ‑12 | **Mitigation** | Suggests converting to inline styles or using a proxy that inlines resources. | Section IX‑B |

#### 3.2.2 Detector: @media Conditional
| ID | Requirement | Description | Paper Reference |
|----|-------------|-------------|-----------------|
| REQ‑13 | **Pattern** | Detects `@media` rules that query viewport dimensions (`width`, `height`, `resolution`, `device‑width`, `orientation`) **and** contain a `url()` inside the block. | Section III‑B, IV‑A3 |
| REQ‑14 | **Risk** | **Critical** if both conditions met; **Medium** if media query exists without `url()`. | – |
| REQ‑15 | **Mitigation** | Advises preloading all resources to eliminate conditional leakage. | Section IX‑B |

#### 3.2.3 Detector: @container Query
| ID | Requirement | Description | Paper Reference |
|----|-------------|-------------|-----------------|
| REQ‑16 | **Pattern** | Detects `@container` rules that contain **either** a `url()` (Critical) **or** font‑relative units (`ch`, `ex`, `ic`, `cap`) (High). | Section IV‑A, Listing 1 |
| REQ‑17 | **Risk** | Critical (if `url()` present); High (if font units present without `url()`). | – |
| REQ‑18 | **Mitigation** | Same as media queries: preload resources, or rewrite to inline styles. | Section IX‑B |

#### 3.2.4 Detector: calc() Expression
| ID | Requirement | Description | Paper Reference |
|----|-------------|-------------|-----------------|
| REQ‑19 | **Pattern** | Detects `calc()` expressions containing any of the following functions: `sin`, `cos`, `tan`, `asin`, `acos`, `atan`, `atan2`. | Section V‑A, Listing 3 |
| REQ‑20 | **Risk** | **High** (information leakage). | – |
| REQ‑21 | **Mitigation** | Suggest using a proxy that inlines resources or removing dynamic functions. | Section IX‑B |

#### 3.2.5 Detector: @font-face Remote
| ID | Requirement | Description | Paper Reference |
|----|-------------|-------------|-----------------|
| REQ‑22 | **Pattern** | Detects `@font-face` rules with `src: url(...)` where the URL is not a data: URL. | Section III‑B (Table I), IV‑C1 |
| REQ‑23 | **Risk** | **High** (remote font loading enables font fingerprinting). | – |
| REQ‑24 | **Mitigation** | Disable remote fonts or use a proxy that serves fonts locally. | Section IX‑B |

#### 3.2.6 Detector: @supports Probe
| ID | Requirement | Description | Paper Reference |
|----|-------------|-------------|-----------------|
| REQ‑25 | **Pattern** | Detects `@supports` blocks that contain a `url()` (exfiltration). | Section IV‑B, IV‑C2 |
| REQ‑26 | **Risk** | **High**. | – |
| REQ‑27 | **Mitigation** | Same as media queries: preload resources. | Section IX‑B |

#### 3.2.7 Finding Object Structure
Each detector shall produce objects of the following structure:

| Field | Type | Description |
|-------|------|-------------|
| `technique` | string | Human‑readable name (e.g., "Container Query Font Detection") |
| `snippet` | string | The exact CSS snippet that matched |
| `risk_level` | string | "Critical", "High", "Medium", or "Low" |
| `paper_section` | string | Reference to the paper (e.g., "Section IV-A, Listing 1") |
| `description` | string | Plain‑English explanation of what this technique does |
| `mitigation` | string | Recommended countermeasure (from Section IX‑B) |

### 3.3 Correlation Engine
| ID | Requirement | Description | Paper Reference |
|----|-------------|-------------|-----------------|
| REQ‑28 | **Input** | Takes the list of `Finding` objects from all detectors. | – |
| REQ‑29 | **Multi‑stage detection** | Identifies sequences of detectors that indicate a progressive fingerprinting attempt. For example: `@supports` followed by `@media` followed by `calc()`. | – |
| REQ‑30 | **Attack chain** | Detects chains like `@import` (loads external CSS) + `@media` with `url()` (exfiltration). | – |
| REQ‑31 | **Output** | Produces a list of correlation insights, each containing a description and a boost value (to be added to risk score). | – |

### 3.4 Risk Scoring
| ID | Requirement | Description |
|----|-------------|-------------|
| REQ‑32 | **Base scores** | Each finding has a base score: Critical = 30, High = 15, Medium = 8, Low = 3. |
| REQ‑33 | **Correlation boosts** | Each correlation insight contributes a boost (5–20) depending on the severity of the combination. |
| REQ‑34 | **Total calculation** | `score = min(100, sum(base_scores) + sum(boosts))` |
| REQ‑35 | **Label assignment** | 0–20 → Safe, 21–45 → Moderate, 46–70 → High, 71–100 → Critical. |

### 3.5 Command‑Line Interface (CLI)
| ID | Requirement | Description |
|----|-------------|-------------|
| REQ‑36 | **Arguments** | `--input` (required): path to `.eml` file. `--output` (optional): path for report (default: `report.html`). `--verbose` (flag): print findings to console. `--summary` (flag): only print risk score and label. |
| REQ‑37 | **Exit codes** | 0 for successful analysis, 1 for errors (file not found, invalid format). |

### 3.6 Web Interface (Flask)
| ID | Requirement | Description |
|----|-------------|-------------|
| REQ‑38 | **Upload form** | A simple HTML form that accepts an `.eml` file. |
| REQ‑39 | **Processing** | Upon upload, the system processes the email and displays the report in the browser. |
| REQ‑40 | **Download** | A button to download the report as a standalone HTML file. |
| REQ‑41 | **Error handling** | Show user‑friendly error messages for invalid files or processing failures. |

### 3.7 Reporting
| ID | Requirement | Description |
|----|-------------|-------------|
| REQ‑42 | **Metadata section** | Displays subject, sender, date. |
| REQ‑43 | **Risk summary** | Shows overall score and label with a color‑coded badge. |
| REQ‑44 | **Findings table** | Lists each finding with columns: technique, risk level, paper section, matched snippet (expandable), description, mitigation. |
| REQ‑45 | **Correlation insights** | Separate section listing each correlation and its boost. |
| REQ‑46 | **Mitigation section** | Summarizes defenses from paper Section IX‑B (e.g., use a proxy that inlines resources). |
| REQ‑47 | **Self‑contained** | No external CSS/JS dependencies; uses inline styles. |

---

## 4. External Interface Requirements

### 4.1 User Interfaces
- **CLI:** Terminal interaction as described in Section 3.5.
- **Web:** Simple, responsive interface with upload form and report display.

### 4.2 Hardware Interfaces
None.

### 4.3 Software Interfaces
| Interface | Purpose |
|-----------|---------|
| Python `email` | Parse MIME and extract HTML. |
| `beautifulsoup4` | Parse HTML and extract CSS. |
| `re` (regex) | Pattern matching for detectors. |
| `jinja2` | HTML report generation. |
| `flask` | Web application framework. |
| `pytest` | Testing. |

### 4.4 Communications Interfaces
- Web interface uses HTTP/HTTPS.
- No network requests during analysis.

---

## 5. Non‑Functional Requirements

| Category | Requirement | ID |
|----------|-------------|-----|
| **Performance** | Processing a single `.eml` file shall not exceed 2 seconds on an Intel i7‑1255U, 16 GB RAM. | NFR‑1 |
| **Security** | The system shall never execute or fetch any CSS/JavaScript content. | NFR‑2 |
| **Maintainability** | Code shall be modular with separate directories for parser, detectors, analyzer, scoring, reporter. | NFR‑3 |
| **Portability** | The system shall run on Windows, Linux, and macOS without modification. | NFR‑4 |
| **Reliability** | Unit tests shall cover at least 80% of the code; integration tests shall pass for provided test emails. | NFR‑5 |
| **Usability** | Reports shall be readable by non‑technical users; CLI shall have clear help text. | NFR‑6 |

---

## 6. Other Requirements

### 6.1 Legal / Regulatory
- The tool does not store or transmit email content except for local report generation.
- Users must comply with applicable privacy laws when analyzing emails.

### 6.2 Testing Requirements
- **Unit tests** for each detector using positive test cases from the paper (Listings 1 and 3).
- **Integration tests** covering full pipeline on sample `.eml` files.
- **Edge‑case tests** with malformed HTML, empty CSS, obfuscated patterns.
- **False‑positive tests** on at least 10 clean newsletters.

### 6.3 Documentation Requirements
- `README.md` with installation, usage, architecture, and references.
- This SRS document.
- In‑line code comments.
- Project report (8–10 pages) covering design, implementation, evaluation.

### 6.4 Project Deliverables
| Deliverable | Format | Due (Week) |
|-------------|--------|------------|
| Source code | GitHub repository | End of Week 4 |
| SRS | PDF / Markdown | Week 1 |
| Project report | PDF | Week 4 |
| Presentation slides | PPT / PDF | Week 4 |
| Live demo URL | Web link | Week 4 |

---

## Appendix A: Traceability Matrix

| Requirement ID | Paper Section | Detector / Module |
|----------------|---------------|-------------------|
| REQ‑10 | IV‑B, VIII‑C2 | @import detector |
| REQ‑13 | III‑B, IV‑A3 | @media detector |
| REQ‑16 | IV‑A, Listing 1 | @container detector |
| REQ‑19 | V‑A, Listing 3 | calc() detector |
| REQ‑22 | III‑B, IV‑C1 | @font‑face detector |
| REQ‑25 | IV‑B, IV‑C2 | @supports detector |
| REQ‑32 | – (custom) | Risk scoring |
| REQ‑46 | IX‑B | Mitigation section |

---

## Appendix B: Glossary

- **CSS At‑rule** – A statement that begins with `@` and controls how CSS behaves (e.g., `@media`, `@import`).
- **Container Query** – A CSS feature that applies styles based on the size of a parent container.
- **Fingerprinting** – Techniques to collect unique attributes of a user’s environment for tracking.
- **MIME** – Multipurpose Internet Mail Extensions, used to encode email content.
- **Exfiltration** – The act of sending collected data to an attacker‑controlled server (via `url()` in CSS).

---

## Appendix C: Team Role Distribution

| Role | Member A | Member B |
|------|----------|----------|
| **Parser** | ✅ | – |
| **CSS Extractor** | ✅ | – |
| **Detectors** | @import, @media, @container | calc(), @font-face, @supports |
| **Correlation Engine** | ✅ | – |
| **Risk Scoring** | – | ✅ |
| **CLI** | ✅ | – |
| **Flask Web App** | – | ✅ |
| **HTML Report** | – | ✅ |
| **Testing** | Shared | Shared |
| **Documentation** | Shared | Shared |
| **PPT** | Technical slides | Design & lead |

---

## Appendix D: Implementation Timeline (4 Weeks)

| Week | Member A | Member B |
|------|----------|----------|
| **1** | Setup, parser, CSS extractor, unit tests | Setup, Flask skeleton, sample emails, report template |
| **2** | Detectors (import, media, container), correlation (basic) | Detectors (calc, font-face, supports), risk scoring design |
| **3** | Complete correlation, CLI integration, tests | Finish scoring, Flask integration, report styling |
| **4** | Deployment, integration tests, performance | Finalize PPT, project report, user guide |

---

**End of SRS**