import requests
import re
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
req = requests.get("https://images.search.yahoo.com/search/images?p=Buruli+ulcer", headers=headers)
urls = re.findall(r'imgurl=&quot;(http.*?)&quot;', req.text)
print(f"Yahoo found {len(urls)} urls. First 3: {urls[:3]}")
