from typing import List
from src.db.base import init_db, check_connection, get_db
from src.db.model import StockData
from src.utils.mock_data import mock_five_stocks


def test_db_connection():
    assert check_connection() is True


def test_init_db():
    init_db()


def test_get_db():
    with get_db() as db:
        assert db is not None
        assert db.connection().closed == 0


def test_crud_stock_data():
    # 生成模拟数据
    df = mock_five_stocks("2018-01-01", "2023-01-01")

    # 初始化数据库
    init_db()

    with get_db() as db:
        # 清空表数据
        db.query(StockData).delete()
        db.commit()

        # 插入数据
        for _, row in df.iterrows():
            stock_data = StockData(
                stock_code=row["stock_code"],
                date=row["date"],
                open=row["open"],
                close=row["close"],
            )
            db.add(instance=stock_data)
        db.commit()

        # 查询数据
        result: List[StockData] = db.query(StockData).all()
        assert len(result) == len(df)

        # 验证数据正确性
        for _, row in df.iterrows():
            assert any(
                r.stock_code == row["stock_code"] and r.date == row["date"]
                for r in result
            )
