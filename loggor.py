import logging
import sys

# 加入日志
#获取logger实例
logger = logging.getLogger("basekd")
# 指定输出格式
formatter = logging.Formatter('%(asctime)s\
              %(levelname)-8s:%(message)s')
# 文件日志
file_handler = logging.FileHandler("basekd.log")
file_handler.setFormatter(formatter)
# 控制台日志
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(formatter)

# 为logge添加具体的日志处理器
logger.addHandler(file_handler)
logger.addHandler(console_handler)

logger.setLevel(logging.INFO)

def info(string=None):
    if string:
        logger.info(string)

def error(string=None):
    if string:
        logger.error(string)

# logger.error("failed: ")

# logger.info('info')
