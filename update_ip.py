import os
import requests
import json

# 配置从 GitHub Secrets 获取变量
ACCOUNT = os.getenv('CF_ACCOUNT_ID')
NAMESPACE = os.getenv('CF_NAMESPACE')
TOKEN = os.getenv('CF_API_TOKEN')

# 定义抓取源
countries = {
    "US": "https://raw.githubusercontent.com/cmliu/CFcdnIP/master/US.txt",
    "JP": "https://raw.githubusercontent.com/cmliu/CFcdnIP/master/JP.txt",
    "HK": "https://raw.githubusercontent.com/cmliu/CFcdnIP/master/HK.txt",
    "SG": "https://raw.githubusercontent.com/cmliu/CFcdnIP/master/SG.txt",
    "DE": "https://raw.githubusercontent.com/cmliu/CFcdnIP/master/DE.txt",
    "GB": "https://raw.githubusercontent.com/cmliu/CFcdnIP/master/GB.txt",
    "KR": "https://raw.githubusercontent.com/cmliu/CFcdnIP/master/KR.txt",
    "TR": "https://raw.githubusercontent.com/cmliu/CFcdnIP/master/TR.txt",
    "TW": "https://raw.githubusercontent.com/cmliu/CFcdnIP/master/TW.txt"
}

ip_pool = {}

for c, url in countries.items():
    try:
        r = requests.get(url, timeout=10)
        # 核心修复：只有状态码为 200 且内容不包含 "Not Found" 时才处理
        if r.status_code == 200 and "Not Found" not in r.text:
            # 过滤每一行，确保只存入包含 3 个点的 IP 地址
            ips = [line.strip() for line in r.text.split("\n") 
                   if line.strip() and line.count('.') >= 3]
            if ips:
                ip_pool[c] = ips
                print(f"✅ 成功获取 {c} 节点")
        else:
            print(f"❌ 跳过 {c}：源地址返回 404 或内容异常")
    except Exception as e:
        print(f"无法连接 {c}: {e}")

# 只有抓到有效 IP 才执行写入，防止把 KV 覆盖成 404
if ip_pool:
    try:
        cf_api = f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT}/storage/kv/namespaces/{NAMESPACE}/values/ips"
        headers = {
            "Authorization": f"Bearer {TOKEN}",
            "Content-Type": "application/json"
        }
        response = requests.put(cf_api, headers=headers, data=json.dumps(ip_pool))
        if response.status_code == 200:
            print("🚀 IP 数据已成功同步至 Cloudflare！")
        else:
            print(f"写入失败，错误码: {response.status_code}")
    except Exception as e:
        print(f"推送出错: {e}")
else:
    print("终止操作：未抓取到任何有效 IP 数据。")
