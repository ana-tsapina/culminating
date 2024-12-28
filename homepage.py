import streamlit as st 

st.title("What would you like to do? ")

st.page_link("pages/Log.py", label = "One")
st.page_link("pages/Calendar.py", label = "Calendar")
st.page_link("pages/Settings.py", label = "Settings")