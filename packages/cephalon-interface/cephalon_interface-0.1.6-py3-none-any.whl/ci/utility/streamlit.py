import sys
import toml
import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path
from typing import Union


def fix_email_prompt():
    # * this is a fix for the streamlit prompt for your email to subscribe to their newsletter
    streamlit_config_dir: Path = Path.home() / ".streamlit"
    streamlit_credentials_file: Path = streamlit_config_dir / "credentials.toml"
    if not streamlit_credentials_file.exists():
        streamlit_config_dir.mkdir(exist_ok=True)
        with open(streamlit_credentials_file, "w") as scf:
            toml.dump({"general": {"email": ""}}, scf)
        scf.close()


def get_url_query_parameters() -> dict[str, str]:
    query_params = st.experimental_get_query_params()
    for key, val in query_params.items():
        query_params[key] = val[0]
    return query_params


def set_url_query_parameters(query_params: dict[str, str]) -> None:
    st.experimental_set_query_params(**query_params)


def get_node() -> Union[str, None]:
    query_params = get_url_query_parameters()
    if not len(query_params):
        return None
    elif "node" not in query_params.keys():
        return None
    else:
        return query_params["node"]


def set_node(node: str) -> None:
    set_url_query_parameters({"node": node})


def reset_node() -> None:
    set_url_query_parameters(dict())


def redirect(url: str):
    nav_script = """
        <meta http-equiv="refresh" content="0; url='%s'">
    """ % (
        url
    )
    st.write(nav_script, unsafe_allow_html=True)


def inject_css(css: str) -> None:
    """
    Inject CSS into streamlit application.

    Args:
        css (str): css style string
    """
    st.markdown(f"<style>\n{css}\n</style>", unsafe_allow_html=True)


def inject_hotkey_jump_to_selectbox(
    selectbox_label: str, special: list[str] = ["shift", "meta"], character: str = "k"
):
    "meta (cmd/windows) + k hardcoded"
    special_substring = [f"e.{s}Key" for s in special]
    special_substring = " && ".join(special_substring)
    js_code = """
    <script>
    const doc = window.parent.document;
    doc.addEventListener('keydown', function(e) {"""
    js_code += f"""
    if ({special_substring} && e.key === '{character}') {{
        var selectbox = doc.querySelector("input[aria-label*='{selectbox_label}']");
        var parentDiv = selectbox.parentNode.parentNode.parentNode;
        var clearValue = parentDiv.querySelector("svg[title='Clear value']");
        if (clearValue) {{
            var clickEvent = new MouseEvent("click", {{
                bubbles: true,
                cancelable: true,
                view: window
            }});
            clearValue.dispatchEvent(clickEvent);
        }};

        if (selectbox) {{
            e.preventDefault();
            selectbox.click();
            selectbox.value = '';
        }}
    }}"""

    js_code += """
    });
    </script>
    """
    components.html(js_code, height=0, width=0)


# todo: implement development mode
def make_app_start_command(
    app_path: Union[str, Path],
    open_browser: bool = False,
    development_mode: bool = False,
    magic_enabled: bool = False,
) -> list[str]:
    """
    subprocess start command for app

    Args:
        _open (bool, optional): open the GUI in the default browser window. Defaults to False.

    Returns:
        list[str]: the start command

    look into:
    --client.caching
    --client.displayEnabled
    --runner.installTracer
    --runner.postScriptGC
    --runner.fastReruns < this seems intuitively like there could be a security vulnerability
    --server.scriptHealthCheckEnabled
    --server.baseUrlPath
    --server.maxMessageSize
    --server.enableWebsocketCompression
    --server.enableStaticServing
    --magic.displayRootDocString
    --magic.displayLastExprIfNoSemicolon
    --deprecation.showfileUploaderEncoding
    --deprecation.showImageFormat
    --deprecation.showPyplotGlobalUse
    --global.showWarningOnDirectExecution False

    look into, but don't use:
    --server.sslCertFile * excerpt from CLI docs: DO NOT USE THIS OPTION IN A PRODUCTION ENVIRONMENT.
    --server.sslKeyFile * excerpt from CLI docs: DO NOT USE THIS OPTION IN A PRODUCTION ENVIRONMENT.

    maybe use:
    --server.maxUploadSize < not currently relevant

    added, but look into in more detail:
    --server.enableCORS
    --server.enableXsrfProtection

    ui, test differences:
    --ui.hideSidebarNav
    --theme.primaryColor
    --theme.backgroundColor
    --theme.secondaryBackgroundColor
    --theme.textColor
    --theme.font

    INFO
    --global.developmentMode > seems to be mostly used for developing streamlit components

    show text
    --theme.textColor "#0F5555"
    """

    return [
        sys.executable,
        "-m",
        "streamlit",
        "run",
        app_path,
        "--global.developmentMode=False",
        "--global.suppressDeprecationWarnings=False",
        "--logger.enableRich=True",
        "--client.showErrorDetails=True",
        "--client.toolbarMode=minimal",
        f"--runner.magicEnabled={str(magic_enabled)}",
        f"--server.headless={str(not open_browser)}",
        "--server.runOnSave=True",
        "--server.allowRunOnSave=True",
        "--server.enableCORS=True",
        "--server.enableXsrfProtection=True",
        "--browser.gatherUsageStats=False",
        "--theme.base=dark",
        "--theme.primaryColor=#4b77ff",
        # "--theme.backgroundColor=#161616",
        "--ui.hideTopBar=True",
        "--server.address=localhost",
        "--server.port=31415",
    ]


# ! temp archive


# def get_url_auth_code(query_params: dict[str, str]) -> Union[str, None]:
#     if not len(query_params):
#         return None
#     elif "code" not in query_params.keys():
#         return None
#     else:
#         return query_params["code"]
