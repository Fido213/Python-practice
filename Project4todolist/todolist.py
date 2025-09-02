import json
import uuid
from datetime import datetime
import questionary
from prompt_toolkit.styles import Style  # this is for styling prompts


def start_dictionary():
    # this function is purely as a failsafe to restart and update
    # the dictionary format
    status = {
        "done": {},
        "unfinished": {},
        "pending": {},
    }
    # This is a dictionary, the key is the status
    # its value is a another set of nested dictionaries
    # containing uuid, date and task as strings to the keys
    return status


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
                print("\n System:")
                print("File is empty")
                status = start_dictionary()
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
        print("\n System:")
        print("Memory file not found/Error decoding it, creating a new one.")
        status = start_dictionary()
        return status
        # if the file is not found, create a new dictionary


def update_memory(data):
    with open('Project4todolist/memory.json', 'w') as file:
        # write mode also creates the file if it does not exist
        # so this basically sets up error avoidance and makes it up
        # by creating the file later whilst reseting the dictionary
        # sets a context manager to open the file in write mode
        # (this also makes it so that it closes automatically)
        # memory.json is saved as "file"
        json.dump(data, file, indent=4)
        # json.dump is used to basically takes the dictionary and writes
        # it in json format in the file (memory.json)
        # indent 4 is to make it human readable


# def reverse_map(task):


def sanitise_function():
    # this function is for clearing out bad data
    status = read_memory()
    seen_tasks = set()
    for status_verification in status:
        for task_dictionary in status[status_verification].values():
            task_to_compare = task_dictionary.get("Task").strip()
            if task_to_compare in seen_tasks:
                print("\n System:")
                print(f"'{task_to_compare}' in '{status_verification}' is a duplicate, deleting...")
            else:
                seen_tasks.add(task_to_compare)
                print("\n System:")
                print("Stable")


def get_user_input():
    while True:
        # this function is only used for the "add" functionality
        userinput = input("Enter status and task name in order: ")
        # get the user input and then split it into status and task name
        try:
            split_input = userinput.split(" ", 1)
            print(split_input)
            # assign a variable to the status
            status_input = split_input[0].lower()  # convert the status to lowercase
            task_inputsplit = split_input[1:]  # assign a variable to the task
            # the 1: is like in excel where u select a range of cells from a
            # certain index
            task_input = ' '.join(task_inputsplit)   # join the list into a string
            if not task_input:
                print("Put a task after the status")
            else:
                return status_input, task_input  # return the status and task input
        except (TypeError):
            print("Can't add non-iterable object (such as nothing)")
            break


def add_task(INPstatus, task_input):
    status = read_memory()
    # get status from read_memory function
    if INPstatus in status:
        unique_id = str(uuid.uuid4())
        current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        task_to_add = {
            "UUID": unique_id,
            "Date": current_date,
            "Task": task_input
        }
        # since the new format is dictionaries inside dictionaries
        # ill have to add a new key, same with the append function
        # ill add a new key (inside the dictionary) and its valuew would be
        # task_to_add
        # generate a unique id for the task using uuid4
        status[INPstatus][unique_id] = task_to_add
        # INP status is the paramater that is passed to the function,
        # the INPstatus is the status_input that is passed to the function
        # if INPStatus is found in the dictionary status,
        # datetime.now().strftime is used to format the date and time
        # to a more human readable format
        update_memory(status)
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
            if not status[status_input]:
                print(f"No tasks in {status_input}")
            else:
                for task_overview in status[status_input].values():
                    # the .values makes it so i can see an overview of the
                    # dictionary
                    # since status[status_input] = dictionary, python goes to
                    # the dictionary
                    # then inside the dictionary it shows an overview, since
                    # inside the dictionary is just {uuid{task data}}, the
                    # .values makes it
                    # so i see only {task data} (since tatus[status_input] =
                    # dictionary
                    # , that means when i type status[done], i get the
                    # dictionary then
                    # i can call .values to get only the values of the
                    # dictionary which
                    # is the task data), i would then use .get to get a value
                    # from a key
                    # which is task, and assign it to a variable, so i can then
                    #  print it
                    task_to_view = task_overview.get("Task", "Couldnt find task")
                    print(f"- {task_to_view}")
        elif status_input == 'exit':
            print("Exiting view tasks.")
            break
        else:
            print("Invalid status. Please enter 'done', 'unfinished', 'pending'"\
                  ", or 'exit' to quit.")


def remove_task():
    status = read_memory()  # get memory from read_memory function
    status_input = input("\nEnter status to delete task from (done, unfinished, pending)"
                         ",\nType exit to quit deleting: ").lower()
    # get the user input and convert it to lowercase

    if status_input in status:
        if not status[status_input]:
                print(f"No tasks in {status_input}")
        else:
            print(f"\n Pick a task to remove from '{status_input}' list:")
            list_to_show = []
            # creates an empty list to get all the choices from our
            # for loop which goes through each dictionary value (through .values)
            # and gets the value of the key task, which then appends it to the list
            # this makes it easy for me to do a questionary.select with the choices
            # as the variable which is a list, then i do default=list_to_show[0]
            # to make it so that the first task is highlighted
            # i also add a failcheck for if they dont contain anything so it wont
            # highlight, i also seperated options and answers, so options
            # only contains the actual select list whilst answers
            # contains the .ask(), this allows me to change the questions
            # whilst keeping the core code intact
            for task_overview in status[status_input].values():
                task_to_Show = task_overview.get("Task", "Couldnt find task")
                list_to_show.append(task_to_Show)
            custom_style = Style([
                 ("qmark", "fg:#ff9d00 bold"),  # question mark colour
                 (("pointer", "fg:#000000")),  # pointer colour
                 ("highlighted", "bg:#ffffff fg:#000000"),  # highlight color
                    ])
            options = questionary.select("Choose a task:",
                                         choices=list_to_show,
                                         style=custom_style)
            answer = options.ask()
            print(f"Removing task: {answer}")
    elif status_input == 'exit':
        print("Exiting remove tasks.")


def terminal_interface():
    user_input = input("\n add \n view \n remove \n update \n exit \n Type input: ").lower()
    return user_input


# Main program loop
while True:
    print("\n ----- Todo List Terminal Interface -----"
          "\nYou can add tasks with 'add', view tasks with 'view', "
          "remove tasks with 'remove', update tasks with 'update' "
          "or exit with 'exit'.")
    sanitise_function()
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
    elif user_input == 'remove':
        remove_task()
