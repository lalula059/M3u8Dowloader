from sjz42_url.configure.config import INDEX_URL
from sjz42_url.utils.tools import init_url
from sjz42_url.Dowloader.M3U8dowloader import M3u8_dowloader_fac,M3u8_dowloader_NONE_AES,M3u8_dowloader_WITH_AES
from sjz42_url.core.req import ts_Req,ts_AES_Req
from sjz42_url.utils.logger import logger

class producer:
    def __init__(self) -> None:
        self.url_list=init_url(INDEX_URL)
        self.m3u8_innner = None
    def run(self):
        self.m3u8_innner = M3u8_dowloader_fac().get_m3u8_dowloader(self.url_list)
        for item in self.m3u8_innner:
            if isinstance(item,M3u8_dowloader_NONE_AES):
                ts_file = item.get_ts()
            if isinstance(item,M3u8_dowloader_WITH_AES):
                logger.info("检测到AES加密视频")
                ts_file_AES = item.get_ts()
        
        ts_as_dow = ts_Req(ts_file)
        ts_as_dow.run()
        ts_as_dow1 = ts_AES_Req(ts_file_AES)
        ts_as_dow1.run()
        

def start():
    producer1 = producer()
    producer1.run()