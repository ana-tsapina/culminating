import streamlit as st 

st.title("what would you like to do? ")


log = st.button("Log")
settings = st.button("Settings")
cal = st.button("Calendar")

if log: 
        st.switch_page("Log.py")
if settings: 
        st.switch_page("Settings.py")
if Calendar: 
        st.switch_page("Calendar.py")