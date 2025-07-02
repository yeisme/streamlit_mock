import os
import pytest
from src.config.config import Settings
from pydantic_settings import SettingsConfigDict


def clear_env() -> None:
    # 清除所有相关的环境变量，确保测试环境干净
    env_vars = ["DB_USER", "DB_PASSWORD", "DB_HOST", "DB_PORT", "DB_NAME", "LOG_LEVEL"]
    for var in env_vars:
        if var in os.environ:
            del os.environ[var]


@pytest.fixture
def set_env(monkeypatch):
    monkeypatch.setenv("DB_USER", "test_user")
    monkeypatch.setenv("DB_PASSWORD", "test_pass")
    monkeypatch.setenv("DB_HOST", "127.0.0.1")
    monkeypatch.setenv("DB_PORT", "3307")
    monkeypatch.setenv("DB_NAME", "test_db")
    monkeypatch.setenv("LOG_LEVEL", "INFO")
    yield
    # 环境变量自动恢复


def test_settings_default():
    clear_env()

    settings = Settings()  # type: ignore
    assert settings.db_host == "localhost"
    assert settings.db_port == 3306
    assert settings.db_user == "streamlit_user"
    assert settings.db_password == "streamlit_password"
    assert settings.db_name == "streamlit_db"


def test_settings_from_envfile():
    clear_env()

    # 测试从 .env 文件加载配置
    class test_settings(Settings):
        model_config = SettingsConfigDict(env_file=".env.example")

    settings = test_settings()  # type: ignore
    assert settings.db_user == "streamlit_user"
    assert settings.db_password == "streamlit_password"
    assert settings.db_host == "localhost"
    assert settings.db_port == 3306
    assert settings.db_name == "streamlit_db"
    assert settings.log_level == "DEBUG"
