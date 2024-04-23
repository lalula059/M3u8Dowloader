import aiofiles
import os
import re
from sjz42_url.utils.logger import logger

async def datas(content,url,count):
    logger.info(f'正在写入{url}')
    pa = os.path.abspath(__file__).split('\sjz42_url')[0]
    if not os.path.isdir(f'E:\\video\\{(count)}'):
        os.makedirs(f'E:\\video\\{(count)}')
    file = f'E:\\video\\{(count)}\\'
    pattern = re.compile('(http.*?)/(\w+\.ts)')
    pa = pattern.findall(url)[0][1]
    file = file+pa
    logger.info(f'正在写入{file}')
    with open(file=file,mode='wb') as file:
        file.write(content)

async def check_Data(name,count):
    if not os.path.exists(f'E:\\video\\{(count)}'):
        return True
    if  os.path.isdir(f'E:\\video\\{(count)}'):
        file = f'E:\\video\\{(count)}\\'
        if name in os.listdir(file):
            return False
        else:
            return True