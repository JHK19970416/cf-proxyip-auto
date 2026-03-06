import requests
import json

countries = {
"US":"https://raw.githubusercontent.com/cmliu/CFcdnIP/master/US.txt",
"JP":"https://raw.githubusercontent.com/cmliu/CFcdnIP/master/JP.txt",
"KR":"https://raw.githubusercontent.com/cmliu/CFcdnIP/master/KR.txt",
"HK":"https://raw.githubusercontent.com/cmliu/CFcdnIP/master/HK.txt",
"DE":"https://raw.githubusercontent.com/cmliu/CFcdnIP/master/DE.txt",
"GB":"https://raw.githubusercontent.com/cmliu/CFcdnIP/master/GB.txt",
"TW":"https://raw.githubusercontent.com/cmliu/CFcdnIP/master/TW.txt",
"TR":"https://raw.githubusercontent.com/cmliu/CFcdnIP/master/TR.txt"
}

ip_pool = {}

for c,url in countries.items():
    r=requests.get(url)
    ips=[]
    for line in r.text.split("\n"):
        ip=line.strip()
        if ip:
            ips.append(ip)
    ip_pool[c]=ips

print(json.dumps(ip_pool))
