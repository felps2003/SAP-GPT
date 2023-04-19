import streamlit as st
from src.modelo_gpt import get_response
from src.functions import *
from streamlit_extras.switch_page_button import switch_page

st.set_page_config(initial_sidebar_state = "collapsed",
                   page_icon = "util/imgs/logo.png",
                   page_title = "Challenge NoName")

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html = True) 

st.image("util/imgs/logo.png")

st.markdown("<h1>GPT teste</h1>", unsafe_allow_html = True)

texto_usuario = st.text_input("Faça a pergunta: ")

if st.button("Send question"):
    if not texto_usuario:
        st.warning("Please enter a prompt!")
    else:
        st.write('Resposta: ', get_response(texto_usuario))

if st.button("switch"):
    switch_page("teste")