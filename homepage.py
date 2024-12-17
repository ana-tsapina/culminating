import streamlit as st
import numpy 
from PIL import Image



st.title("Amplify")


st.page_link("pages/Log.py", label = ":gray-background[Log]", use_container_width = True)
st.page_link("pages/Settings.py", label = ":gray-background[Settings]")  
st.page_link("pages/Calendar.py", label = ":gray-background[Calendar]")  

st.text_input("Enter your priority task: ")


st.title("what would you like to do? ")


log = st.button("Log") 
settings = st.button("Settings")
cal = st.button("Calendar")