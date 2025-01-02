import streamlit as st 
import sqlite3
from datetime import datetime

@st.cache_data 
def query(): 
    info = c.execute("Select * FROM tasks")
    return st.dataframe(info)

def begin_connection():
    conn = sqlite3.connect('tasks.db')
    return conn 

conn = begin_connection()
c = conn.cursor()
 
def insert_data(task, due_date, duration, category, priority):
    conn = begin_connection()
    c = conn.cursor()
    c.execute("INSERT INTO tasks (task, due_date, duration, category, priority) VALUES (?,?,?,?,?)", (task, due_date, duration, category, priority))
    conn.commit()
    conn.close()

def table_creation(): 
    conn = begin_connection()
    c = conn.cursor()
    c.execute('DROP TABLE IF EXISTS tasks')
    c.execute(
        '''CREATE TABLE tasks( 
            task TEXT, 
            due_date TEXT,
            duration TEXT, 
            category TEXT,
            priority INTEGER
        )''') 
    conn.commit()
    conn.close()

if "table_creation" not in st.session_state:
    st.session_state["table_creation"] = True
    table_creation()

st.title("Task Organization")
day = st.date_input("What day is it today? ")
task = st.text_input("What task do you want to add?")
due_input = st.time_input("When is it due? (Use 24 hour time)", step = 60)
due_date = due_input.strftime('%H:%M')
duration_input = st.time_input("How long will it take?")
duration = duration_input.strftime('%H:%M')
category = st.radio("Category", ["Physiological", "Safety and Security", "Love and Belonging", "Self-Esteem", "Self-Actualization"])
priority = st.slider("How important is it to you?", min_value = 0, max_value = 5, value = 2)
add = st.button('Add')


#print sucess after adding 


if add: 
    insert_data(task, due_date, duration, category, priority)


#if st.button("Show Tasks"): 
    #st.dataframe()


    #c.execute("Select * FROM tasks")
    #rows = c.fetchall()
   # st.write(rows)


    
if st.button("Show Tasks"): 
    info = c.execute("Select * FROM tasks")
    st.dataframe(info)
    rows = c.fetchall()





