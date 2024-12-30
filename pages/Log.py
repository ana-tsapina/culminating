import streamlit as st 
import sqlite3
from datetime import datetime


def begin_connection():
    conn = sqlite3.connect('tasks.db')
    return conn 

conn = begin_connection()
c = conn.cursor()

def insert_data(task, due_date, category, priority):
    conn = begin_connection()
    c = conn.cursor()
    c.execute("INSERT INTO tasks (task, due_date, category, priority) VALUES (?,?,?,?)", (task, due_date, category, priority))
    conn.commit()
    conn.close()

def table_creation(): 
    conn = begin_connection()
    c = conn.cursor()
    c.execute(
        '''CREATE TABLE IF NOT EXISTS tasks ( 
            task TEXT 
            due_date INT 
            category TEXT 
            priority INTEGER
        )''') 
    conn.commit()
    conn.close()


table_creation()

st.title("Task Organization")
day = st.date_input("What day is it today? ")
task = st.text_input("What task do you want to add?")
due_date = st.time_input("When is it due?", step = 60)
category = st.radio("Category", ["Physiological", "Safety and Security", "Love and Belonging", "Self-Esteem", "Self-Actualization"])
priority = st.slider("How important is it to you?", min_value = 0, max_value = 5, value = 2)
add = st.button('Add')


#print sucess after adding 


if add: 
    insert_data(task, due_date, category, priority)


if st.button("Show Tasks"): 
    c.execute("Select * FROM tasks")
    rows = c.fetchall()

