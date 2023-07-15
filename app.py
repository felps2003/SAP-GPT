import streamlit as st
from src.functions import *
from streamlit_extras.switch_page_button import switch_page
import pandas as pd


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


# con = sqlite3.connect("data/data.db")
# cur = con.cursor()
can_pass = False
tab_login, tab_create = st.tabs(["Login", "Criar conta"])


if tab_login:
    with tab_login:
        placeholder_login = st.empty()
        with placeholder_login.form("login"):
            email = st.text_input("Email")
            password = st.text_input("Senha", type = "password")
            submit = st.form_submit_button("Entrar")

        if submit and email:
            data = pd.DataFrame()
            # data = pd.read_sql_query("SELECT * from usuarios", con)

            for _, col in data.iterrows():
                if email == str(col.email) and password == str(col.password):
                    auth = True
                    break
                else:
                    auth = False
                    continue

            if "auth" in globals():
                if auth != False:
                    can_pass = True
                    placeholder_login.empty()
                    st.success("Usuario Autenticado!")
                else:
                    st.error("Usuario nao autenticado")
            else:
                pass

        elif submit and not email:
            st.warning("Por favor coloque seu email")

if tab_create:
    with tab_create:
        placeholder_create = st.empty()
        with placeholder_create.form("create"):
            email_create = st.text_input("Email")
            password_create = st.text_input("Senha", type = "password")
            confirm_password = st.text_input("Confirmar senha", type = "password")
            send = st.form_submit_button("Criar conta")

            if send:
                if not email_create:
                    st.warning("Por favor coloque seu email.")
                elif not password_create:
                    st.warning("Por favor coloque sua senha.")
                elif not confirm_password:
                    st.warning("Por favor confirme a senha.")
                elif password_create != confirm_password:
                    st.warning("Senha nao coincidem!")
                else:
                    # cur.execute(f"INSERT INTO usuarios (email,password) VALUES (?,?);", (email_create, password_create)).fetchall()
                    # con.commit()                
                    st.success("Login created successfully!!!")

if can_pass != False:
    if st.button("Preencher dados do produto"):
        switch_page("cadastro_produto")
    elif st.button("Enviar Excel para preencher dados do produto"):
        switch_page("preencher_excel")