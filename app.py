import streamlit as st
from src import modelo_gpt
from streamlit_extras.switch_page_button import switch_page

st.set_page_config(initial_sidebar_state = "collapsed")

st.markdown("<h1>GPT teste</h1>", unsafe_allow_html = True)

texto_usuario = st.text_input("Faça a pergunta: ")

if texto_usuario:
    st.write('Resposta: ', modelo_gpt.get_response(texto_usuario))

if st.button("switch"):
    switch_page("teste")