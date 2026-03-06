import requests
import json
import os
# 修改第 6 行和第 8 行，确保与 GitHub Secrets 的名称完全一样
ACCOUNT = os.getenv('CF_ACCOUNT_ID')
NAMESPACE = os.getenv('CF_NAMESPACE')
TOKEN = os.getenv('CF_API_TOKEN')
countries = {
    "US": "https://raw.githubusercontent.com/cmliu/CFcdnIP/master/US.txt",
    "JP": "https://raw.githubusercontent.com/cmliu/CFcdnIP/master/JP.txt",
    "HK": "https://raw.githubusercontent.com/cmliu/CFcdnIP/master/HK.txt",
    "SG": "https://raw.githubusercontent.com/cmliu/CFcdnIP/master/SG.txt",  # 新加坡
    "DE": "https://raw.githubusercontent.com/cmliu/CFcdnIP/master/DE.txt",  # 德国
    "GB": "https://raw.githubusercontent.com/cmliu/CFcdnIP/master/GB.txt",  # 英国
    "KR": "https://raw.githubusercontent.com/cmliu/CFcdnIP/master/KR.txt",  # 韩国
    "TR": "https://raw.githubusercontent.com/cmliu/CFcdnIP/master/TR.txt",  # 土耳其
    "TW": "https://raw.githubusercontent.com/cmliu/CFcdnIP/master/TW.txt"   # 台湾
}

ip_pool = {}

for c, url in countries.items():
    try:
        r = requests.get(url)
        ips = [line.strip() for line in r.text.split("\n") if line.strip()]
        ip_pool[c] = ips
    except:
        continue

# 写入 Cloudflare KV
cf_api = f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT}/storage/kv/namespaces/{NAMESPACE}/values/ips"
headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

requests.put(cf_api, headers=headers, data=json.dumps(ip_pool))
print("IP 同步至 Cloudflare KV 成功！")
