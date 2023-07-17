import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from src.modelo_gpt import get_response
import pandas as pd



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
        df = pd.read_excel(uploaded_file)
        with st.expander("Seu arquivo"):    
            st.dataframe(df)
        with st.expander("Criar coluna de descrição"): 
            coluna = st.selectbox("Selecione o nome da coluna que contem os nomes dos produtos", options = df.columns)
            if st.button("Gerar descrição"):
                if coluna:
                    try:
                        with st.spinner("Gerando descrições, por favor aguarde..."):
                            df['Descricao'] = ''
                            for i in df.index:
                                nome = df.loc[i,coluna]
                                descricao = get_response(f"Escreva uma descricao para o produto (em apenas 10 palavras): {nome}")
                                df.loc[i,'Descricao'] = descricao
                            st.dataframe(df)

                        excel = df.to_csv(sep=";").encode('utf-8')
                        st.download_button(label = "Baixar o Excel", data = excel, file_name = f'{uploaded_file.name}_descricao.csv')

                    except Exception as e:
                        st.error(f'Ocorreu um erro com o Chat GPT: {e}')
                else:
                    st.warning("Por favor preencha o nome da coluna que contem os nomes")