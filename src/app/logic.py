import streamlit as st
from ..services import db_instance
from ..db.model import UserData
import hashlib


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


if not st.session_state.get("authenticated", False):
    st.title("登录")
    username = st.text_input("用户名")
    password = st.text_input("密码", type="password")
    login_btn = st.button("登录")
    register_btn = st.button("注册")
    login_msg = ""
    if login_btn:
        with db_instance.get_db() as db:
            user = db.query(UserData).filter_by(username=username).first()
            if user is not None and getattr(user, "password", None) == hash_password(
                password
            ):
                st.session_state["authenticated"] = True
                st.session_state["username"] = username
                st.success("登录成功！")
                st.rerun()
            else:
                st.error("用户名或密码错误")
    if register_btn:
        with db_instance.get_db() as db:
            user = db.query(UserData).filter_by(username=username).first()
            if user:
                st.warning("用户名已存在")
            else:
                new_user = UserData(username=username, password=hash_password(password))
                db.add(new_user)
                db.commit()
                st.success("注册成功，请登录")
else:
    st.title("欢迎登录！")
    st.success("登录成功，点击下方按钮进入主应用页面。")
    if st.button("进入主应用页面"):
        st.switch_page("app.py")
