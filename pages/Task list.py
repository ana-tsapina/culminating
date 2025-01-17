import streamlit as st 
import sqlite3
import pandas as pd 
import numpy as np


#Functions to connect to 'tasks' database, as well as to select and display the data it holds

def begin_connection():
    conn = sqlite3.connect('tasks.db')
    return conn

def load_tasks():
    conn = begin_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM tasks")
    rows = c.fetchall()
    conn.close()
    return rows

def display_tasks(): 
    tasks = load_tasks()
    info = c.execute("Select * FROM tasks")
    st.dataframe(info)
    rows = c.fetchall()

#Connect to database 'tasks'
#Define c, which creates a cursor object so as to send commands to the databse, as well as to traverse and fetch records 
conn = begin_connection()
c = conn.cursor()

if 'clicked' not in st.session_state:
    st.session_state.clicked = False 

st.title("List of Tasks to Do: ")
display_tasks()

st.image("https://images.unsplash.com/photo-1542123491-63f422a5f45e?q=80&w=2940&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D", width = 500)

