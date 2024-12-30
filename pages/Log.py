import streamlit as st 
import sqlite3

conn = sqlite3.connect('to_do.db')
c = conn.cursor()


def data_entry(activity, due_date, type): 
    c.execute('INSERT INTO progress (task, due_date, category) VALUES(?,?,?)', (task, due_date, category))
    conn.commit()
   
def create_table(): 
    conn 

task = st.text_input("What task do you want to add?")
due_date = st.text_input("When is it due?")
category = st.radio("Category", ["Physiological", "Safety and Security", "Love and Belonging", "Self-Esteem", "Self-Actualization"])
add = st.button('Add')

if add: 
    if task and due_date and category: 
        data_entry(task, due_date, category)
    else: 
        st.warning("Please enter a name")


if st.button("Show Tasks"): 
    c.execute("Select * FROM progress")
    rows = c.fetchall()






# class ToDo: 
#     def __init__(self, task): 
#         self.task = task

 
# connect = sqlite3.connect(tasks.sqlite)
# c = connect.cursor()


# c.execute('''
#     INSERT INTO tasks (current)
# ''')
# connect.commit()

# insert_data()

