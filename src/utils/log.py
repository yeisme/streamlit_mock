import sys
from loguru import logger
from ..config import settings


def configure_logger(level: str = "DEBUG"):
    """初始化并配置 loguru 日志，支持动态设置级别"""
    # 移除默认处理器
    logger.remove()
    # 添加新处理器，JSON 格式输出，启用异常追踪和诊断
    logger.add(sink=sys.stdout, level=level)
    return logger


configure_logger(level=settings.log_level)
