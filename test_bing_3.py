import requests
import re
resp = requests.get("https://www.bing.com/images/search?q=cat", headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
print([re.findall(r'murl&quot;:&quot;(.*?)&quot;', resp.text)[:3]])
print([re.findall(r'murl":"(.*?)"', resp.text)[:3]])
