# 🚀 Final Execution‑Ready Roadmap

## EMailGuard – CSS Email Fingerprinting Analyzer

**Team Size:** 2 | **Duration:** 4 Weeks | **Based on:** *Cascading Spy Sheets* (NDSS 2025)  
**Artifact:** https://github.com/cispa/cascading-spy-sheets (only email PoCs)

---

## 📌 Core Commitments (Non‑Negotiable)

| Area | Commitment |
|------|-------------|
| **Scope** | 6 detectors, correlation engine, risk scoring, CLI + Flask web UI |
| **Dataset** | 15–20 emails: 4–5 paper PoCs + 5–8 synthetic attacks + 5–10 clean |
| **MVP** | By end of Week 2: CLI can parse, detect, and output findings (even if report is plain text) |
| **Quality** | Unit tests for each detector; integration test on full dataset; false positive measurement |

---

## 👥 Role Distribution (Final)

| Module | Member A | Member B |
|--------|----------|----------|
| `.eml` parser + CSS extractor | ✅ | – |
| Detectors | `@import`, `@media`, `@container` | `calc()`, `@font-face`, `@supports` |
| Correlation engine | ✅ | – |
| Risk scoring | – | ✅ |
| CLI | ✅ | – |
| Flask web app | – | ✅ |
| HTML report (Jinja2) | – | ✅ |
| Unit tests (own detectors) | ✅ | ✅ |
| Integration tests | Shared | Shared |
| Dataset creation | Shared | Shared |
| Documentation & PPT | Shared (A: technical slides; B: design lead) | Shared |
| Deployment (Render) | ✅ | – |

---

## 📅 Week‑by‑Week Execution Plan

### Week 1 – Foundation & Parsing (Days 1–7)

**Goal:** Project skeleton, parser, CSS extractor, and test harness.

| Day | Member A | Member B |
|-----|----------|----------|
| 1–2 | Create repo, venv, `requirements.txt`. Implement `eml_parser.py` (extract HTML + metadata). | Same setup. Create Flask skeleton (upload route, basic HTML). Download artifact email PoCs. |
| 3–4 | Implement `css_extractor.py` (`<style>`, inline, `<link>`, `@import`). Unit tests. | Create `test_samples/` with 4 paper PoCs. Write script to test parser on them. |
| 5–7 | Integrate parser+extractor into `main.py` (CLI stub: `--input`). Test on all PoCs. | Build Jinja2 HTML template with placeholders (metadata, findings table). |

**End Week 1 Deliverables:**  
✔ Parser works on all paper PoCs.  
✔ CLI can print extracted CSS.  
✔ Flask can upload and show dummy report.  
✔ `test_samples/` has 4 `.eml` files.

---

### Week 2 – Detectors (Core Fingerprinting Logic)

**Goal:** All 6 detectors implemented, unit tested, and integrated into CLI.

| Day | Member A | Member B |
|-----|----------|----------|
| 8–9 | Detector: `@import` chain (Critical). Unit test on paper PoCs. | Detector: `calc()` expression (High). Unit test. |
| 10–11 | Detector: `@media` conditional (Critical). Unit test. | Detector: `@font-face` remote (High). Unit test. |
| 12–13 | Detector: `@container` query (Critical/High). Unit test. | Detector: `@supports` probe (High). Unit test. |
| 14 | Integrate all 6 detectors into `main.py`. Run on paper PoCs – verify detection. | Create **5–8 synthetic attack emails** (nested `@media`, obfuscated `calc()`, multiple `@import`, etc.). |

**End Week 2 Deliverables:**  
✔ 6 detectors with passing unit tests.  
✔ `main.py --input file.eml --verbose` prints findings.  
✔ Synthetic dataset (5–8 `.eml` files) ready.

---

### Week 3 – Correlation, Scoring, Reporting, Web Integration

**Goal:** Add intelligence, full reporting, and web UI.

| Day | Member A | Member B |
|-----|----------|----------|
| 15–16 | Implement correlation engine: rule‑based (sequences like `@supports`→`@media`→`calc()`; chains like `@import`+`@media`). | Implement risk scoring: base scores (Critical=30, High=15, Medium=8, Low=3) + correlation boosts → total score → label (Safe/Moderate/High/Critical). |
| 17–18 | Integrate correlator into `main.py`. Test on synthetic multi‑stage emails. | Integrate scoring into `main.py`. Verify labels. |
| 19–20 | Implement HTML report generator (`reporter/html_reporter.py`) – uses Jinja2, includes metadata, findings table, correlation insights, mitigations. | Enhance Flask app: after upload, run full pipeline, display report, add download button. |
| 21 | Collect **5–10 clean emails** (from your inbox). Run full pipeline on all 15–20 emails. Record detection rate & false positives. | Write integration tests (`test_integration.py`) – end‑to‑end on entire dataset. |

**End Week 3 Deliverables:**  
✔ Correlation & scoring working.  
✔ CLI produces HTML report (via `--output`).  
✔ Flask app shows full report.  
✔ Evaluation metrics (detection %, false positive %) calculated.

---

### Week 4 – Polish, Documentation, Deployment, Presentation

**Goal:** Final deliverables, live demo, report, PPT.

| Day | Member A | Member B |
|-----|----------|----------|
| 22–23 | Deploy Flask app on Render (free tier). Set `gunicorn app:app`. Test live URL. | Finalise PPT: title, problem, architecture, detectors, correlation, results, demo, challenges, future work. |
| 24–25 | Write `README.md` (installation, usage, architecture, link to paper, live demo URL, screenshots). | Write project report (8–10 pages): abstract, intro (paper summary), requirements, design, implementation, evaluation (metrics, false positives), conclusion, references. |
| 26–27 | Final code cleanup, docstrings, run all tests. | Review report, add architecture diagram (from SRS). Prepare viva answers. |
| 28 | Push final code to GitHub. Submit report PDF, PPT, live demo link. | Practice presentation (10–12 min). |

**End Week 4 Deliverables:**  
✔ Fully working CLI + web tool.  
✔ Live demo URL (optional but recommended).  
✔ Complete README + project report.  
✔ PPT slides.  
✔ GitHub repo public/shared.

---

## 🧪 How to Use the Artifact (Step‑by‑Step)

1. **Clone the artifact** (outside your project folder):
   ```bash
   git clone https://github.com/cispa/cascading-spy-sheets.git
   ```
2. **Copy only the email PoCs** into your `test_samples/paper_pocs/`:
   - `pocs/email/osdetect/osdetect.eml`
   - `pocs/email/officedetect/officedetect.eml`
   - `pocs/email/styledetect/styledetect.eml`
   - `pocs/email/printdetect/printdetect.eml`
   - (Optional) any `.eml` from `pocs/examples/` that uses email‑like HTML.
3. **Ignore** `pocs/browser/`, `pocs/extensions/`, `evaluation/browser/`, `mitigation/browser/`.
4. **Do NOT copy code** – only use the `.eml` files as test inputs.

---

## 📊 Dataset Construction (15–20 Emails)

| Category | Count | Source |
|----------|-------|--------|
| Paper PoCs | 4–5 | Artifact (copied as above) |
| Synthetic attacks | 5–8 | Create by modifying PoCs: nested `@media`, obfuscated `calc()`, multiple `@import`, inline‑only CSS, malformed CSS |
| Clean emails | 5–10 | Export newsletters from your own email (as `.eml`) or create simple HTML emails with no CSS |

**Organisation:**  
```
test_samples/
├── paper_pocs/      (4–5 files)
├── synthetic/       (5–8 files)
└── clean/           (5–10 files)
```

---

## 🧠 Micro‑Optimisations (Do Not Skip)

1. **Start Flask early** – add a basic upload page by end of Week 2 to catch encoding bugs early.
2. **Lock detector output format in Week 1** – define the `Finding` dataclass (technique, snippet, risk, paper_section, description, mitigation).
3. **Keep correlation simple** – use explicit rules like `if detector_X and detector_Y: boost += 10`. No nested logic.
4. **Track metrics from Week 3** – as soon as dataset is ready, run the full pipeline and log detection rate and false positives.

---

## 📈 Evaluation Metrics (Report These)

- **Detection rate** = (attacks correctly flagged) / (total attack emails) × 100%
- **False positive rate** = (clean emails flagged risky) / (total clean emails) × 100%
- **Per‑detector accuracy** (on its own test cases)
- **Average processing time** per email (target < 2 sec)

**Expected realistic results:**  
- Paper PoCs: 95–100% detection  
- Synthetic: 80–90%  
- Clean: 0–10% false positives

---

## 🏁 Final Checklist (Before Submission)

- [ ] Repo has all source code, `requirements.txt`, `README.md`.
- [ ] `test_samples/` contains 15–20 `.eml` files (paper + synthetic + clean).
- [ ] CLI works: `python main.py --input sample.eml --output report.html --verbose`.
- [ ] Flask app works locally and (if deployed) on Render.
- [ ] Unit tests pass (`pytest tests/`).
- [ ] Integration test passes on full dataset.
- [ ] Report includes evaluation metrics.
- [ ] PPT is ready (10–12 slides).
- [ ] Project report (8–10 pages) submitted.
- [ ] Live demo URL (optional) is accessible.

---
