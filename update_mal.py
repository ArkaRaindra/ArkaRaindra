import requests
import xml.etree.ElementTree as ET
import re
from bs4 import BeautifulSoup

RSS_URL = "https://myanimelist.net/rss.php?type=rwe&u=ArkaNotHere"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(RSS_URL, headers=headers)
root = ET.fromstring(response.content)

items = root.findall("./channel/item")

anime_html = []
added = set()

def get_cover(url):
    try:
        page = requests.get(url, headers=headers)
        soup = BeautifulSoup(page.text, "html.parser")

        img = soup.find("img", {"itemprop": "image"})

        if img:
            return img["data-src"] if img.get("data-src") else img["src"]

    except:
        pass

    return "https://via.placeholder.com/120x170?text=No+Image"

for item in items:
    title = item.find("title").text
    link = item.find("link").text
    desc = item.find("description").text.strip()

    if title in added:
        continue

    added.add(title)

    cover = get_cover(link)

    card = f"""
<table>
<tr>
<td width="75%">

## [{title}]({link})

{desc}

</td>

<td align="right">

<img src="{cover}" width="120"/>

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
