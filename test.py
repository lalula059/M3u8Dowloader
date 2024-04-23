import requests
url = 'https://tscdn.hyz1.top/20230718/tpMaglPK/hls/0UGZRwhe.ts'
HEADERS = { 'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
            'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            }
resp = requests.get(url=url,headers=HEADERS)
print(resp.content)
with open('test.ts','wb') as f:
    f.write(resp.content)