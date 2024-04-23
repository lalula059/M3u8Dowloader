"""存储数据库还有URL等相关信息"""
import random
import requests

INDEX_URL = ['https://leshiyuncdn.36s.top/20230717/7JgUZoR2/hls/index.m3u8']
HEADERS = { 'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
            'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            'Referer':'https://jx.ijujitv.cc/'}
proxy = {
    'http':'http://127.0.0.1:7890',
    'https':'http://127.0.0.1:7890'
}
SEM_NUM = 5
IS_PROXY=False