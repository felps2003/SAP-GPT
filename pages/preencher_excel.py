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
            st.table(df)
        with st.expander("Criar coluna de descrição"): 
            coluna = st.text_input("Qual o nome da coluna que contem os nomes dos produtos")
            if st.button("Gerar descrição"):
                if coluna:
                    try:
                        df['Descricao'] = ''
                        for i in df.index:
                            nome = df.loc[i,coluna]
                            descricao = get_response(f"Escreva uma descricao para o produto (em apenas 10 palavras): {nome}")
                            df.loc[i,'Descricao'] = descricao
                        st.table(df)
                        excel = df.to_excel()
                        st.download_button(label="Baixar o Excel",data=excel,file_name='large_df.xlsx')

                    except:
                        st.error('Ocorreu um erro com o Chat GPT')
                else:
                    st.warning("Por favor preencha o nome da coluna que contem os nomes")