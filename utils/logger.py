import logging
def get_logger():
    logger = logging.getLogger(__name__)
    """如果调用basicconfig会默认创建一个stranmehandler所以说会输出两次，且basicconfig一次是根节点日志格式等设置"""
    formatter = logging.Formatter('%(levelname)s等级||||%(asctime)s============信息内容:%(message)s')
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)  # 设置日志级别
    return logger

logger = get_logger()