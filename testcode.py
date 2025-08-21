import json
import uuid
from datetime import datetime


status = {
    "done": [],
    "unfinished": [],
    "pending": [],
    }
# This is a dictionary, the key is the status and its value is a list in which
# tasks will be appended to


def read_data(filename):
    try:
        with open(filename, 'r') as file:  # open the file in read mode
            saveddata = json.load(file)
            # load the json data into python objects
            print(f"Data read from '{filename}': {saveddata}")
            # debugging line
            return saveddata  # returns the data for another funciton
    except FileNotFoundError:
        print(f"File '{filename}' not found.")
        return None
    except json.JSONDecodeError:
        print(f"Error decoding JSON from file '{filename}'.")
        return None


def append_data(filename, data):
    saveddata = read_data(filename)
    # read the data from the file in the previous function
    saveddata.append(data)  # append the data to the list
    try:
        with open(filename, 'w') as file:  # open the file in write mode
            json.dump(data, file, indent=4)
            # dump the data into the file in json format
            print(f"Data written to '{filename}': {data}")  # debugging line
    except IOError as e:
        print(f"Error writing to file '{filename}': {e}")
        return None


def get_user_input():
    userinput = input("Enter status and task name in order")
    # get the user input and then split it into status and task name
    split_input = userinput.split(" ", 1)
    print(split_input)
    # assign a variable to the status
    status_input = split_input[0].lower()  # convert the status to lowercase
    task_inputsplit = split_input[1:]  # assign a variable to the task
    # the 1: is like in excel where u select a range of cells from a
    # certain index
    task_input = ' '.join(task_inputsplit)   # join the list into a string
    # simplifies the task name aswell as going from list to string
    return status_input, task_input  # return the status and task input


def check_task(INPstatus, task_input):
    if INPstatus in status:
        saveddata = read_data('testcode.json')
        status[INPstatus].append(task_input)
        # append the task to the list of the status
        # INP status is the paramater that is passed to the function,
        # the INPstatus is the status_input that is passed to the function
        # if INPStatus is found in the dictionary status,
        # the task input is then appended to the list of the
        # corresponding status
        print(f"Task '{task_input}' added to '{INPstatus}' list.")
        print(f"Current '{INPstatus}' list: {status[INPstatus]}")
    else:
        print("Invalid status. Please enter 'done', 'unfinished', or 'pending'.")


# Main program loop
print("Welcome to the To-Do List Manager!")
while True:
    # loop to allow the user to enter multiple tasks (debug too)
    if input("do you want to add another task? (yes/no): ").lower() != 'yes':
        break
    else:
        status_input, task_input = get_user_input()
        # get the user input and assign it to the status_input and task_input
        check_task(status_input, task_input)