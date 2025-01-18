import streamlit as st 
import sqlite3
from datetime import datetime

#Define function to connect to 'tasks' database, as well as to create the database 

def begin_connection():
    conn = sqlite3.connect('tasks.db')
    return conn 

#Connect to 'tasks' and set cursor object
conn = begin_connection()
c = conn.cursor()
 
def table_creation(): 
    conn = begin_connection()
    c = conn.cursor()
    c.execute(
        '''CREATE TABLE IF NOT EXISTS tasks( 
            task TEXT, 
            due_time TEXT,
            due_date TEXT,
            duration TEXT, 
            category TEXT,
            priority INTEGER,
            resource_id TEXT
        )''') 
    conn.commit()
    conn.close()

# Define functions to insert data into 'tasks' and display it  
def insert_data(task, due_time, due_date, duration, category, priority, resource_id):
    conn = begin_connection()
    c = conn.cursor()
    c.execute("INSERT INTO tasks (task, due_time, due_date, duration, category, priority, resource_id) VALUES (?,?,?,?,?, ?,?)", (task, due_time, due_date, duration, category, priority, resource_id))
    conn.commit()
    conn.close()

def load_tasks(): 
    conn = begin_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM tasks")
    rows = c.fetchall()
    conn.close()
    return rows 

#The following code ensures that the table is created only once if it is not already existent in session state, which allows for the ability to persist state
if "table_creation" not in st.session_state:
    st.session_state["table_creation"] = True
    table_creation()

#Page Title 
st.title("Task Organization")

#User Input
day = st.date_input("What day is it today? ")
task = st.text_input("What task do you want to add?")
due_input = st.time_input("When is it due? (Use 24 hour time)", step = 60)
due_time = due_input.strftime('%H:%M') 
due_date_input = st.date_input("On which day is it due?")
due_date = due_date_input.strftime("%m/%d/%Y, %H:%M:%S")
duration_input = st.time_input("How long will it take?")
resource_id = "a" #resource_id is a value that is necessary to have in order to connect to the calendar, and thus is not customizable 
duration = duration_input.strftime('%H:%M')
category = st.radio("Category", ["Physiological", "Safety and Security", "Love and Belonging", "Self-Esteem", "Self-Actualization"])
priority = st.slider("How important is it to you?", min_value = 0, max_value = 5, value = 2)
add = st.button('Add')


# Ensures that when 'add' is clicked, the user inputs three key data components: the name of the task, the day it is due, and the priority rating they give it. Otherwise, an error message is displayed.
# These values are important because they are used to track and calculate the urgency of the task  

if add: 
    if task != "" and due_date != "" and priority != "":
        insert_data(task, due_time, due_date, duration, category, priority, resource_id)
        st.success("Your task has been added! ")
    else: 
        st.error("You are missing key data. Please ensure that all rows are filled")
    
#Button to show tasks in 'tasks'
if st.button("Show Tasks"): 
    tasks = load_tasks()
    info = c.execute("Select * FROM tasks")
    st.dataframe(info)
    rows = c.fetchall()




