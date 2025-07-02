from sqlalchemy import Column, String, Float, Date
from .base import Base


class StockData(Base):
    """
    股票数据模型
    """

    __tablename__ = "stock_data"

    stock_code = Column(String(10), primary_key=True, comment="股票代码")
    date = Column(Date, primary_key=True, comment="交易日期")
    open = Column(Float, comment="开盘价")
    close = Column(Float, comment="收盘价")

    def __repr__(self) -> str:
        return f"<StockData(stock_code={self.stock_code}, date={self.date}, open={self.open}, close={self.close})>"


class UserData(Base):
    """
    用户数据模型
    """

    __tablename__ = "user_data"

    username = Column(String(50), primary_key=True, comment="用户名")
    password = Column(String(100), comment="密码")

    def __repr__(self) -> str:
        return f"<UserData(username={self.username})>"
