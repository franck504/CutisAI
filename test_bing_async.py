import requests
import re
keyword = "Buruli ulcer lesion"
urls = []
for offset in [1, 150, 300]:
    url = f"https://www.bing.com/images/async?q={keyword}&first={offset}&count=150"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    }
    response = requests.get(url, headers=headers, timeout=15)
    batch = re.findall(r'murl&quot;:&quot;(.*?)&quot;', response.text)
    urls.extend(batch)
    print(f"Offset {offset}: found {len(batch)} urls")

urls = [u for u in urls if u.startswith("http")]
print(f"Total unique Bing URLs: {len(set(urls))}")
