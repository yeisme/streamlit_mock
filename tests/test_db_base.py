from src.db.base import init_db, check_connection, get_db
from src.db.model import StockData, UserData
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
        result = db.query(StockData).all()
        assert len(result) == len(df)

        # 验证数据正确性
        for _, row in df.iterrows():
            assert any(
                r.stock_code == row["stock_code"] and r.date == row["date"]
                for r in result
            )


def test_crud_user_data():
    init_db()
    with get_db() as db:
        # 清空表数据
        db.query(UserData).delete()
        db.commit()

        # 插入用户
        user1 = UserData(username="testuser1", password="pass1")
        user2 = UserData(username="testuser2", password="pass2")
        db.add(user1)
        db.add(user2)
        db.commit()

        # 查询用户
        users = db.query(UserData).all()
        assert len(users) == 2
        assert any(u.username == "testuser1" for u in users)
        assert any(u.username == "testuser2" for u in users)

        # 更新用户密码
        user1_db = db.query(UserData).filter_by(username="testuser1").first()
        setattr(user1_db, "password", "newpass1")
        db.commit()
        user1_db = db.query(UserData).filter_by(username="testuser1").first()
        assert getattr(user1_db, "password") == "newpass1"

        # 删除用户
        db.query(UserData).filter_by(username="testuser1").delete()
        db.commit()
        users = db.query(UserData).all()
        assert len(users) == 1
        assert getattr(users[0], "username") == "testuser2"

        # 清空表
        db.query(UserData).delete()
        db.commit()
        users = db.query(UserData).all()
        assert len(users) == 0
