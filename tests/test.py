from pathlib import Path
import requests


url = "https://example.com/page"

response = requests.get(
    url,
    headers={
        "User-Agent": "Mozilla/5.0",
    },
    timeout=(5, 15),
)
response.raise_for_status()

Path("page.html").write_text(response.text, encoding="utf-8")


response = parser.session.get(url, timeout=(5, 15))
response.raise_for_status()

with open("tests/html/page.html", "w", encoding="utf-8") as file:
    file.write(response.text)
