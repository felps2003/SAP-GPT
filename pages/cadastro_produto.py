import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from src.modelo_gpt import get_response


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
if st.button("Tela Inicial"):
    switch_page("app")
st.markdown("---", unsafe_allow_html = True)

col_data1, col_data2, col_data3 = st.columns([1, 1, 1])
id_produto = col_data1.number_input("ID: ", step = 1)
nome_produto = col_data2.text_input("Nome: ")
decisao_descricao = col_data3.radio(
    f"Selecione a opçao desejada para a criacao da descricao do produto: {nome_produto}", 
    options = ("Escrever", "ChatGPT"))

if decisao_descricao == "ChatGPT":
    try: 
        descricao_produto = get_response(f"Escreva uma descricao para o produto: {nome_produto}")
    except Exception as e:
        st.error(f"Alguem erro encontrado em relaçao ao chatgpt. Erro: {e}")
        
if decisao_descricao == "Escrever":
    descricao_produto = st.text_area(label = "Descrição do Produto")

submit = st.button("Enviar")
if submit:
    text_produto = """
                   ID do produto: {}
                   Nome do produto: {}
                   Descrição do produto: {}
                   """.format(id_produto, nome_produto, descricao_produto)
    st.text(text_produto)
    st.balloons()