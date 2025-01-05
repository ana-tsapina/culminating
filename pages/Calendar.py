import streamlit as st
import sqlite3
import pandas as pd
import numpy as np
from streamlit_calendar import calendar
from pages.Settings import wake, bed_time
from datetime import datetime, timedelta

def begin_connection():
    conn = sqlite3.connect('tasks.db')
    return conn

def add_event(conn):
    c = conn.cursor()
    result = c.execute('''
            SELECT task, due_time, due_date, duration, category, priority FROM tasks
        ''')
    tasks = c.fetchall()
    return tasks

def load_tasks():
    conn = begin_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM tasks")
    rows = c.fetchall()
    conn.close()
    return rows

def per_second_value(x): 
    return x[1]


calendar_options = {
    "editable": True,
    "selectable": True,
    "headerToolbar": {
        "left": "today prev,next",
        "center": "title",
        "right": "resourceTimelineDay,resourceTimelineWeek,resourceTimelineMonth",
    },
    "slotMinTime": "06:00:00",
    "slotMaxTime": "18:00:00",
    "initialView": "resourceTimelineDay",
    "resource": "of",
#{"id": "a", "building": " A", "title": "Building A"},
     #   {"id": "b", "building": "Building A", "title": "Building B"},
      #  {"id": "c", "building": "Building B", "title": "Building C"},
      #  {"id": "d", "building": "Building B", "title": "Building D"},
       # {"id": "e", "building": "Building C", "title": "Building E"},
      #  {"id": "f", "building": "Building C", "title": "Building F"},
    
}
events_to_add = [
    
]

custom_css = """
    .fc-event-past {
        opacity: 0.8;
    }
    .fc-event-time {
        font-style: italic;
    }
    .fc-event-title {
        font-weight: 700;
    }
    .fc-toolbar-title {
        font-size: 2rem;
    }
"""

conn = begin_connection()
c = conn.cursor()

st.title("Here's your Schedule for Today") 
top_priority = c.execute("SELECT task FROM tasks WHERE priority =5 AND category != 'Physiological' ")
st.write("Priorities = ", *top_priority)

info = c.execute("Select * FROM tasks")
tasks_df = pd.DataFrame(info.fetchall(), columns=['task', 'due_time', 'due_date', 'duration', 'category', 'priority'])
#st.write(tasks_df)

db_rep = tasks_df.to_dict(orient='index') # takes data from sqlite table and puts in representable form  
#st.write(db_rep)
events_with_calculated_priority = []

#st.write(db_rep["due_time"])
# #calculation of the time it takes for each task  -> get all events + their score -> largest score = most important
for task_index, task_info in db_rep.items():
    get_dtime = db_rep[task_index]["due_time"]
  #  st.write(get_dtime)
    dtime = get_dtime.split(":")
    due_hours = int(dtime[0]) #set hour at which task is due  hourse
    due_minutes = int(dtime[1]) # set minutes when task is due  minutes 
    due_total_min = due_hours * 60 + due_minutes #was called total_due 

    get_required_time = db_rep[task_index]["duration"]
   # st.write(get_required_time)
    required_time = get_required_time.split(":")
    required_hours = int(required_time[0])
    required_minutes = int(required_time[1])
    total_duration = required_hours * 60 + required_minutes
     
    priority_score = db_rep[task_index]["priority"]
  #  st.write(priority_score)
    priority_sum = due_total_min + total_duration + priority_score 
    events_with_calculated_priority.append([task_index, priority_sum]) #_> [0, 99]
    events_with_calculated_priority.sort(reverse=True, key= per_second_value) 

#     #sorted_priorities = sorted(events_with_calculated_priority(reverse = True))
#     # not necessary : st.write(events_with_calculated_priority)

time_passed = 0 #no time has passed YET

for i in events_with_calculated_priority:
    add_to_cal = {}
    add_to_cal["title"] = db_rep[i[0]]['task'] 
    add_to_cal["start_time"] = (datetime.now() + timedelta(minutes=time_passed, seconds=0)).strftime("%Y-%m-%dT%H:%M:%S") #format for calendar event
    hours, minutes = map(int, db_rep[i[0]]["duration"].split(":"))
    time_passed += (hours*60 + minutes)
    add_to_cal["end"] = (datetime.now() + timedelta(minutes=time_passed, seconds=0)).strftime("%Y-%m-%dT%H:%M:%S")
    add_to_cal["resourceId"] = "a"


display = calendar(events= events_with_calculated_priority, options=calendar_options, custom_css=custom_css)



#events_with_calculated_priority.append(add_to_cal)
#st.write(add_to_cal)

# timeadd = 0
# for i in events_with_calculated_priority:
#     #print(number1[i[0]]["task"])
#     addtocalendarevents = {}
#     addtocalendarevents["title"] = db_representation[i[1]]["task"]
#     #print(number1[i[0]])
#     #print(i)
#     #print(addtocalendarevents["title"])
#     addtocalendarevents["start"] = (datetime.now() + timedelta(hours=0, minutes=timeadd, seconds=0)).strftime("%Y-%m-%dT%H:%M:%S")
#     hoursz, miniutesz = map(int, db_representation[i[0]]["duration"].split(":"))
#     timeadd += (hoursz*60 + miniutesz)
#     addtocalendarevents["end"] = (datetime.now() + timedelta(hours=0, minutes=timeadd, seconds=0)).strftime("%Y-%m-%dT%H:%M:%S")
#     addtocalendarevents["resourceId"] = "a"
#     events_with_calculated_priority.append(addtocalendarevents)



#START OF ORIGINAL CODE 

# number1 = tasks_df.to_dict(orient='index')

# parsed_tasks = []

#for idx, task_info in number1.items():
   # partsd = task_info["due_time"].split(":")
  #  hoursd = int(partsd[0])
  #  minutesd = int(partsd[1]) 
  #  total_due = hoursd * 60 + minutesd

   # partse = task_info["duration"].split(":")
   # hourse = int(partse[0])
    #  minutese = int(partse[1])
     #total_duration = hourse * 60 + minutese

    # priority = task_info["priority"]

   # total_value = total_due + total_duration + priority

  #  parsed_tasks.append([idx, total_value])

# parsed_tasks.sort(key=lambda x: x[1])
# reverse this bcs we're sorting this from least priority to most priority, you shoudl sort from most priority to least priiority 


 # timeadd = 0
#for i in parsed_tasks:
   # print(number1[i[0]]["task"])
#    addtocalendarevents = {}
  #  addtocalendarevents["title"] = number1[i[0]]["task"]
   # print(number1[i[0]])
    #print(i)
   # print(addtocalendarevents["title"])
  #  addtocalendarevents["start"] = (datetime.now() + timedelta(hours=0, minutes=timeadd, seconds=0)).strftime("%Y-%m-%dT%H:%M:%S")
  #  hoursz, miniutesz = map(int, number1[i[0]]["duration"].split(":"))
  #  timeadd += (hoursz*60 + miniutesz)
   # addtocalendarevents["end"] = (datetime.now() + timedelta(hours=0, minutes=timeadd, seconds=0)).strftime("%Y-%m-%dT%H:%M:%S")
   # addtocalendarevents["resourceId"] = "a"
    #events_with_calculated_priority.append(addtocalendarevents)



