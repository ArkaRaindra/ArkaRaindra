import requests
import xml.etree.ElementTree as ET
import re

RSS_URL = "https://myanimelist.net/rss.php?type=rwe&u=ArkaNotHere"

response = requests.get(RSS_URL)
root = ET.fromstring(response.content)

items = root.findall("./channel/item")

cards = []
added = set()

for item in items:
title = item.find("title").text
link = item.find("link").text
desc = item.find("description").text.strip()

```
if title in added:
    continue

added.add(title)

status = desc.replace("<![CDATA[", "").replace("]]>", "").strip()

card = f"""
```

<a href="{link}">
  <img src="https://img.shields.io/badge/{title.replace(' ', '%20')}-{status.replace(' ', '%20')}-ff69b4?style=for-the-badge&logo=myanimelist&logoColor=white"/>
</a>
"""

```
cards.append(card)

if len(cards) >= 10:
    break
```

with open("README.md", "r", encoding="utf-8") as f:
readme = f.read()

start = "<!-- MAL-START -->"
end = "<!-- MAL-END -->"

replacement = start + "\n" + "\n".join(cards) + "\n" + end

updated = re.sub(
f"{start}[\s\S]*?{end}",
replacement,
readme
)

with open("README.md", "w", encoding="utf-8") as f:
f.write(updated)

print("README updated!")
