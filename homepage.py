import streamlit as st 

st.title("what would you like to do? ")


log = st.button("Log")
settings = st.button("Settings")


st.page_link("pages/Log.py", label = "One")