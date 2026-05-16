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

    # Thumbnail Jikan CDN
    image_url = f"https://cdn.myanimelist.net/images/anime/{anime_id}.jpg"

    block = f"""
<table>
<tr>
<td width="75%">

### [{title}]({link})

```diff
{desc}
