import requests
import re
keyword = "Buruli ulcer lesion"
urls = []
for page in [0, 60, 120, 180]:
    url = f"https://images.search.yahoo.com/search/images?p={keyword}&b={page}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    }
    response = requests.get(url, headers=headers, timeout=15)
    batch = re.findall(r'imgurl=&quot;(http.*?)&quot;', response.text)
    urls.extend(batch)
    print(f"B={page}: found {len(batch)} urls")

urls = [u for u in urls if u.startswith("http")]
print(f"Total unique Yahoo URLs: {len(set(urls))}")
