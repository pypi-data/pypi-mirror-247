import streamlit as st
from ci.core import cephalon


def home():
    st.write("# Account")


def render_authenticated():
    (about_tab,) = st.tabs(["About"])
    with about_tab:
        home()


def render_unauthenticated():
    (about_tab,) = st.tabs(["About"])
    with about_tab:
        st.error("You are not currently logged in. ")
        st.write(
            """
                Some features of this tool depend on the API, and as such may require an account.
                Currently, there is no way to register for an account (primarily due to cost concerns), but an access request form will
                be available soon. If you already have an account, or just received a confirmation email, you can login below. If you would
                like to test the functionality of this tool, you can also enabled the "demo mode" in the CLI, or local configuration page.
                """
        )

        # todo: future
        st.write("To create an account, run the following command in your terminal:")
        st.code("ci account register", language="bash")
        with st.expander("Login via CLI"):
            st.write(
                """
                To login to an account, run the following command in your terminal.
                Once you have successfully logged in, you can return to this page and click the refresh button below.
                Make sure to use this command in a new terminal window, that is not running the Streamlit app.
                """
            )
            st.code("ci account login", language="bash")
            refresh_button = st.button("Refresh", use_container_width=True)
            if refresh_button:
                st.rerun()

        with st.expander("Reset password via CLI"):
            st.write(
                """
                Alternatively, if you need to reset your password, run the following command in your terminal.
                You should get a password reset email shortly after running this command.
                Make sure to use this command in a new terminal window, that is not running the Streamlit app.
                """
            )
            st.code("ci account recover", language="bash")

        with st.expander("Login with Python"):
            st.write(
                """
                    Note that your password is not stored locally, only an ID token with an expiration period of 30 days.
                    To ensure your password is secure, you should not actually pass your password or email as plaintext.
                    Instead, consider using something like the [1password-client](https://github.com/wandera/1password-client)
                    to programatically retrieve your password from your password manager (this only works for 1password).
                    """
            )
            st.code(
                """
                # import the system module
                from ci import system

                # login to your account
                system.account.login(email: str = "<your email>", password: str = "<your password>")
                """,
                language="python",
            )

        with st.expander("Reset password with Python"):
            st.write(
                """
                To reset your password you can use the following code snippet.
                If you don't provide your email, then it will use whatever email is
                currently locally cached (if any).
                """
            )
            st.code(
                """
                # import the system module
                from ci import system
                from typing import Optional # optional, only used for type hinting

                # request a password reset
                system.account.recover(email: Optional[str] = "<your email>")
                """
            )


def render():
    if not cephalon.account.authenticated:
        render_unauthenticated()
    else:
        render_authenticated()
