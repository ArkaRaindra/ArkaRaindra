import requests
import re

USERNAME = "ArkaNotHere"
JIKAN_V4 = f"https://api.jikan.moe/v4/users/{USERNAME}/history/anime"

def fetch_mal_history():
    response = requests.get(JIKAN_V4)
    response.raise_for_status()
    data = response.json()
    entries = data.get("data", [])[:10]

    lines = []
    for entry in entries:
        title = entry["entry"]["name"]
        url = entry["entry"]["url"]
        increment = entry["increment"]
        date = entry["date"][:10]
        lines.append(f"- [{title}]({url}) — +{increment} ep · {date}")

    return "\n".join(lines) if lines else "_No recent activity found._"

def update_readme(content):
    with open("README.md", "r", encoding="utf-8") as f:
        readme = f.read()

    new_section = f"<!-- MAL_ACTIVITY:start -->\n{content}\n<!-- MAL_ACTIVITY:end -->"
    updated = re.sub(
        r"<!-- MAL_ACTIVITY:start -->.*?<!-- MAL_ACTIVITY:end -->",
        new_section,
        readme,
        flags=re.DOTALL,
    )

    with open("README.md", "w", encoding="utf-8") as f:
        f.write(updated)

if __name__ == "__main__":
    update_readme(fetch_mal_history())
