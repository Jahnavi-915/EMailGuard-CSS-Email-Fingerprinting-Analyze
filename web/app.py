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

        if html is None:
            return "Failed to parse email"

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

        return render_template(
            "report.html",
            metadata=metadata,
            css_snippets=css_snippets,
            findings=findings
        )

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)