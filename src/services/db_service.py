class DBServices:
    """
    数据库服务类，提供数据库相关操作
    """

    def __init__(self):
        from src.db.base import init_db, check_connection, get_db

        self.init_db = init_db
        self.check_connection = check_connection
        self.get_db = get_db

    def initialize(self):
        """
        初始化数据库
        """
        self.init_db()

    def is_connected(self) -> bool:
        """
        检查数据库连接状态
        """
        return self.check_connection()

    def get_session(self):
        """
        获取数据库会话
        """
        return self.get_db()


# 全局数据库服务实例
db_instance = DBServices()
