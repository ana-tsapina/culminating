import streamlit as st 
import sqlite3
import pandas as pd 
import numpy as np 

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


conn = begin_connection()
c = conn.cursor()




if st.button("Show list"): 
    st.write(events_with_calculated_priority)

if st.button("show_algo"): 
    st.write(add_to_cal)


st.write("THIS IS YOUR TASK LIST ")
display_tasks()



