import streamlit as st 
import sqlite3
import pandas as pd 
import numpy as np 


#Define functions to connect to databases used to store data throughout project 

def begin_connection_tasks():
    conn = sqlite3.connect('tasks.db')
    return conn 

def begin_connection_messages():
    conn_mes = sqlite3.connect('messages.db')
    return conn_mes 

def connection_yes():
    conn_y = sqlite3.connect('count_yes.db')
    return conn_y

def connection_no():
    conn_n = sqlite3.connect('count_no.db')
    return conn_n

#Connect to databases and set up cursor objects for each one

conn = begin_connection_tasks()
conn_mes = begin_connection_messages()
c = conn.cursor()
cm = conn_mes.cursor()

conn_y = connection_yes()
cy = conn_y.cursor()

conn_n = connection_no()
cn = conn_n.cursor()

# define functions to delete, display, and insert data for each respecitive database
def delete_data(task, due_time, due_date, duration, category, priority, resource_id):
    conn = begin_connection_tasks()
    c = conn.cursor()
    result = c.execute('''
             DELETE FROM tasks 
        ''')
    conn.commit()
    conn.close()

def load_tasks():
    conn = begin_connection_tasks()
    c = conn.cursor()
    c.execute("SELECT * FROM tasks")
    rows = c.fetchall()
    conn.close()
    return rows

def insert_data(task, due_time, due_date, duration, category, priority, resource_id):
    conn = begin_connection_tasks()
    c = conn.cursor()
    c.execute("INSERT INTO tasks (task, due-time, due_date, duration, category, priority, resource_id) VALUES (?,?, ?, ?,?, ?,?)", (task, due_time, due_date, duration, category, priority, resource_id))
    conn.commit()
    conn.close()

def delete_table(): 
    conn = begin_connection_tasks()
    c = conn.cursor()
    c.execute("DROP TABLE tasks")
    conn.commit()
    conn.close()

def delete_yes(): 
    conn_y = connection_yes()
    cy = conn_y.cursor()
    cy.execute("DELETE FROM count_yes")
    conn_y.commit()
    conn_y.close()

def delete_no(): 
    conn_n = connection_no()
    cn = conn_n.cursor()
    cn.execute("DELETE FROM count_no")
    conn_n.commit()
    conn_n.close()

#Below are functions specifically related to the 'messages' database. In this group, there are functions to connect to the database, to insert messages of each kind in to it, as well as to delete the values in the table

def message_table_creation(): 
    conn_mes = begin_connection_messages()
    cm = conn_mes.cursor()
    cm.execute(
        '''CREATE TABLE IF NOT EXISTS messages( 
            encouraging_messages TEXT, 
            redirecting_messages TEXT
        )''') 
    conn_mes.commit()
    conn_mes.close()

def insert_positive(encouraging_messages, redirecting_message):
    conn_mes = begin_connection_messages()
    cm = conn_mes.cursor()
    cm.execute("INSERT INTO messages (encouraging_messages, redirecting_messages) VALUES (?, ?)", (encouraging_messages, redirecting_message))
    conn_mes.commit()
    conn_mes.close()

def load_messages():
    conn_mes = begin_connection_messages()
    cm = conn_mes.cursor()
    cm.execute("SELECT * FROM messages")
    rows = cm.fetchall()
    conn_mes.close()
    return rows

def delete_messages():
    conn_mes = begin_connection_messages()
    cm = conn_mes.cursor()
    result = cm.execute('''
             DELETE FROM messages 
        ''')
    conn_mes.commit()
    conn_mes.close()


#Checks to see if 'message_table_creation' already exists and is being stored in the session state. If not, it creates the database. 

if "message_table_creation" not in st.session_state:
    st.session_state["message_table_creation"] = True
    message_table_creation()

#Titles and subheadings to indicate the different sections of the page 
st.title("Settings")

#Below are actions related to the 'task' database
st.subheader("Clear Task Database: ")

clear = st.button("Clear Database")

if clear: 
   delete_data('task', 'due_time', 'due_date', 'duration', 'category','priority','resource_id')

#Below are actions realated to editing the entries in the 'messages' database (allowing user to add customized messages and to to display them)
st.subheader("Edit messages: ")

encouraging_messages = st.text_input("Customize your message of Encouragement")
redirecting_messages = st.text_input("Customize your message for Redirection")
save = st.button("Save")
if save: 
    insert_positive(encouraging_messages, redirecting_messages)


#The following allow the user to display their entries in the 'messages' database and to clear it as well
st.subheader("Message Database: ")

if st.button("Display Messages"): 
    tasks = load_messages()
    info = cm.execute("Select * FROM messages")
    st.dataframe(info)
    rows = cm.fetchall()

if st.button("Clear Message Database"): 
    delete_messages()

#The following buttons allow the user to reset the count of days that were spent on task and not 

st.subheader("Day Count Settings: ")

if st.button("Clear 'Yes' Count Table"): 
    delete_yes()

if st.button("Clear 'No' Count Table"): 
    delete_no()


