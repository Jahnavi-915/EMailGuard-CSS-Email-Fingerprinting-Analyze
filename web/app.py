import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask, render_template, request
from eml_parser import parse_eml
from css_extractor import extract_all_css

# ✅ DEFINE APP FIRST
app = Flask(__name__)

# ✅ THEN USE ROUTES
@app.route("/", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        if "file" not in request.files:
            return "No file uploaded"

        file = request.files["file"]

        filepath = f"temp_{file.filename}"
        file.save(filepath)

        html, metadata = parse_eml(filepath)

        if html is None:
            return "Failed to parse email"

        css_snippets = extract_all_css(html)

        return render_template(
            "report.html",
            metadata=metadata,
            css_snippets=css_snippets
        )

    return render_template("index.html")


# ✅ RUN APP LAST
if __name__ == "__main__":
    app.run(debug=True)