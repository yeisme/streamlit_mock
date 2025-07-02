import contextlib
from typing import Any

import pandas as pd
from sqlalchemy import CursorResult, create_engine, text
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy.orm.session import Session

from ..config import settings
from ..utils import logger
from ..utils.mock_data import mock_five_stocks

# 构造数据库连接 URL，使用 pymysql 驱动
SQLALCHEMY_DATABASE_URL: str = (
    f"mysql+pymysql://{settings.db_user}:{settings.db_password}"
    f"@{settings.db_host}:{settings.db_port}/{settings.db_name}?charset=utf8mb4"
)

# 创建 SQLAlchemy 引擎，启用 pool_pre_ping 以保证连接可用
engine = create_engine(url=SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)

# 打印数据库连接信息（不打印密码）
logger.info(
    f"连接数据库: {settings.db_user}@{settings.db_host}:{settings.db_port}/{settings.db_name}"
)
# Session 工厂
SessionLocal: sessionmaker[Session] = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)


class Base(DeclarativeBase):
    pass


@contextlib.contextmanager
def get_db():
    """
    获取数据库会话的生成器，使用完毕后应关闭连接
    Usage:
        with get_db() as db:
            ...
    """
    db: Session
    try:
        db: Session = SessionLocal()
        logger.debug("数据库会话已创建")
        yield db
    except Exception as e:
        logger.error(f"获取数据库会话时发生异常: {e}")
        raise
    finally:
        if db is not None:
            try:
                db.close()
                logger.debug("数据库会话已关闭")
            except Exception as close_err:
                logger.error(f"关闭数据库会话时发生异常: {close_err}")


def init_db():
    """
    初始化数据库，自动创建所有在 Base 上注册的表
    """
    try:
        # 导入所有模型模块以便注册
        from .model import (  # noqa: F401
            StockData,
            UserData,
        )

        Base.metadata.create_all(bind=engine)
        logger.info("数据库表初始化完成")
    except Exception as e:
        logger.error(f"初始化数据库表时发生异常: {e}")
        raise


def check_connection() -> bool:
    """
    检查与数据库的连接状态，返回 True 表示连接正常
    """
    try:
        with engine.connect() as conn:
            logger.debug("数据库连接已建立，开始执行健康检查 SQL")
            result: CursorResult[Any] = conn.execute(statement=text("SELECT 1"))
            value = result.scalar()
        if value != 1:
            logger.error(f"数据库连接检查失败，返回值为 {value}")
            return False
        logger.info("数据库连接检查成功")
        return True
    except Exception as e:
        logger.error(f"数据库连接检查失败，发生异常: {e}")
        return False


def gen_df_to_sql() -> None:
    """
    将模拟数据 DataFrame 写入到数据库的 'stock_data' 表中
    """
    # 定义起始和结束日期
    end: str = pd.Timestamp.today().strftime("%Y-%m-%d")
    start: str = (pd.Timestamp.today() - pd.DateOffset(years=5)).strftime("%Y-%m-%d")
    df: pd.DataFrame = mock_five_stocks(start_date=start, end_date=end)

    try:
        df.to_sql(name="stock_data", con=engine, index=False, if_exists="replace")
        logger.info("模拟数据已成功写入到 'stock_data' 表")
    except Exception as e:
        logger.error(f"写入模拟数据到 'stock_data' 表时发生异常: {e}")
    finally:
        engine.dispose()
