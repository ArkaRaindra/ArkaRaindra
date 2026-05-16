import requests
import xml.etree.ElementTree as ET
import re

RSS_URL = "https://myanimelist.net/rss.php?type=rwe&u=ArkaNotHere"

response = requests.get(RSS_URL)
root = ET.fromstring(response.content)

items = root.findall("./channel/item")

anime_html = []
added = set()

for item in items:
    title = item.find("title").text
    link = item.find("link").text
    desc = item.find("description").text.strip()

    if title in added:
        continue

    added.add(title)

    anime_id = link.split("/")[4]

    image_url = f"https://cdn.myanimelist.net/images/anime/{anime_id}.jpg"

    card = f"""
<table>
<tr>
<td width="70%">

### [{title}]({link})

✨ {desc}

</td>

<td align="right">
<img src="{image_url}" width="120"/>
</td>
</tr>
</table>

"""

    anime_html.append(card)

    if len(anime_html) >= 5:
        break

with open("README.md", "r", encoding="utf-8") as f:
    readme = f.read()

start = "<!-- MAL-START -->"
end = "<!-- MAL-END -->"

new_content = start + "\n" + "\n".join(anime_html) + "\n" + end

updated = re.sub(
    f"{start}[\\s\\S]*?{end}",
    new_content,
    readme
)

with open("README.md", "w", encoding="utf-8") as f:
    f.write(updated)

print("README updated!")
