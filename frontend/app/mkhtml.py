# This file is being archived on 15.11.2026 and is not part of the new version.
import markdown_fastapi_rs


def markdown_to_html(input: str) -> str:
    return markdown_fastapi_rs.md_to_html(input)
