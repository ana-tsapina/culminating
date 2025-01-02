import streamlit as st 
import sqlite3
import pandas as pd 
import numpy as np 

def begin_connection():
    conn = sqlite3.connect('tasks.db')
    return conn 

def insert_data(task, duration, category, priority):
    conn = begin_connection()
    c = conn.cursor()
    c.execute("INSERT INTO tasks (task, duration, category, priority) VALUES (?,?,?,?)", (task, duration, category, priority))
    conn.commit()
    conn.close()

conn = begin_connection()
c = conn.cursor()

st.title("Enter key info here!")
st.subheader("These are timeblocks that will not be altered in your scheduele. This is specifically for sleep ")


sleep = st.time_input("How long do you sleep for? (Aim for 6-8hr)")
bed_time = st.number_input("When do you go to bed? ")
wake = st.number_input("When do you wake up? ")



#some how work around time for sleep, treat as own category 