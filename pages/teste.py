import streamlit as st
from streamlit_extras.switch_page_button import switch_page

st.success("Page Switched")

if st.button("switchsds"):
    switch_page("app")