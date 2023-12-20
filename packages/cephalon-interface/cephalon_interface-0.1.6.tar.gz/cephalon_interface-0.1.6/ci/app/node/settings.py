import streamlit as st
from ci.core import cephalon


def about():
    st.write("About")


def catalog():
    st.write("Catalog")


def render():
    (
        about_tab,
        catalog_tab,
    ) = st.tabs(["About", "Catalog"])
    with about_tab:
        about()
    with catalog_tab:
        catalog()
