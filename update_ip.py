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

# 修改后的抓取循环
for c, url in countries.items():
    try:
        # 设置 10 秒超时，防止某个链接卡死导致整个脚本失败
        r = requests.get(url, timeout=10)
        
        # 只有当网页状态码为 200 (正常) 且内容不包含 "Not Found" 时才处理
        if r.status_code == 200 and "Not Found" not in r.text:
            # 过滤掉非 IP 字符，确保每一行至少包含三个点（简单的 IPv4 校验）
            ips = [line.strip() for line in r.text.split("\n") 
                   if line.strip() and line.count('.') >= 3]
            
            if ips:
                ip_pool[c] = ips
                print(f"✅ 成功获取 {c} 节点的优选 IP")
            else:
                print(f"⚠️ {c} 节点抓取成功但内容为空，已跳过")
        else:
            print(f"❌ 抓取 {c} 失败，状态码: {r.status_code} (可能是源链接失效)")
            
    except Exception as e:
        print(f"无法连接到 {c} 的源地址: {e}")

# 只有在抓取到有效 IP 的情况下才更新 KV，防止误删旧数据
if ip_pool:
    try:
        response = requests.put(cf_api, headers=headers, data=json.dumps(ip_pool))
        if response.status_code == 200:
            print("🚀 所有 IP 已成功同步至 Cloudflare KV！")
        else:
            print(f"写入 KV 失败，API 返回状态码: {response.status_code}")
    except Exception as e:
        print(f"推送至 Cloudflare 过程中出错: {e}")
else:
    print("终止操作：未抓取到任何有效 IP，不执行数据库更新以保护旧数据。")")
