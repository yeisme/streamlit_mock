import streamlit as st
from ..services import db_instance
from ..db.model import StockData
import pandas as pd
import numpy as np
from datetime import datetime

st.set_page_config(page_title="股票统计与分析", layout="wide")

st.title("股票行情与投资组合分析")

# 获取所有股票数据
with db_instance.get_db() as db:
    all_data = db.query(StockData).all()

if not all_data:
    st.info("数据库暂无股票数据。")
    st.stop()

# 转为 DataFrame
all_df = pd.DataFrame([
    {"股票代码": d.stock_code, "日期": d.date, "开盘价": d.open, "收盘价": d.close}
    for d in all_data
])
all_df["日期"] = pd.to_datetime(all_df["日期"])

# 股票代码选择
stock_codes = sorted(all_df["股票代码"].unique())
stock_code = st.selectbox("选择单只股票", stock_codes)
stock_df = all_df[all_df["股票代码"] == stock_code].sort_values("日期")

# 统计区块
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader(f"{stock_code} 收盘价走势图")
    st.line_chart(stock_df.set_index("日期")["收盘价"])

with col2:
    st.subheader(f"{stock_code} 统计指标")
    # 收益率
    stock_df = stock_df.sort_values("日期")
    stock_df["收益率"] = stock_df["收盘价"].pct_change()
    today = datetime.now().date()
    this_year = today.year
    year_start = datetime(this_year, 1, 1)
    month_start = datetime(today.year, today.month, 1)

    daily_return: float = (
        stock_df["收益率"].dropna().mean()
        if not stock_df["收益率"].dropna().empty
        else 0.0
    )
    monthly_data = stock_df[stock_df["日期"] >= month_start]["收益率"].dropna()
    monthly_return = monthly_data.mean() if not monthly_data.empty else 0.0
    ytd_data = stock_df[stock_df["日期"] >= year_start]["收益率"].dropna()
    ytd_return = ytd_data.sum() if not ytd_data.empty else 0.0
    total_return = (
        (stock_df["收盘价"].iloc[-1] / stock_df["收盘价"].iloc[0]) - 1
        if len(stock_df) > 1
        else 0.0
    )

    # 最大回撤
    roll_max = stock_df["收盘价"].cummax()
    drawdown = (stock_df["收盘价"] - roll_max) / roll_max
    max_drawdown = drawdown.min() if not drawdown.empty else 0.0
    # 夏普比率
    std = stock_df["收益率"].dropna().std()
    sharpe = (
        (daily_return / std * np.sqrt(252)) if std and not np.isnan(std) else np.nan
    )

    st.metric(
        "日均收益率", f"{daily_return:.4%}" if not np.isnan(daily_return) else "无数据"
    )
    st.metric(
        "月均收益率",
        f"{monthly_return:.4%}" if not np.isnan(monthly_return) else "无数据",
    )
    st.metric(
        "今年以来收益率", f"{ytd_return:.4%}" if not np.isnan(ytd_return) else "无数据"
    )
    st.metric(
        "历史累计收益率",
        f"{total_return:.4%}" if not np.isnan(total_return) else "无数据",
    )
    st.metric(
        "最大回撤", f"{max_drawdown:.2%}" if not np.isnan(max_drawdown) else "无数据"
    )
    st.metric("夏普比率", f"{sharpe:.2f}" if not np.isnan(sharpe) else "无数据")

st.divider()

# 投资组合分析
st.header("投资组合（5 只股票等权持有）")
portfolio_df = all_df.pivot(
    index="日期", columns="股票代码", values="收盘价"
).sort_index()
portfolio_df = portfolio_df.dropna()
portfolio_return = portfolio_df.pct_change().mean(axis=1)
portfolio_nav = (1 + portfolio_return).cumprod()

# 组合收益率
today = datetime.now().date()
this_year = today.year
year_start = datetime(this_year, 1, 1)
month_start = datetime(today.year, today.month, 1)

portfolio_daily_return = portfolio_return.mean()
portfolio_monthly_return = portfolio_return[
    portfolio_df.index >= pd.to_datetime(month_start)
].mean()
portfolio_ytd_return = portfolio_return[
    portfolio_df.index >= pd.to_datetime(year_start)
].sum()
portfolio_total_return = portfolio_nav.iloc[-1] - 1

# 组合最大回撤
roll_max = portfolio_nav.cummax()
portfolio_drawdown = (portfolio_nav - roll_max) / roll_max
portfolio_max_drawdown = portfolio_drawdown.min()
# 组合夏普比率
portfolio_sharpe = (
    portfolio_return.mean() / portfolio_return.std() * np.sqrt(252)
    if portfolio_return.std()
    else np.nan
)

col1, col2 = st.columns(2)
with col1:
    st.subheader("投资组合历史净值走势图")
    st.line_chart(portfolio_nav)
with col2:
    st.subheader("投资组合统计指标")
    st.metric("日均收益率", f"{portfolio_daily_return:.4%}")
    st.metric("月均收益率", f"{portfolio_monthly_return:.4%}")
    st.metric("今年以来收益率", f"{portfolio_ytd_return:.4%}")
    st.metric("历史累计收益率", f"{portfolio_total_return:.4%}")
    st.metric("最大回撤", f"{portfolio_max_drawdown:.2%}")
    st.metric("夏普比率", f"{portfolio_sharpe:.2f}")
