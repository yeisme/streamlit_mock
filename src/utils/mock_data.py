"""
mock_data.py

数据模拟模块，用于生成 5 只模拟股票行情数据（5 年历史，包含股票代码、日期、开盘价、收盘价）
"""

import pandas as pd
import numpy as np
from typing import List


def generate_stock_data(
    stock_codes: List[str], start_date: str, end_date: str
) -> pd.DataFrame:
    """
    生成股票历史行情数据

    参数:
    - stock_codes: list of str, 股票代码列表
    - start_date: str, 起始日期，格式 YYYY-MM-DD
    - end_date: str, 结束日期，格式 YYYY-MM-DD

    返回:
    - DataFrame, 包含 columns: ['stock_code', 'date', 'open', 'close']
    """
    # 生成交易日序列（仅包含工作日）
    dates: pd.DatetimeIndex = pd.date_range(start=start_date, end=end_date, freq="B")
    all_data: List[dict] = []

    for code in stock_codes:
        # 随机游走模拟价格基础
        base_price = 100 + np.cumsum(np.random.normal(0, 1, len(dates)))
        # 模拟开盘价和收盘价
        open_prices = base_price + np.random.normal(0, 1, len(dates))
        close_prices = base_price + np.random.normal(0, 1, len(dates))

        for date, op, cp in zip(dates, open_prices, close_prices):
            all_data.append(
                {
                    "stock_code": code,
                    "date": date.date(),
                    "open": round(op, 2),
                    "close": round(cp, 2),
                }
            )

    df = pd.DataFrame(all_data)
    return df


def mock_five_stocks(start_date: str, end_date: str) -> pd.DataFrame:
    """
    针对 5 只股票生成模拟数据，默认股票代码 STOCK1 ~ STOCK5
    """
    codes = [f"STOCK{i + 1}" for i in range(5)]
    return generate_stock_data(codes, start_date, end_date)


if __name__ == "__main__":
    # 示例用法：生成最近 5 年 (近似) 的模拟数据
    end = pd.Timestamp.today().strftime("%Y-%m-%d")
    start = (pd.Timestamp.today() - pd.DateOffset(years=5)).strftime("%Y-%m-%d")
    df = mock_five_stocks(start, end)
    print(df.head())
