import os
import sys
"""加载环境配置"""
sys.path.append(os.path.abspath(__file__.split('\sjz42_url')[0]))
from utils.logger import logger
from core.proceduer import start
from data_save.merge import  merge
"""加载日志模块"""
logging = logger
import time
timex = time.time()
start()
merge()
t = time.time()-timex
logger.info(f"{'*'*50}任务完成时间为{t}{'*'*50}")
