import requests
import re

url = "https://images.search.yahoo.com/search/images?p=cat"
headers = {"User-Agent": "Mozilla/5.0"}
resp = requests.get(url, headers=headers)
urls = re.findall(r'imgurl=&quot;(.*?)&quot;', resp.text)
print(f"Old regex urls: {len(urls)}")

urls_new = re.findall(r'src="(http[^"]+)"', resp.text)
print(f"New regex urls: {len(urls_new)}")
