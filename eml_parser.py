import email
from email import policy
from email.parser import BytesParser
import base64
import quopri
from typing import Optional, Dict, Tuple

def parse_eml(file_path: str) -> Tuple[Optional[str], Dict[str, str]]:
    """
    Returns (html_content, metadata)
    metadata = {'subject': ..., 'from': ..., 'date': ...}
    """
    with open(file_path, 'rb') as f:
        msg = BytesParser(policy=policy.default).parse(f)

    metadata = {
        'subject': msg.get('Subject', ''),
        'from': msg.get('From', ''),
        'date': msg.get('Date', '')
    }

    html_content = None

    def extract_html_part(part):
        nonlocal html_content
        if part.get_content_type() == 'text/html':
            payload = part.get_payload(decode=True)
            charset = part.get_content_charset() or 'utf-8'
            html_content = payload.decode(charset, errors='replace')
        elif part.is_multipart():
            for subpart in part.get_payload():
                extract_html_part(subpart)

    extract_html_part(msg)
    return html_content, metadata