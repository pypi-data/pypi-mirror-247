import json
import streamlit as st

from ci import var
from ci.core import cephalon
from ci.utility import streamlit
import webbrowser
from PIL import Image

# from ci.app.node.account import login

from ci.app.node import loki, account

"""

- account
    - login
- config/settings
    - plugins
- system
    - agent (web)
- daemon (local)
- utility
- plugin
- ? local
    - logs
    - cache control
    - datasets

"""

CFG_PAGE_ICON = "🧠"
CFG_LAYOUT = "wide"
CFG_INITIAL_SIDEBAR_STATE = "expanded"


OBJ_LOGO: Image = Image.open(var.PATH_LOGO)

# todo: replace with pyeio
with open(var.PATH_THEME) as theme_file:
    OBJ_THEME: str = theme_file.read()
theme_file.close()


st.set_page_config(
    page_title=var.PACKAGE_NAME_TITLE,
    page_icon=CFG_PAGE_ICON,
    layout=CFG_LAYOUT,
    initial_sidebar_state=CFG_INITIAL_SIDEBAR_STATE,
)

# with open(env.PATH_GLOBE) as file:
#     animation = json.load(file)
# file.close()


streamlit.inject_css(OBJ_THEME)


# if "node" not in st.session_state.keys():
#     st.session_state["node"] = None


# todo: sort these with tags
# account: login, recover, request, settings
# logs: local, remote
# tools: pipelines, agent, experiment, monitor
global_nodes: dict = {
    # "test": loki.render,
    # "=": config
    # "/": micro-tool/component,
    # "?": logs/monitor,
    # ">": quick actions
    # ? docs
    # external webpages
    # ":": agent/experiment deployment and monitoring
    # "tool.pipelines": pipelines,
    # "tool.account": "asdf",
    # "settings.account": "asdf",
    # "signal.moirai": "asdf",
    # "experiment/a3"
}

# * you can still access these pages if you are not authenticated
# * by turning on the demo mode in the app, or using the CLI,
# * but they won't be too useful unless you register for an account
# * as they depend on various cloud resources

nonauthenticated_nodes = {
    "account/login": account.login.render,
    "account/register": account.register.render,
}

authenticated_nodes = {
    "account/logout": account.logout.render,
    # "loki": loki.render,
}

if cephalon.account.authenticated:
    global_nodes.update(authenticated_nodes)
else:
    global_nodes.update(nonauthenticated_nodes)

# todo: add ability for user to filter out nodes they don't want to see in the quick nav

options = sorted(list(global_nodes.keys()))


def home():
    st.markdown(f"# Cephalon Interface :blue[{var.PACKAGE_VERSION}]")
    if not cephalon.account.initialized:
        st.markdown(f"#### Account: :orange[None [Standalone Mode]]")
    else:
        # wierd fix for streamlit autolinking
        informal_username, domain = cephalon.account.email.split("@")
        user = f":blue[{informal_username}:blue[@]:blue[{domain}]]"
        st.markdown(f"#### Account: {user}")
        st.markdown(f"#### Status: :green[Initialized]")
        if cephalon.account.authenticated:
            st.markdown(f"#### Authenticated: :green[True]")
        else:
            st.markdown(f"#### Authenticated: :red[False]")
            st.error(
                "You likely need to confirm your account, or login again to refresh your session."
            )


def main() -> None:
    # current_node = streamlit.get_node()
    # if current_node is not None:
    #     selection_index = options.index(current_node)
    with st.sidebar:
        selected_node = st.selectbox(
            label="selected_node",
            options=options,
            index=None,
            placeholder="Go to...",
            key="selected_node",
            label_visibility="hidden",
        )
        if selected_node is not None:
            streamlit.set_node(selected_node)
        b1, b2 = st.columns([1, 1])
        with b1:
            home_button = st.button("Home", use_container_width=True)
            if home_button:
                streamlit.reset_node()
        with b2:
            docs_button = st.button("Docs", use_container_width=True, type="primary")
            if docs_button:
                webbrowser.open_new_tab("https://cephalon.systems")

    current_node = streamlit.get_node()

    if current_node is not None:
        if current_node in global_nodes.keys():
            global_nodes[current_node]()
        else:
            streamlit.reset_node()
            home()
    else:
        home()
    streamlit.inject_hotkey_jump_to_selectbox(
        selectbox_label="selected_node", character="k", special=["meta"]
    )


if __name__ == "__main__":
    main()
