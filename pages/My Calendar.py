import streamlit as st
import sqlite3
import pandas as pd
import os  
from streamlit_calendar import calendar
from datetime import datetime, timedelta

#Page Title
st.title("Here's your Schedule for Today") 

#Creation of function that connect to tasks database, as well as add events to it and display them 
# The function per_second_value is used to select the second element of the parameter, which later is used for a dictionary 

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

#The following is code from the streamlit-calendar module and is used to display a calendar 
calendar_options = {
    "editable": True,
    "selectable": True,
    "headerToolbar": {
        "left": "today,prev,next",
        "center": "title",
        "right": "resourceTimelineDay,resourceTimelineWeek,resourceTimelineMonth",
    },
    "slotMinTime": "06:00:00",
    "slotMaxTime": "22:00:00",
    "initialView": "resourceTimelineDay",
    "resourcesGroupField": "building", 
    "resources": [
    {"id": "a", "building": " A", "title": "Building A"},
    {"id": "b", "building": "Building A", "title": "Building B"},
    {"id": "c", "building": "Building B", "title": "Building C"},
    {"id": "d", "building": "Building B", "title": "Building D"},
    {"id": "e", "building": "Building C", "title": "Building E"},
    {"id": "f", "building": "Building C", "title": "Building F"},
    ]
}

calendar_resources = [
        {"id": "a", "building": "Building A", "title": "Room A"},
        {"id": "b", "building": "Building A", "title": "Room B"},
        {"id": "c", "building": "Building B", "title": "Room C"},
        {"id": "d", "building": "Building B", "title": "Room D"},
        {"id": "e", "building": "Building C", "title": "Room E"},
        {"id": "f", "building": "Building C", "title": "Room F"},
    ]

events = []

calendar_options = {
        "editable": True,
        "navLinks": True,
        "resources": calendar_resources,
        "selectable": True,
    }

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

mode = st.selectbox(
       "Calendar Mode:",
       (
           "daygrid",
           "timegrid",
           "timeline",
           "resource-daygrid",
           "resource-timegrid",
           "resource-timeline",
           "list",
           "multimonth",
       ),
   )


calendar_options = {
        "editable": True,
        "navLinks": True,
        "resources": calendar_resources,
        "selectable": True,
    }

if "resource" in mode:
        if mode == "resource-daygrid":
            calendar_options = {
                **calendar_options,
                "initialDate": "2025-01-01", 
                "initialView": "resourceDayGridDay",
                "resourceGroupField": "building",
            }
        elif mode == "resource-timeline":
            calendar_options = {
                **calendar_options,
                "headerToolbar": {
                    "left": "today, prev,next",
                    "center": "title",
                    "right": "resourceTimelineDay,resourceTimelineWeek,resourceTimelineMonth",
                },
                "initialDate": "2025-01-01",
                "initialView": "resourceTimelineDay",
                "resourceGroupField": "building",
            }
        elif mode == "resource-timegrid":
            calendar_options = {
                **calendar_options,
                "initialDate": "2025-01-01",
                "initialView": "resourceTimeGridDay",
                "resourceGroupField": "building",
            }
else:
        if mode == "daygrid":
            calendar_options = {
                **calendar_options,
                "headerToolbar": {
                    "left": "today, prev,next",
                    "center": "title",
                    "right": "dayGridDay,dayGridWeek,dayGridMonth",
                },
                "initialDate": "2025-01-01",
                "initialView": "dayGridMonth",
            }
        elif mode == "timegrid":
            calendar_options = {
                **calendar_options,
                "initialView": "timeGridWeek",
            }
        elif mode == "timeline":
            calendar_options = {
                **calendar_options,
                "headerToolbar": {
                    "left": "today, prev,next",
                    "center": "title",
                    "right": "timelineDay,timelineWeek,timelineMonth",
                },
                "initialDate": "2025-01-01",
                "initialView": "timelineMonth",
            }
        elif mode == "list":
            calendar_options = {
                **calendar_options,
                "initialDate": "2025-01-01",
                "initialView": "listMonth",
            }
        elif mode == "multimonth":
            calendar_options = {
                **calendar_options,
                "initialView": "multiMonthYear",
            }

#Establish a connection to the 'tasks' database
conn = begin_connection()
c = conn.cursor()

#Select all data from 'tasks'
info = c.execute("Select * FROM tasks")

#Convert data into a pandas dataframe
tasks_df = pd.DataFrame(info.fetchall(), columns=['task', 'due_time', 'due_date', 'duration', 'category', 'priority', 'resource_id'])

#Convert dataframe into a dictionary, taking data from sqlite table and putting it in a form that can be displayed and more easily manipulated with python
db_rep = tasks_df.to_dict(orient='index')  
#Create a list to store events with their corresponding priorities 
events_with_calculated_priority = []



# Calculation of the importance of each task  -> based on due_time, time it takes, and priority score  -> largest score = most important

for task_index, task_info in db_rep.items():
    
    #Calculation of the due time required for the task as a sum of total minutes, which is to be used in the calculation of the score 
    get_dtime = db_rep[task_index]["due_time"]
    dtime = get_dtime.split(":") 
    due_hours = int(dtime[0]) #Get the hour 
    due_minutes = int(dtime[1]) # Get the minutes
    due_total_min = due_hours * 60 + due_minutes 

    #Calculation of the total required time for task completion in minutes
    get_required_time = db_rep[task_index]["duration"]
    required_time = get_required_time.split(":")
    required_hours = int(required_time[0])
    required_minutes = int(required_time[1])
    total_duration = required_hours * 60 + required_minutes
     
    #Get priority score for task 
    priority_score = db_rep[task_index]["priority"]

    #Sum all integers together to get priority score
    priority_sum = due_total_min + total_duration + priority_score 

    events_with_calculated_priority.append([task_index, priority_sum]) #Add each task and its associated value to events_with_calculated_priority
    events_with_calculated_priority.sort(reverse=True, key= per_second_value)
    #Sort tasks in reverse order, as .sort() method sorts in asending order, but the reverse sorts it in descending order with the largest value going first 
    #The key 'per_second_value' indicates that items should be sorted based on their score and not the event index  -> the value at the first index of the list

#Next, the time necessary for each event will be calculated

#Determines that the sorting of items will begin from the present moment 
time_passed = 0 

output = []
events_list = []


#Used to create a dictionary (add_to_cal) that is to be stored in a list (events_list) and then displayed
#Each event has a associated title, start time, end time, and resource id -> resource id is used connect inputed information and to display it as an event on the calendar
for key in events_with_calculated_priority:
    add_to_cal = {}
    add_to_cal["title"]= db_rep[key[0]]['task'] #Get the name of a task from db_rep dictionary
    add_to_cal["start"] = (datetime.now() + timedelta(minutes=time_passed, seconds=0)).strftime("%Y-%m-%dT%H:%M:%S") #Get current time and time_passed, then format to year/month/day/hour/minute/second for calendar compatibility
    hours, minutes = map(int, db_rep[key[0]]["duration"].split(":")) # take and store duration as integer variables: hours and minutes
    time_passed += (hours*60 + minutes) #Update time passed with calculated values
    add_to_cal["end"] = (datetime.now() + timedelta(minutes=time_passed, seconds=0)).strftime("%Y-%m-%dT%H:%M:%S") 
    add_to_cal["resourceId"] = db_rep[key[0]]['resource_id']
    events.append(add_to_cal) 





#Display the events in a calendar using the calendar function and inputting the according parameters
display = calendar(events= events, options=calendar_options, custom_css=custom_css, key = f"calendar_{mode}")
