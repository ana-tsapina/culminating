import streamlit as st 

st.text_input("What are your priorities for today? ")



task = st.text_input("Enter your task", " ")

if st.button("Add Task"): 
    if task: 
        st.session_state["task_list"].append(task)

if "task_list" not in st.session_state: 
    st.session_state["task_list"] = []

for i, t in enumerate(st.session_state["task_list"]):
    st.write(f"{i+1}, {t}")

for i, t in enumerate(st.session_state["task_list"]):
    if st.checkbox(f"{i+1}. t")
        st. sesion_state["task_list"]. remove(t)