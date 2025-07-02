import streamlit as st
from pathlib import Path


def main():
    # 动态切换页面
    if not st.session_state.get("authenticated", False):
        # 未登录，显示登录页
        logic_path: Path = Path(__file__).parent / "app" / "logic.py"
        with open(logic_path, "r", encoding="utf-8") as f:
            code: str = f.read()
        exec(code, globals=globals())
    else:
        # 已登录，显示主应用页
        app_path: Path = Path(__file__).parent / "app" / "app.py"
        with open(app_path, "r", encoding="utf-8") as f:
            code: str = f.read()
        exec(code, globals=globals())


if __name__ == "__main__":
    main()
