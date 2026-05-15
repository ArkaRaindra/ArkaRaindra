import requests
import xml.etree.ElementTree as ET

RSS_URL = "https://myanimelist.net/rss.php?type=rwe&u=ArkaNotHere"

response = requests.get(RSS_URL)
root = ET.fromstring(response.content)

items = root.findall("./channel/item")

anime_list = []

added = set()

for item in items:
    title = item.find("title").text
    desc = item.find("description").text.strip()

    if title not in added:
        anime_list.append(f"- **{title}** → {desc}")
        added.add(title)

    if len(anime_list) >= 10:
        break

with open("README.md", "r", encoding="utf-8") as f:
    readme = f.read()

start = "<!-- MAL-START -->"
end = "<!-- MAL-END -->"

new_content = start + "\n" + "\n".join(anime_list) + "\n" + end

import re

updated = re.sub(
    f"{start}[\\s\\S]*?{end}",
    new_content,
    readme
)

with open("README.md", "w", encoding="utf-8") as f:
    f.write(updated)

print("README updated!")
