import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask, render_template, request
from eml_parser import parse_eml
from css_extractor import extract_all_css

# 🔥 Import all detectors
from detectors.import_detector import detect_import_rules
from detectors.media_detector import detect_media_queries
from detectors.container_detector import detect_container_queries
from detectors.calc_detector import detect_calc
from detectors.fontface_detector import detect_fontface
from detectors.supports_detector import detect_supports

# 🔥 NEW IMPORTS
from correlation_engine import CorrelationEngine
from risk_scoring import calculate_risk_score
from reporter.html_reporter import generate_html_report

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        if "file" not in request.files:
            return "No file uploaded"

        file = request.files["file"]

        filepath = f"temp_{file.filename}"
        file.save(filepath)

        # Step 1: Parse
        html, metadata = parse_eml(filepath)

        # 🔥 HANDLE PLAIN TEXT EMAILS
        if html is None:
            return f"""
            <html>
            <head>
                <title>Email Analysis Result</title>
                <style>
                    body {{
                        font-family: Arial;
                        text-align: center;
                        margin-top: 100px;
                    }}
                    .box {{
                        display: inline-block;
                        padding: 30px;
                        border: 1px solid #ccc;
                        border-radius: 10px;
                        box-shadow: 0px 0px 10px rgba(0,0,0,0.1);
                    }}
                    .safe {{
                        color: green;
                        font-size: 24px;
                        font-weight: bold;
                    }}
                </style>
            </head>
            <body>

                <div class="box">
                    <h2>Plain Text Email Detected</h2>

                    <p>This email contains <b>no HTML or CSS content</b>.</p>
                    <p>No CSS-based fingerprinting or tracking is possible.</p>

                    <p class="safe">Status: SAFE ✅</p>

                    <hr>
                    <p><b>Subject:</b> {metadata.get("subject", "N/A")}</p>
                    <p><b>From:</b> {metadata.get("from", "N/A")}</p>
                    <p><b>Date:</b> {metadata.get("date", "N/A")}</p>

                    <br><br>
                    <a href="/">⬅️ Analyze another email</a>
                </div>

            </body>
            </html>
            """

        # Step 2: Extract CSS
        css_snippets = extract_all_css(html)

        # 🔥 Step 3: Run ALL detectors
        findings = []
        findings.extend(detect_import_rules(css_snippets))
        findings.extend(detect_media_queries(css_snippets))
        findings.extend(detect_container_queries(css_snippets))
        findings.extend(detect_calc(css_snippets))
        findings.extend(detect_fontface(css_snippets))
        findings.extend(detect_supports(css_snippets))

        # 🔗 Step 4: Correlation
        corr_engine = CorrelationEngine(findings)
        insights = corr_engine.get_correlation_insights()

        # 🔢 Step 5: Risk Scoring
        risk = calculate_risk_score(findings, insights)

        # 📄 Step 6: Generate HTML report
        output_path = "temp_report.html"
        generate_html_report(findings, metadata, risk, insights, output_path)

        # Return report
        with open(output_path, "r", encoding="utf-8") as f:
            html_report = f.read()

        return html_report

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)