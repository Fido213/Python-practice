import json
import uuid
from datetime import datetime
import inquirer


status = {
    "done": [],
    "unfinished": [],
    "pending": [],
    }
# This is a dictionary, the key is the status and its value is a list in which
# tasks will be appended to


def read_memory():
    try:
        with open('Project4todolist/memory.json', 'r') as file:
            # set a context manager to open the file in read mode
            # this will let me check old memoery as to not overide it
            memory_check = file.read()
            # turn the file.read into a variable so its simpler to use
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
                # if the file is empty, create a new dictionary with empty
                # lists for each status
                return status
            # return the status dictionary in all 3 cases of the function for
            # later usage by other functions
            else:
                # now since reading a file basically puts a "cursor"
                # (in this case its at the end)
                # python will try to load the file from the end which will
                # result in our deocde error, so we reset the cursor
                file.seek(0)
                # seek(0) basically resets the cursor to the start of the file
                # this will let json.load work properly and load the whole file
                status = json.load(file)
                # load the json data (dictionary in json format) into the
                # python dictionary status, this basically updates the status
                # dictionary
                return status
    except (FileNotFoundError, json.JSONDecodeError):
        print("Memory file not found/Error decoding it, creating a new one.")
        status = {
            "done": [],
            "unfinished": [],
            "pending": []
        }
        return status
        # if the file is not found, create a new dictionary


def get_user_input():
    # this function is only used for the "add" functionality
    userinput = input("Enter status and task name in order: ")
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


def add_task(INPstatus, task_input):
    status = read_memory()
    # get status from read_memory function
    if INPstatus in status:
        status[INPstatus].append(task_input + ": " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        # append the task to the list of the status
        # INP status is the paramater that is passed to the function,
        # the INPstatus is the status_input that is passed to the function
        # if INPStatus is found in the dictionary status,
        # the task input is then appended to the list of the
        # corresponding status
        # datetime.now().strftime is used to format the date and time
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
        print(f"Task '{task_input}' added to '{INPstatus}' list at {datetime.now()}.")
        # print(f"Current '{INPstatus}' list: {status[INPstatus]}")
        # this is used for debugging purposes
    else:
        print("Invalid status. Please enter 'done', 'unfinished', or 'pending'.")


def view_tasks():
    status = read_memory()  # get memory from read_memory function
    while True:
        status_input = input("\nEnter status to view (done, unfinished, pending)"
                             ",\nType exit to quit viewing: ").lower()
        # get the user input and convert it to lowercase
        if status_input in status:
            print(f"\n Tasks in '{status_input}' list:")
            for task in status[status_input]:
                print(f"- {task.split(':')[0]}")  # Print only the part before the
                # colon the [0] is an index to get only the first part of the split
                # string (via the .split function and precising that its split
                # from the ":")
                # i also use a for loop to loop through all the tasks, and the
                # print function makes it so that its a new line for each task
        elif status_input == 'exit':
            print("Exiting view tasks.")
            break
        else:
            print("Invalid status. Please enter 'done', 'unfinished', 'pending'"\
                  ", or 'exit' to quit.")


def terminal_interface():
    user_input = input("\n add \n view \n remove \n update \n exit \n Type input: ").lower()
    return user_input


# Main program loop
while True:
    print("\n ----- Todo List Terminal Interface -----"
          "\nYou can add tasks with 'add', view tasks with 'view', "
          "remove tasks with 'remove', update tasks with 'update' "
          "or exit with 'exit'.")
    # loop to allow the user to enter multiple tasks (debug too)
    user_input = terminal_interface()
    # get the user input and assign it to the user_input variable
    if user_input == 'exit':
        print("Exiting the todo list terminal interface.")
        break
    elif user_input == 'add':
        status_input, task_input = get_user_input()
        # get the user input and assign it to the status_input and task_input
        add_task(status_input, task_input)
    elif user_input == 'view':
        view_tasks()
