import re
from sjz42_url.utils.logger import logger

logger = logger
def init_url(url):
    if isinstance(url,str):
        return [url]
    elif isinstance(url,list):
        return url

def get_m3u8_prefix(url,value):
    pattern = re.compile('(http.*?)/(\w+).m3u8')
    value = pattern.findall(url)[0]
    logger.info(f"提取M3U8前缀-------------{value}")
    return value
    


def concat_m3u8_url(pre,text):
    pattern = re.compile('http.*?//.*?/(\d+)/(\w+)')
    F_match = pattern.findall(pre)[0][1]
    logger.info(f"检测匹配字符串中{F_match}")
    if F_match in text:
        lasts_pa = re.compile(f'.*?{F_match}/(.*?index.m3u8)')
        logger.info(f"输出构造断句为{lasts_pa}")
        last_text = lasts_pa.findall(text)[0]
    else:
        lasts_pa = re.compile('(.*?m3u8)')
        last_text = lasts_pa.findall(text)[0]
    logger.info(f"断开后续字符串中{last_text}")
    return pre+'/'+last_text
    