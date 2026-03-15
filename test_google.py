import requests
import re
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
req = requests.get("https://www.google.com/search?q=Buruli+ulcer&tbm=isch", headers=headers)
urls = re.findall(r'\["(http.*?)"', req.text)
print(f"Google found {len(urls)} urls. First 3: {urls[:3]}")
