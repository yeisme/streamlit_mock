from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    数据库配置类，使用 Pydantic 进行环境变量加载和验证
    通过 .env 文件加载配置，支持 DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME 等变量
    使用时请确保 .env 文件存在并包含正确的数据库连接信息
    """

    db_user: str
    db_password: str
    db_host: str = "localhost"
    db_port: int = 3306
    db_name: str

    log_level: str = "DEBUG"

    class Config:
        env_file: str = ".env"


settings = Settings()  # type: ignore
