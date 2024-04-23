import asyncio
import re
import aiohttp
import aiofiles
from abc import  ABC
from sjz42_url.utils.logger import logger
from sjz42_url.configure.config import HEADERS,proxy,IS_PROXY,SEM_NUM
from sjz42_url.data_save.ds import datas,check_Data
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
logger = logger


count = 0
class Req(ABC):
    def __init__(self,cl_ts) -> None:
        self.loop = asyncio.get_event_loop()
        self.cl_ts =cl_ts
    async def set_tasks(self):
        pass
    async def get_in(self):
        pass
    async def req_content(self,url,count,sem,session):
        try:
            async with sem:
                if IS_PROXY == False:
                    await self.req_main(url, count, session)
                else:
                    await self.req_main_proxy(url, count, session)
        except aiohttp.ClientConnectorError as e:
            logger.error(f"客户端连接出错{e}") 
        except aiohttp.ServerConnectionError as e:
            logger.error(f"服务器连接出错{e}") 
        except Exception as e:
            logger.error(f"未知出错{e}网址为{url}") 

    async def req_main_proxy(self, url, count, session):
        async with session.get(url=url,headers=HEADERS,proxy=proxy['https']) as resp:
            logger.info(f"正在抓取{url}")
            result = await aiohttp.StreamReader.read(resp.content)
            await datas(result,url,count)

    async def req_main(self, url, count, session):
        async with session.get(url=url,headers=HEADERS) as resp:
            logger.info(f"正在抓取{url}")
            result = await aiohttp.StreamReader.read(resp.content)
            await datas(result,url,count)
            
    def run(self):
        self.loop.run_until_complete(self.get_in())
    
class ts_Req(Req):
    def __init__(self, cl_ts) -> None:
        super().__init__(cl_ts)
        self.sem = None
    async def check_item(self,url,count):
        pattern = re.compile('^http.*/(\w+.ts)')
        text = pattern.findall(url)[0]
        no_download = await check_Data(text,count)
        if no_download:
            return True
    async def set_tasks(self):
        tasks = []
        global count
        for keys in self.cl_ts.m3u8_save_ts_noaes.shuliang_suoying:
            count +=1
            async with aiohttp.ClientSession() as session:
                for item in self.cl_ts.m3u8_save_ts_noaes.ts_suoyin[keys]:
                    if await self.check_item(item,count):
                        task = asyncio.create_task(self.req_content(item,count,self.sem,session))
                        tasks.append(task)
                await asyncio.gather(*tasks)
    async def get_in(self):
        self.sem = asyncio.Semaphore(20)
        await self.set_tasks()


class ts_AES_Req(Req):
    def __init__(self, cl_ts) -> None:
        super().__init__(cl_ts)
        self.sem = None
    async def check_item(self,url,count):
        pattern = re.compile('^http.*/(\w+.ts)')
        text = pattern.findall(url)[0]
        no_download = await check_Data(text,count)
        logger.info('检测是否存在相同文件{}'.format(text))
        if no_download:
            logger.info('不存在相同文件')
            return True
    
    async def req_main_proxy(self, url, count, session,key):
        async with session.get(url=url,headers=HEADERS,proxy=proxy['https']) as resp:
            res = await resp.content.read()
            logger.info(f"正在抓取{url}")
            try:
                if self.cl_ts.m3u8_save_ts_AES.categories[key]['IV_NO_EXI'] is not None :
                    keys = self.cl_ts.m3u8_save_ts_AES.categories[key]['IV_NO_EXI'].encode('utf-8')
                    aes = AES.new(keys,AES.MODE_CBC, IV=b'\x00' * 16)
                    result = aes.decrypt(res)
                elif self.cl_ts.m3u8_save_ts_AES.categories[key]['IV_EXI'] is not None:
                    keys = self.cl_ts.m3u8_save_ts_AES.categories[key]['IV_EXI'][0]
                    IV_num =self.cl_ts.m3u8_save_ts_AES.categories[key]['IV_EXI'][1]
                    aes = AES.new(keys,AES.MODE_CBC, IV= bytes.fromhex(IV_num))
                    result = aes.decrypt(res)
                await datas(result,url,count)
            except Exception as e:
                logger.error("需要填充文本")
                logger.info("正在填充文本")
                if 'padded' in e.args:
                    res1 = pad(res,16)
                    result = aes.decrypt(res1)
                    await datas(result,url,count)
    async def req_main(self, url, count, session,key):
        async with session.get(url=url,headers=HEADERS) as resp:
            res = await resp.content.read()
            logger.info(f"正在抓取{url}")
            try:
                if self.cl_ts.m3u8_save_ts_AES.categories[key]['IV_NO_EXI'] is not None:
                    keys = self.cl_ts.m3u8_save_ts_AES.categories[key]['IV_NO_EXI'].encode('utf-8')
                    aes = AES.new(keys ,AES.MODE_CBC, IV=b'\x00' * 16)
                    result = aes.decrypt(res)
                elif self.cl_ts.m3u8_save_ts_AES.categories[key]['IV_EXI'] is not None:
                    keys = self.cl_ts.m3u8_save_ts_AES.categories[key]['IV_EXI'][0]
                    IV_num =(self.cl_ts.m3u8_save_ts_AES.categories[key]['IV_EXI'][1][2:])
                    aes = AES.new(keys,AES.MODE_CBC, IV= bytes.fromhex(IV_num))
                    result = aes.decrypt(res)
                await datas(result,url,count)
            except Exception as e:
                logger.error("需要填充文本")
                logger.info("正在填充文本")
                if 'padded' in e.args:
                    res1 = pad(res,16)
                    result = aes.decrypt(res1)
                    await datas(result,url,count)
    async def req_content(self,url,count,sem,session,keys):
        try:
            async with sem:
                if IS_PROXY == False:
                    await self.req_main(url, count, session,keys)
                else:
                    await self.req_main_proxy(url, count, session,keys)
        except aiohttp.ClientConnectorError as e:
            logger.error(f"客户端连接出错{e}") 
        except aiohttp.ServerConnectionError as e:
            logger.error(f"服务器连接出错{e}") 
        except Exception as e:
            logger.error(f"未知出错{e}网址为{url}") 
            
    async def set_tasks(self):
        tasks = []
        global count
        for keys in self.cl_ts.m3u8_save_ts_AES.shuliang_suoying:
            count +=1
            async with aiohttp.ClientSession() as session:
                for item in self.cl_ts.m3u8_save_ts_AES.ts_suoyin[keys]:
                    # pass
                    if await self.check_item(item,count):
                        logger.info("检测完毕不存在{}".format(item))
                        task = asyncio.create_task(self.req_content(item,count,self.sem,session,keys))
                        tasks.append(task)
                await asyncio.gather(*tasks)
    async def get_in(self):
        self.sem = asyncio.Semaphore(SEM_NUM)
        await self.set_tasks()