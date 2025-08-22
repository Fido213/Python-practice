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

current_date = datetime.now()  # defining the current date and time


def get_user_input():
    userinput = input("Enter status and task name in order ")
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
    try:
        with open('Project4todolist/memory.json', 'r') as file:
            # set a context manager to open the file in read mode
            # this will let me check old memoery as to not overide it
            memory_check = file.read()
            # turn the file.read into a variable so i can use it outside
            # the with open statement
            # file.read() basically reads everything
            # then we run a if not check, if the file is empty
            # it will be true, if not, it will continue to the else statement
            if not memory_check:
                print("File is empty")
                status = {
                    "done": [],
                    "unfinished": [],
                    "pending": []
                }
                # if the file is empty, create a new dictionary with empty lists
                # for each status
            else:
                # now since reading a file basically puts a "cursor"
                # (in this case its at the end)
                # python will try to load the file from the end which will
                # result in our deocde error, so we reset the cursor
                file.seek(0)
                # seek(0) basically resets the cursor to the start of the file
                # this will let out json.load work properly and load the whole file
                status = json.load(file)
                # load the json data (dictionary in json format) into the
                # python dictionary status, this basically updates the status
                # dictionary
    except (FileNotFoundError, json.JSONDecodeError):
        print("Memory file not found/Error decoding it, creating a new one.")
        status = {
            "done": [],
            "unfinished": [],
            "pending": []
        }
        # if the file is not found, create a new dictionary
    if INPstatus in status:
        status[INPstatus].append(task_input + ": " + current_date.strftime("%Y-%m-%d %H:%M:%S"))
        # append the task to the list of the status
        # INP status is the paramater that is passed to the function,
        # the INPstatus is the status_input that is passed to the function
        # if INPStatus is found in the dictionary status,
        # the task input is then appended to the list of the
        # corresponding status
        # current_date.strftime is used to format the date and time
        # to a more human readable format
        with open('Project4todolist/memory.json', 'w') as file:
            # write mode also creates the file if it does not exist
            # so this basically sets up error avoidance and makes it up
            # by creating the file later whilst reseting the dictionary
            # sets a context manager to open the file in write mode
            # (this also makes it so that it closes automatically)
            # memory.json is saved as "file"
            json.dump(status, file, indent=4)
            # json.dump is used to basically takes the dictionary and writes
            # it in json format in the file (memory.json)
            # indent 4 is to make it human readable
        print(f"Task '{task_input}' added to '{INPstatus}' list at {current_date}.")
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
