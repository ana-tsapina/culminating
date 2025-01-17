import streamlit as st 

# Amplify Homepage 
# User can use the sidebar to navigate the different webpages, though there are page links to the most focal functionings of this project on this page

st.title("Welcome to Amplify! ")

st.image("https://i.pinimg.com/736x/11/55/3d/11553de3a98fa70d70d8351378ff9761.jpg")


col1, col2, col3 = st.columns(3)


col1 = st.page_link("pages/Log.py", label = "Log", icon = "💾")
col2 = st.page_link("pages/My Calendar.py", label = "Calendar", icon = "🗓")
col3 = st.page_link("pages/Accountability.py", label = "Reflection Zone", icon = "📝")
