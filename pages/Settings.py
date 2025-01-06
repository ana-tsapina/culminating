import streamlit as st 
import sqlite3
import pandas as pd 
import numpy as np 

def begin_connection():
    conn = sqlite3.connect('tasks.db')
    return conn 

def delete_data(task, due_time, due_date, duration, category, priority):
    conn = begin_connection()
    c = conn.cursor()
    result = c.execute('''
             DELETE FROM tasks 
        ''')
    conn.commit()
    conn.close()

def load_tasks():
    conn = begin_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM tasks")
    rows = c.fetchall()
    conn.close()
    return rows

def insert_data(task, duration, category, priority):
    conn = begin_connection()
    c = conn.cursor()
    c.execute("INSERT INTO tasks (task, due-time, due_date, duration, category, priority) VALUES (?,?, ?, ?,?,?)", (task, due_time, due_date, duration, category, priority))
    conn.commit()
    conn.close()


conn = begin_connection()
c = conn.cursor()

# st.title("Enter key info here!")
# st.subheader("These are timeblocks that will not be altered in your scheduele. This is specifically for sleep ")

# task = "sleep" 
# priority = "5"

# sleep = st.time_input("How long do you sleep for? (Aim for 6-8hr)")
# bed_time_input = st.time_input("When do you go to bed? ", step = 60)
# bed_time = bed_time_input.strftime('%H:%M')
# calendar_options["slotMaxTime"] = bed_time
# wake_input = st.time_input("When do you wake up? ", step = 60)
# wake = wake_input.strftime('%H%M')
# calendar_options["slotMinTime"] = wake 
# confirm = st.button("Confirm")
     
#some how work around time for sleep, treat as own category 
# add or delete tasks 

clear = st.button("Clear Database")

if clear: 
   delete_data('task', 'due_time', 'due_date', 'duration', 'category','priority')

