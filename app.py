import streamlit as st
from src.functions import *
from streamlit_extras.switch_page_button import switch_page

st.set_page_config(initial_sidebar_state = "collapsed",
                   page_icon = "util/imgs/logo.png",
                   page_title = "Challenge NoName")

st.markdown(
    """
        <style>
            [data-testid="collapsedControl"] {
                display: none
            }
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
        </style>
    """,
    unsafe_allow_html = True)
col_project_name, col_img  = st.columns([3, 1])
col_img.image("util/imgs/logo.png")
col_project_name.header("Challenge SAP")
st.markdown("---", unsafe_allow_html = True)

st.info("Este aplicativo está em desenvolvimento pelo time da NoName!")
st.success("Constituido por: Henrico, Felype, Sara, Emily e Daniel!")

if st.button("Preencher dados do produto"):
    switch_page("cadastro_produto")