import streamlit as st
from src import switch_page


st.set_page_config(initial_sidebar_state = "collapsed")

st.markdown("<h1>Olá mundo</h1>", unsafe_allow_html=True)