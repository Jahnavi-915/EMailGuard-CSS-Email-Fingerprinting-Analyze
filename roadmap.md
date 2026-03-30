Here is the final, execution‑ready roadmap. It incorporates all the improvements discussed, balances the workload, and gives you clear milestones to hit each week.

---

## Final Roadmap: EMailGuard – CSS Email Fingerprinting Analyzer

**Team:** 2 Members  
**Duration:** 4 Weeks  
**Goal:** Deliver a fully functional tool with CLI, web interface, six detectors, correlation, risk scoring, and an HTML report, ready for demo and submission.

---

### Guiding Principles
- **MVP by end of Week 2** – you always have something to show.  
- **Design before code** – correlation rules are sketched in Week 1.  
- **Prioritise depth** – 4 solid detectors + correlation > 6 mediocre ones.  
- **Daily 10‑min sync** – unblock quickly and stay aligned.

---

## Week 1 – Foundation + Correlation Design (Days 1–7)

**Goal:** Solid parser, CSS extraction, and a clear plan for correlation rules.

| Task | Member A | Member B |
|------|----------|----------|
| **Setup** | Git repo, Python venv, project structure (e.g., `parser/`, `detectors/`, `correlator/`, `scorer/`, `reporter/`, `cli/`, `web/`, `tests/`). Install dependencies: beautifulsoup4, flask, jinja2, pytest. | Same (collaborate). |
| **Parser** | Implement `.eml` reading, MIME decoding, base64/quoted‑printable handling. Extract headers (Subject, From, Date). | Build a test email corpus: at least 10 `.eml` files covering all six attack types plus clean newsletters. |
| **HTML & CSS Extraction** | Use BeautifulSoup to extract `<style>` tags, inline `style` attributes, `<link rel="stylesheet">` URLs, and `@import` URLs (record but do not fetch). | Validate extraction against the test corpus. |
| **Finding Object** | Define `Finding` class with fields: `technique`, `snippet`, `risk_level`, `paper_section`, `description`, `mitigation`. | Same; align on structure. |
| **Correlation Design** | Draft a simple rule engine: store rules as a list of (condition, boost). Example: if `@import` + `@media` with `url()` → boost 15. | Map attack chains from paper (Section IX‑B) to concrete rules. |
| **Unit Tests** | Write tests for parser functions (file reading, MIME, header extraction). | Write tests for CSS extraction (style tags, inline styles, `@import` detection). |

**Deliverables:**  
- Working parser module.  
- `Finding` class defined.  
- Correlation rule skeleton (rules stored in a config or code).  
- Test email corpus.  
- Initial unit tests.

---

## Week 2 – MVP: First Detectors + Basic Report (Days 8–14)

**Goal:** Minimum viable analyzer – at least 4 detectors, basic CLI, simple HTML report.

| Task | Member A | Member B |
|------|----------|----------|
| **Detectors – Priority Group** | – `@import` chain (Critical)<br>– `@media` conditional (Critical/Medium)<br>– `@font‑face` remote (High) | – `calc()` expression (High)<br>– (optional) `@supports` probe (Medium)<br>– (optional) `@container` query (Critical/High) |
| **Risk Scoring (MVP)** | – | Implement base scoring: Critical 30, High 15, Medium 8, Low 3. Total score = sum of base scores (correlation not yet included). |
| **CLI (MVP)** | Build `cli.py` with `--input` flag, prints findings to console, basic exit codes. | – |
| **Report (MVP)** | – | Jinja2 template showing risk score, list of findings (technique, risk, snippet, description, mitigation). Self‑contained CSS. |
| **Integration** | Wire parser, detectors, scoring, and CLI into a simple script. | – |
| **Testing** | Unit tests for each implemented detector. | Test scoring and report template. |

**Deliverables:**  
- At least 4 working detectors with unit tests.  
- CLI that can analyze an `.eml` and print findings.  
- Basic HTML report (no correlations yet).  
- **MVP ready to demo.**

---

## Week 3 – Correlation, Full Scoring, Web Interface (Days 15–21)

**Goal:** Complete the intelligence layer and make the tool usable via web.

| Task | Member A | Member B |
|------|----------|----------|
| **Correlation Engine** | Implement the rule engine from Week 1. Scan findings, detect chains, produce correlation insights with boosts (5–20). | Help refine rules by testing on the corpus. |
| **Final Risk Scoring** | Integrate correlation boosts into total score, clamp to 0–100, map to label (Safe/Moderate/High/Critical). | Validate scoring logic with edge cases. |
| **Flask Web App** | – | Build upload form, process email, display report in browser. Add download button. Handle errors gracefully. |
| **Report (final)** | – | Add correlation insights section, expandable CSS snippets, paper references, mitigation summary (from Section IX‑B). |
| **Integration Testing** | Test full pipeline (parser → detectors → correlation → scoring) on all test emails. | Test web upload and report generation. |

**Deliverables:**  
- Complete correlation engine.  
- Full risk scoring with boosts.  
- Fully functional Flask web app.  
- Final HTML report format.

---

## Week 4 – Polish, Testing, Documentation, Wow Factor (Days 22–28)

**Goal:** Deliver a production‑ready tool with standout features.

| Task | Member A | Member B |
|------|----------|----------|
| **Testing & Buffer** | Achieve 80% unit test coverage. Run edge‑case tests (malformed HTML, obfuscated patterns). Perform false‑positive test on 10 clean newsletters. | Test on Windows, Linux, macOS. Manual UI/UX testing. |
| **Performance** | Profile processing time; ensure <2 seconds per file on reference hardware. | Optimise report rendering if needed. |
| **Documentation** | In‑line code comments. Contribute to README (installation, usage, architecture). | User guide for web interface. Write project report (8–10 pages). Prepare presentation slides. |
| **Wow Factor (choose one)** | **Option A (explainability):** Add a plain‑English “Why this email is risky” summary in the report. | **Option B (visualisation):** Add a simple graph of attack chains (e.g., using D3.js). |
| **Deployment** | Prepare deployment instructions (Render, Railway, or local). | Deploy Flask app to a public URL; verify live demo. |
| **Final Deliverables** | Push final source code to GitHub. Submit SRS (already done). Contribute to project report. | Submit project report PDF, presentation slides, and live demo URL. |

---

## Workload & Priority Notes

- **Detectors:** If time is tight in Week 2, focus on these four:  
  `@import`, `@media`, `@font‑face`, `calc()` – they cover the highest‑risk techniques and the most distinctive patterns.
- **Correlation:** Start with a few obvious chains (e.g., `@import` + `@media` with `url()`, `@supports` + `@media` + `calc()`). You can always add more later.
- **Flask:** Start the skeleton at the end of Week 2 to catch encoding/file‑upload bugs early.
- **Daily sync:** 10 minutes, just to unblock and align.

---

## Summary of Deliverables by Week

| Week | Deliverables |
|------|--------------|
| 1 | Parser, CSS extraction, Finding object, correlation rule design, test corpus, unit tests |
| 2 | 4+ detectors, basic CLI, simple HTML report, MVP demo |
| 3 | Full correlation, final scoring, Flask web app, final report format |
| 4 | High test coverage, documentation, live demo, project report, presentation, wow feature |

---

**Final note:** This roadmap is designed to be **execution‑ready**. Stick to the milestones, prioritise depth, and you’ll have a project that impresses both evaluators and future interviewers. Good luck! 🚀