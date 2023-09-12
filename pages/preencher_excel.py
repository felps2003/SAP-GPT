import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from src.functions import *
import pandas as pd
import time

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

st.image("./util/imgs/logo-horus.png", width = 200)

st.subheader("Preencher base de dados")

st.markdown('---')



col1, col2, col3 = st.columns(3)

with col1:
    if st.button("Voltar"):
        switch_page("main")

with col2:
    st.text("Contagem de dashboard's")
    st.title(contagem_de_dashboards())

with col3:
    st.text('Chave API')
    if obter_api() == '':
        st.error('Desativado')
    else:
        st.success('Ativo')

st.markdown('---')

coluna1, coluna2 = st.columns(2)

with coluna1:
    st.header('Enviar planilha')

with coluna2:
    uploaded_files = st.file_uploader("", accept_multiple_files=True)

st.markdown('---')
for uploaded_file in uploaded_files:
    bytes_data = uploaded_file.read()
    st.write("Nome do arquivo:", uploaded_file.name)
    if uploaded_file:
        df = pd.read_excel(uploaded_file)
        df.reset_index(drop = True, inplace = True)
        with st.expander("Seu arquivo"):    
            st.dataframe(df)
        with st.expander("Criar coluna de descrição"): 
            coluna = st.selectbox("Selecione o nome da coluna que contem os nomes dos produtos", options = df.columns)
            time_sleep = st.slider('Quantidade de segundos entre as requisições', 0, 180, 60)
            if st.button("Gerar descrição"):
                if coluna:
                    try:
                        with st.spinner("Gerando descrições, por favor aguarde..."):
                            df['Descricao'] = ''
                            for i in df.index:
                                nome = df.loc[i,coluna]
                                descricao = get_response(f"Escreva uma descricao para o produto (em apenas 10 palavras): {nome}")
                                df.loc[i,'Descricao'] = descricao
                                time.sleep(time_sleep)
                            st.dataframe(df)

                        csv = df.to_csv(sep=";").encode('utf-8')
                        df = df.to_excel(df)
                        nome = st.text_input('*Nome do excel')
                        botao = st.button('Adicionar')
                        if botao:
                            if nome != '':
                                coluna, dados = ler_dataframe_e_converter(df)
                                adicionar_dataframe_para_email(nome,coluna,dados)
                                st.success('Foi adicionado com sucesso')
                        st.download_button(label = "Baixar o Excel", data = csv, file_name = f'{uploaded_file.name}_descricao.csv')
                        

                    except Exception as e:
                        st.error(f'Ocorreu um erro com o Chat GPT: {e}')
                else:
                    st.warning("Por favor preencha o nome da coluna que contem os nomes")