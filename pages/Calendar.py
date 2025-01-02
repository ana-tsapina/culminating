import streamlit as st 
import sqlite3
import pandas as pd 
import numpy as np 

def begin_connection():
    conn = sqlite3.connect('tasks.db')
    return conn 

conn = begin_connection()
c = conn.cursor()

st.title("Here's your Schedule for Today")
top_priority = c.execute("SELECT task FROM tasks WHERE priority =5 AND category != 'Physiological' ")
st.write("Priorities = ", *top_priority)

info = c.execute("Select * FROM tasks")
st.dataframe(info)


att = c.execute("SELECT task FROM tasks WHERE priority=2 AND category='Love and Belonging'")

# want to organize day 
#first: set default sleeping times as phys. 
# ask for duration!!!
# 





















st.dataframe(att)












