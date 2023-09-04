import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from src.modelo_gpt import get_response
import pandas as pd
from src.functions import *



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


uploaded_files = st.file_uploader("Enviar Excel", accept_multiple_files=True)
for uploaded_file in uploaded_files:
    bytes_data = uploaded_file.read()
    st.write("Nome do arquivo:", uploaded_file.name)
    if uploaded_file:
        try:
            df = pd.read_excel(uploaded_file)
        except:
            df = pd.read_csv(uploaded_file)
        teste = ler_dataframe_e_converter(df, sheet_name=None)
        email = consultar_email_em_log()
        nome_tabela = st.text_input("Nome da Tabela")
        if st.button("Adicionar novo Excel"):
            adicionar = adicionar_dataframe_para_email(nome_tabela, teste[0], teste[1])
            if adicionar == True:
                st.success('Tabela adicionada com sucesso')
            else: 
                st.error('Tabela não adicionada')