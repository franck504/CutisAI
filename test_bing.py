import requests
import re
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
req = requests.get("https://www.bing.com/images/search?q=Buruli+ulcer", headers=headers)
urls = re.findall(r'"murl":"(.*?)"', req.text)
print(f"Bing found {len(urls)} urls. First 3: {urls[:3]}")
