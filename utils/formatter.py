import re
import html

def markdown_to_html(text: str) -> str:

    def code_block_replacer(match):
        code_content = match.group(2)
        escaped = html.escape(code_content.strip())
        return f"<pre><code>{escaped}</code></pre>"

    text = re.sub(
        r"```(\w+)?\n?(.*?)```",
        code_block_replacer,
        text,
        flags=re.DOTALL
    )

    def inline_code_replacer(match):
        code_content = match.group(1)
        escaped = html.escape(code_content)
        return f"<code>{escaped}</code>"
        
    text = re.sub(
        r"(?<!`)`([^`\n]+)`",
        inline_code_replacer,
        text
    )

    return text
