import streamlit as st 
import sqlite3
import numpy as np
import pandas as pd  
from pages.Settings import begin_connection_messages

#Define connections to databases 'count_yes' and 'count_no,' both keeping track of each day spent either productively or not 
def connection_yes():
    conn_y = sqlite3.connect('count_yes.db')
    return conn_y

def connection_no():
    conn_n = sqlite3.connect('count_no.db')
    return conn_n

#Connecting to and setting up cursors for each database
conn_y = connection_yes()
cy = conn_y.cursor()

conn_n = connection_no()
cn = conn_n.cursor()

conn_mes = begin_connection_messages()
cm = conn_mes.cursor()

#Defining functions realted to creating, inserting data into, and counting the sum of the databases mentioned above

def creation_count_yes(): 
    conn_y = connection_yes()
    cy = conn_y.cursor()
    cy.execute(
        '''CREATE TABLE IF NOT EXISTS count_yes( 
            yes INTEGER 
        )''') 
    conn_y.commit()
    conn_y.close()

def creation_count_no(): 
    conn_n = connection_no()
    cn = conn_n.cursor()
    cn.execute(
        '''CREATE TABLE IF NOT EXISTS count_no ( 
            no INTEGER
        )''') 
    conn_n.commit()
    conn_n.close()

def insert_yes(yes):
    conn_y = connection_yes()
    cy = conn_y.cursor()
    cy.execute("INSERT INTO count_yes (yes) VALUES (?)", (yes,))
    conn_y.commit()
    conn_y.close()

def insert_no(no):
    conn_n= connection_no()
    cn = conn_n.cursor()
    cn.execute("INSERT INTO count_no (no) VALUES (?)", (no,))
    conn_n.commit()
    conn_n.close()

def total_yes(): 
    conn_y = connection_yes()
    cy = conn_y.cursor()
    cy.execute('''SELECT SUM(yes) FROM count_yes ''')
    yes_result = cy.fetchone()
    conn_y.commit()
    conn_y.close()
    return yes_result[0]

def total_no(): 
    conn_n = connection_no()
    cn = conn_n.cursor()
    cn.execute('''SELECT SUM(no) FROM count_no ''')
    result_no = cn.fetchone()
    conn_n.commit()
    conn_n.close()
    return result_no[0]

#Define functions to connect to the 'messages' database, as well as to select and display entires   

def begin_connection_messages():
    conn_mes = sqlite3.connect('messages.db')
    return conn_mes 

def load_messages():
    conn_mes = begin_connection_messages()
    cm = conn_mes.cursor()
    cm.execute("SELECT * FROM messages")
    rows = cm.fetchall()
    conn_mes.close()
    return rows

#Checks if tables 'count_yes' and 'count_no' are present in st.session_state. If not, then the databases are created so that data can be stored and thus not lost between reruns. This happens once per session.

if "creation_count_yes" not in st.session_state:
    st.session_state["creation_count_yes"] = True
    creation_count_yes()

if "creation_count_no" not in st.session_state:
    st.session_state["creation_count_no"] = True
    creation_count_no()


st.title("Evaluate your Productivity")
st.image("https://images.unsplash.com/photo-1653569746987-8c1c63b2ffe2?q=80&w=1770&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D", width = 500)
st.subheader("Were you able to complete the tasks you prioritized? ")

st.markdown("***'Somewhat' will not lead to progress***")

left_column, middle_column, right_column = st.columns(3)

#Buttons to track productivity 
yes_button = left_column.button("Yes")
somewhat = middle_column.button("Somewhat")
no_button = right_column.button("No")

#If user's day was spent productively, then the integer one is added to the count_yes table and a random message of encouragement is displayed. The integer one is representative of a single whole day that is spent on task, and such days are then added up and diplayed. 
if yes_button:

    yes = 1
    insert_yes(yes)
 
    load = load_messages()
    get = cm.execute("SELECT encouraging_messages FROM messages ORDER BY RANDOM() LIMIT 1") 
    show = cm.fetchone()
    display = str(show[0])

    if display: 
        st.success(display)
    else: 
        st.error("No Encouraging Messages")


#If user's day was spent unproductively, then the integer one is added to the 'count_no' database to track the day. These values of one are added up to represent the total number of days spent unproductively. A message of redirection is also displayed. 
if no_button:
    no = 1
    insert_no(no) 
    load = load_messages()
    get = cm.execute("SELECT redirecting_messages FROM messages ORDER BY RANDOM() LIMIT 1") 
    show = cm.fetchone()
    display = str(show[0])

    if display: 
        st.error(display)
    else: 
        st.write("No Redirecting Messages")


#Use of functions to calculate total days spent on task and not 
y_total = total_yes()
n_total = total_no()

#Counter display 

st.header(f"Days Spent on Task: {y_total}")
st.header(f"Days spent NOT on Task : {n_total}")



