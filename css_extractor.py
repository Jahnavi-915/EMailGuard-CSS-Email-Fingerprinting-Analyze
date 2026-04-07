# css_extractor.py
from bs4 import BeautifulSoup
import re
import base64
from typing import List

def decode_data_url(data_url: str) -> str:
    """Extract and decode content from data: URL (supports base64)."""
    # Pattern: data:[<mediatype>][;base64],<data>
    match = re.match(r'data:[^,;]*(?:;base64)?,(.*)', data_url, re.DOTALL)
    if not match:
        return ""
    encoded = match.group(1)
    if ';base64' in data_url[:100]:
        try:
            decoded = base64.b64decode(encoded).decode('utf-8', errors='replace')
            return decoded
        except Exception:
            return ""
    else:
        # plain text (not base64)
        return encoded

def extract_all_css(html: str) -> List[str]:
    soup = BeautifulSoup(html, 'html.parser')
    css_snippets = []

    # <style> tags
    for style_tag in soup.find_all('style'):
        if style_tag.string:
            css_snippets.append(style_tag.string)

    # inline styles
    for tag in soup.find_all(style=True):
        css_snippets.append(f"{{ {tag['style']} }}")

    # <link rel="stylesheet"> - handle both external and data: URLs
    for link in soup.find_all('link', rel='stylesheet'):
        href = link.get('href')
        if href:
            if href.startswith('data:'):
                decoded_css = decode_data_url(href)
                if decoded_css:
                    css_snippets.append(decoded_css)
            else:
                css_snippets.append(f"/* LINK: {href} */")

    # @import statements (also inside existing CSS)
    all_css = "\n".join(css_snippets)
    import_pattern = r'@import\s+url\([\'"]?([^\'"\)]+)[\'"]?\)'
    imports = re.findall(import_pattern, all_css, re.IGNORECASE)
    for imp in imports:
        css_snippets.append(f"@import url({imp});")

    return css_snippets