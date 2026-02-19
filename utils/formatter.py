import html
import re

def has_code_block(text: str) -> bool:
    return "```" in text

def extract_code_language(text: str):
    match = re.search(r"```(\w+)?", text)
    if match:
        return match.group(1)
    return None

def to_html_codeblock(text: str) -> str:
    cleaned = re.sub(r"```(\w+)?", "", text)
    cleaned = cleaned.replace("```", "")
    escaped = html.escape(cleaned.strip())
    return f"<pre><code>{escaped}</code></pre>"
