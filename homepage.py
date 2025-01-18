import streamlit as st 

# Amplify Homepage 
# User can use the sidebar to navigate the different webpages, though there are page links to the most focal functionings of this project on this page

st.title("Welcome to Amplify! ")
st.image("https://i.pinimg.com/736x/11/55/3d/11553de3a98fa70d70d8351378ff9761.jpg")


# Variables that connect to pagelinks 
st.page_link("pages/Log.py", label = "Log", icon = "💾")
st.page_link("pages/My Calendar.py", label = "Calendar", icon = "🗓")
st.page_link("pages/Accountability.py", label = "Reflection Zone", icon = "📝")
