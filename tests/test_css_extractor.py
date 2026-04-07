from css_extractor import extract_all_css


def test_extract_all_css_basic():
    html = """
    <html>
        <head>
            <style>
                body { background: red; }
                @import url("test.css");
            </style>
            <link rel="stylesheet" href="style.css">
        </head>
        <body>
            <div style="color: blue;">Hello</div>
        </body>
    </html>
    """

    css = extract_all_css(html)

    # 🔹 Basic checks
    assert css is not None
    assert isinstance(css, list)
    assert len(css) > 0

    # 🔹 Check <style> content
    assert any("background: red" in c for c in css)

    # 🔹 Check inline style
    assert any("color: blue" in c for c in css)

    # 🔹 Check link extraction
    assert any("style.css" in c for c in css)

    # 🔹 Check @import extraction
    assert any("@import url(test.css)" in c or "test.css" in c for c in css)