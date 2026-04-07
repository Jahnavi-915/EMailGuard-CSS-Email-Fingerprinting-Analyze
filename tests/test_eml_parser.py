import tempfile
from eml_parser import parse_eml


def test_parse_simple_email():
    # 🔹 Step 1: Create dummy email content
    eml_content = """Subject: Test Email
From: test@example.com
Date: Mon, 1 Jan 2024 10:00:00 +0000
Content-Type: text/html; charset="utf-8"

<html>
  <body>
    <h1>Hello World</h1>
    <style>
      body { color: red; }
    </style>
  </body>
</html>
"""

    # 🔹 Step 2: Create temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".eml") as tmp:
        tmp.write(eml_content.encode("utf-8"))
        tmp_path = tmp.name

    # 🔹 Step 3: Run parser
    html, metadata = parse_eml(tmp_path)

    # 🔹 Step 4: Assertions
    assert html is not None
    assert "<html>" in html.lower()
    assert "hello world" in html.lower()

    assert metadata["subject"] == "Test Email"
    assert metadata["from"] == "test@example.com"
    assert "2024" in metadata["date"]