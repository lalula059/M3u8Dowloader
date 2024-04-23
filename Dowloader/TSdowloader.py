from ctypes import Union



class ts_Downloader:
    def __init__(self,m3u8_dowloader,mode = None) -> None:
        if mode =='AES':
            self.m3u8_save_ts_AES = m3u8_dowloader
            self.mode = mode
        else: 
            self.m3u8_save_ts_noaes = m3u8_dowloader
            self.mode = mode