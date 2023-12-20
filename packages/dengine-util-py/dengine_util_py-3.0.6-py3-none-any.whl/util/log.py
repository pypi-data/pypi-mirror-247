import logging
import re
from logging.handlers import TimedRotatingFileHandler

from util.path import get_project_dir

# 设置日志文件的最大大小（可选）
max_file = 1024 * 1024 * 1024 * 1
# 最大备份小时
backup_count = 24 * 30

ext_match = r"^\d{10}$"
suffix = '%Y%m%d%H'

# hander = TimedRotatingFileHandler(filename=get_project_dir() + "/log/all.log", when="H", interval=1,
#                                   backupCount=backup_count)
# hander.suffix = suffix
# hander.extMatch = re.compile(ext_match, re.ASCII)

hander = TimedRotatingFileHandler(filename=get_project_dir() + "/log/public.log", when="H", interval=1,
                                            backupCount=backup_count, utc=True)
hander.suffix = suffix
hander.extMatch = re.compile(ext_match, re.ASCII)

# 配置日志

# logging.basicConfig(
#     level=logging.INFO,
#     format="[%(levelname)s][%(asctime)s.%(msecs)d][%(filename)s:%(lineno)d] _triton-inference-server||%(message)s",
#     handlers=[
#         hander
#         # logging.StreamHandler() 输出日志到标准输出
#     ],
#     datefmt='%Y-%m-%dT%H:%M:%S',
# )
#
# # 创建日志记录器
# logger = logging.getLogger(__name__)

# 配置Public日志

logging.basicConfig(
    level=logging.INFO,
    format="%(logTag)s||timestamp=%(asctime)s||%(message)s",
    handlers=[
        hander
        # logging.StreamHandler() 输出日志到标准输出
    ],
    datefmt='%Y-%m-%d %H:%M:%S',
)

# 创建Public日志记录器
# publiclogger = logging.getLogger("publicLog")
logger = logging.getLogger(__name__)
