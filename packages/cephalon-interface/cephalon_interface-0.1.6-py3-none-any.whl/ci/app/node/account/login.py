import time
import streamlit as st
from ci.core import cephalon


def render_already_logged_in():
    informal_username, domain = cephalon.account.email.split("@")
    user = f":blue[{informal_username}:blue[@]:blue[{domain}]]"
    st.success(f"You are currently logged in as: {user}")


def render_login_form():
    email = st.text_input("Email", placeholder="example@domain.com")
    password = st.text_input("Password", type="password", placeholder="•" * 16)
    if st.button("Login"):
        result = cephalon.account.login(email=email, password=password)
        if result.is_ok():
            st.success("You are now logged in.")
            with st.spinner("Refreshing in 1 second..."):
                time.sleep(1)
                st.rerun()

        else:
            st.error(result.message)


def render():
    st.markdown("# Log in to your account.")
    if cephalon.account.authenticated:
        render_already_logged_in()
    else:
        render_login_form()
