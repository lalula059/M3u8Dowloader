from sjz42_url.Dowloader.Basedowloader import DownLoader
from sjz42_url.Dowloader.TSdowloader import ts_Downloader
from sjz42_url.configure.config import HEADERS,proxy,IS_PROXY
from sjz42_url.data_save.data_sort import  Data_Sort
import requests
import re
from sjz42_url.utils.logger import logger
from sjz42_url.utils.tools import get_m3u8_prefix,concat_m3u8_url
logger = logger
def check_AES(url):
    temp = []
    for urlin in url:
        if IS_PROXY == False:
            resp = requests.get(url=urlin,headers=HEADERS)
        else:
            resp = requests.get(url=urlin,headers=HEADERS,proxies=proxy)
        if 'AES-128' in resp.text:
            temp.append(urlin)
    url = [item for item in url if item not in temp]
    logger.info(f"再次检测对无加密输出网址信息aes网址为{temp}")
    logger.info(f"再次检测对无加密网址信息正常网址为{url}")
    return url,temp
def check_m3u8(url):
    temp_url = []
    AES_url = []
    logger.info("正在检测用户存储M3U8文件")
    for urlin in url:
        if IS_PROXY == False:
            resp = requests.get(url=urlin,headers=HEADERS)
        else:
            resp = requests.get(url=urlin,headers=HEADERS,proxies=proxy)
        logger.info(f"返回体内容{resp.status_code}")
        if 'm3u8' in resp.text:
            prefix = get_m3u8_prefix(url=urlin,value=resp.text)
            logger.info(f"前缀为{prefix}")
            concat_url = concat_m3u8_url(prefix,resp.text)
            logger.info(f"连接为{prefix}")
            temp_url.append(concat_url)
        elif 'METHOD=AES-128' in resp.text:
            AES_url.append(urlin)
        else:
            temp_url.append(urlin)
    logger.info(f"输出构造网址信息正常网址为{temp_url}")
    logger.info(f"输出构造网址信息aes网址为{AES_url}")
    temp_url,ex_aes = check_AES(temp_url)
    AES_url.append(ex_aes)
    AES_url = [item for item in AES_url if not isinstance(item, list)]
    return [M3u8_dowloader_NONE_AES(temp_url),M3u8_dowloader_WITH_AES(AES_url)]
count = 1
def gets_ts(url):
    ts_temp_list = []
    nums = 0
    global count
    if IS_PROXY == False:
        resp = requests.get(url=url,headers=HEADERS)
    else:
        resp = requests.get(url=url,headers=HEADERS,proxies=proxy)
    logger.info("正在初始化ts列表")
    for line in resp.text.split('\n'):
        if 'http' in line:
            ts_temp_list.append(line) 
        elif line.endswith('ts'):
            if 'mixed' in url:
                ts_temp_list.append(url.split('mixed.m3u8')[0]+line) 
                nums +=1
            else:
                pattern  = re.compile('(.*/)(.*?.m3u8)')
                ts = pattern.findall(url)[0][0]+line
                ts_temp_list.append(ts) 
                nums +=1
    # print(ts_temp_list)
    Data_Sort.data_sort.__setitem__(count,ts_temp_list)
    count +=1
    return ts_temp_list,nums
def get_passwd(url):
    if IS_PROXY == False:
        resp = requests.get(url=url,headers=HEADERS)
    else:
        resp = requests.get(url=url,headers=HEADERS,proxies=proxy)
    return resp.text
def get_passwd2_content(url):
    if IS_PROXY == False:
        resp = requests.get(url=url,headers=HEADERS)
    else:
        resp = requests.get(url=url,headers=HEADERS,proxies=proxy)
    return resp.content
def get_key(text,ex,url1):
    value = None
    if ex ==False:
        pattern = re.compile('http.*key')
        value = pattern.findall(text)[0]
        value = get_passwd(value)
    elif ex==True:
        if 'key' not in text:
            patter = re.compile('URI=\"(.*?)\"')
            value_1 = patter.findall(text)[0]
            print(url1)
            pre_pattern = re.compile('(http.*/)')
            prefix = pre_pattern.findall(url1)[0]
            value_1 = prefix + value_1
            value= get_passwd2_content(value_1)
            IV_num_pattern = re.compile('IV=(\w+)')
            IV_num = IV_num_pattern.findall(text)[0]
            logger.info('IvNUM值是{}'.format(IV_num[2:]))
            return [value,IV_num[2:]]
        else:
            pattern = re.compile('http.*key')
            value = pattern.findall(text)[0]
            value = get_passwd(value)
        
    return value
def gets_aes_ts(url1):
    cate = {}
    cate.setdefault('IV_NO_EXI',None)
    cate.setdefault('IV_EXI',None)
    global count
    ts_temp_list = []
    url1 = url1
    nums = 0
    if IS_PROXY == False:
        resp = requests.get(url=url1,headers=HEADERS)
    else:
        resp = requests.get(url=url1,headers=HEADERS,proxies=proxy)
    logger.info("正在初始化ts列表{}".format(url1))
    # 检测key文件和iv值
    if 'URI=' in resp.text:
        if 'IV=' not in resp.text:
            logger.info("该文件不需要偏移量加密")
            cate['IV_NO_EXI'] = get_key(text=resp.text,ex=False,url1=url1)
            cate['IV_EXI'] = None
        else:
            logger.info("该文件需要偏移量加密")
            cate['IV_EXI'] = get_key(text=resp.text,ex=True,url1=url1)
            cate['IV_NO_EXI'] = None
    # 检测所有ts的文件
    if 'http' not in resp.text:
        for line in resp.text.split('\n'):
            if line.endswith('ts'):
                if 'mixed' in url1:
                    ts_temp_list.append(url1.split('mixed.m3u8')[0]+line) 
                    nums +=1
                else:
                    pattern  = re.compile('(.*/)(.*?.m3u8)')
                    ts = pattern.findall(url1)[0][0]+line
                    ts_temp_list.append(ts) 
                    nums +=1
    else:
        for line in resp.text.split('\n'):
            if line.endswith('ts'):
                pattern  = re.compile('(.*/)(.*?.m3u8)')
                ts = line
                ts_temp_list.append(ts) 
                nums +=1
    # logger.info(f"加密的ts列表为{ts_temp_list}")
    count +=1
    Data_Sort.data_sort.__setitem__(count,ts_temp_list)
    return ts_temp_list,nums,cate
class M3u8_dowloader_fac(DownLoader):
    def get_m3u8_dowloader(self,url):
        return check_m3u8(url)



class M3u8_dowloader_NONE_AES:
    def __init__(self,url) -> None:
        self.url = url
        self.ts_suoyin={}
        self.shuliang_suoying={}
        self.url_name = {}    
    def get_ts(self):
        for url in self.url:
            self.ts_suoyin.setdefault(url,None)
            ts_li,nums = gets_ts(url)
            self.ts_suoyin.__setitem__(url,ts_li)
            self.shuliang_suoying.__setitem__(url,nums)
        return ts_Downloader(self)
class M3u8_dowloader_WITH_AES:
    def __init__(self,aes_url) -> None:
        self.aes_url = aes_url
        self.ts_suoyin={}
        self.shuliang_suoying={}
        self.url_name = {}  
        self.categories = {}

    def get_ts(self):
        for url in self.aes_url:
            ts_li,nums,categories = gets_aes_ts(url)
            self.ts_suoyin.__setitem__(url,ts_li)
            self.shuliang_suoying.__setitem__(url,nums)
            self.categories.__setitem__(url,categories)
        return ts_Downloader(self,mode = 'AES')