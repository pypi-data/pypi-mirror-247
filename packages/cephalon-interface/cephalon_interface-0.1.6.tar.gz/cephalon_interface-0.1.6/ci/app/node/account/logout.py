import time
import streamlit as st
from ci.core import cephalon


def render_not_logged_in():
    st.error("You are not logged in to an account.")


def render_logout_check():
    # todo: move to docs
    # with st.expander("Log out details"):
    #     st.write(
    #         """
    #         What logging out does do:

    #         - Removes the locally cached JSON web token.

    #         What logging out does *not* do:

    #         - Delete your account.
    #         - Revoke tokens.
    #         - Uninstall this software.
    #         - Remove local cached package data, examples include (but are not limited to):
    #             - Datasets
    #             - Models
    #             - Configuration Files

    #         If you want to do any of the actions in the latter list, please refer to the docs.
    #         """
    #     )
    st.write("Are you sure you want to log out?")
    if st.button("Yes"):
        cephalon.account.logout()
        with st.spinner("Refreshing in 1 second..."):
            time.sleep(1)
            st.rerun()


def render():
    st.markdown("# Log out of your account.")
    if not cephalon.account.initialized:
        render_not_logged_in()
    else:
        render_logout_check()
