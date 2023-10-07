import streamlit as st
from src.functions import *
from streamlit_extras.switch_page_button import switch_page
import pandas as pd


st.set_page_config(initial_sidebar_state = "collapsed",
                   page_icon = "util/imgs/logo-horus.png",
                   page_title = "NoName")

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
col_project_name.image("./util/imgs/logo-horus.png", width = 200)

st.markdown("---", unsafe_allow_html = True)

email_log = consultar_email_em_log()

#with st.expander("Atualizar chave pessoal"):
#    api_column, botao_column  = st.columns([3, 1])
#    with api_column:
#        api = st.text_input("Token pessoal do Openai",type="password")
#    with botao_column:
#        adicionar = st.button("adicionar novo token")
#        if adicionar:
#            atualizar_chave_api(api)
#            st.success('API adicionada com sucesso')
#            api = ''
#            st.experimental_rerun()



if st.button("Preencher dados do produto"):
    switch_page("cadastro_produto")
elif st.button("Preencher base com dados do produto"):
    switch_page("preencher_excel")
elif st.button("Detectar produtos"):
    switch_page("detectar_produtos")
elif st.button("Atualizar base"):
    switch_page("adicionar_novo_df")
elif st.button("Sair"):
    switch_page("app")

with st.expander(f"Databases do Usuario: {email_log}"):
    try:
        st.dataframe(get_user_dataframes(), use_container_width = True)
    except:
        st.warning("Este usuario ainda nao possui bases em seu cadastro!")