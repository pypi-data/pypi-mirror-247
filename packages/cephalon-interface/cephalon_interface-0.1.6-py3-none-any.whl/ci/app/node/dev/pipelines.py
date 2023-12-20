"""
Save custom transforms and scripts and load them to create pipelines.
"""

import streamlit as st
from streamlit_ace import st_ace
from ci.core import cephalon
from ci.utility import streamlit


ace_custom = """
.ace_scroller, .ace_gutter {
    top: 1rem !important;
}
"""


# 28, 31

default = """from ci import system

def function(x: int) -> int:
    return x
"""
# todo: should check user is not in homebrew installation
# * they really ought to be using vscode for something like this
# todo.sub: add a button to open in vscode

# todo: add code graph (barfi)


def render():
    content = st_ace(value=default, language="python", theme="dracula")
    streamlit.inject_css(ace_custom)
