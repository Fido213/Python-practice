import json
import uuid
from datetime import datetime
import questionary
from prompt_toolkit.styles import Style  # this is for styling prompts

# custom style for usage throughout the code
custom_style = Style([
                 ("qmark", "fg:#ff9d00 bold"),  # question mark colour
                 (("pointer", "fg:#000000")),  # pointer colour
                 ("highlighted", "bg:#ffffff fg:#000000"),  # highlight color
                    ])
reverse_memory_Cache = {}  # global caching place, deletes on exit


def start_dictionary():
    # this function is purely as a failsafe to restart and update
    # the dictionary format
    status = {
        "finished": {},
        "pending": {},
        "unfinished": {},
    }
    # This is a dictionary, the key is the status
    # its value is a another set of nested dictionaries
    # containing uuid, date and task as strings to the keys
    return status


def read_memory():
    Memory_is_empty = False
    Memory_not_found_or_error = False
    Memory_found = "found"
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
                print("\n System: \n - File is empty")
                Memory_is_empty = True
                status = start_dictionary()
                # if the file is empty, create a new dictionary with empty
                # lists for each status
                return status, Memory_is_empty
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
                return status, Memory_found
    except (FileNotFoundError, json.JSONDecodeError):
        print("\n System: \n - Memory file not found/Error decoding it, creating a new one.\n")
        status = start_dictionary()
        Memory_not_found_or_error = True
        return status, Memory_not_found_or_error
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


def update_memory_reverse(data):
    with open('Project4todolist/reverse_memory.json', 'w') as file:
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


def initialise_reverse_map():
    status, _ = read_memory()  # get the current normal memory
    reverse_dictionary = {}  # prepare an empty dic to populat in reverse
    for nested_status in status.values():
        # in status variable (its a dict) we go through each
        # key (done unfinished and pending) assign it to nested_status
        # then in the loop below we get the .values (since the value of that
        # key is a dictionary) to get the task details
        # then its a simple .get
        for outer_task_overview in nested_status.values():
            # basically, the values inside the status input inside the
            # big dict status, assign a temp variable
            # named outer_task_overview, then assign the task (values)
            # using the .get to the variable task name, same with UUID
            # then reverse via normal dict assignment
            # i then save it to a json for ease of access
            task_name = outer_task_overview.get("Task")
            uuid_id = outer_task_overview.get("UUID")
            if uuid_id and task_name:
                reverse_dictionary[task_name] = uuid_id
    update_memory_reverse(reverse_dictionary)


def reverse_memory_read():
    try:
        with open('Project4todolist/reverse_memory.json', 'r') as file:
            # set a context manager to open the file in read mode
            reverse_map = json.load(file)
            return reverse_map
    except (FileNotFoundError, json.JSONDecodeError):
        print("\n System:")
        print("Error opening reverse map. initialising new one")
        initialise_reverse_map()
        return reverse_map


def reverse_memory_cache():
    global reverse_memory_Cache
    reverse_map = reverse_memory_read()
    for reverse_cache_keys, reverse_cache_values in reverse_map.items():
        reverse_memory_Cache[reverse_cache_keys] = reverse_cache_values


def update_reverse_memory_cache(task, uuidvalue):
    reverse_memory_Cache[task] = uuidvalue


def sanitise_function():
    # this function is for clearing out bad data
    status, _ = read_memory()
    seen_tasks = set()
    tasks_to_delete = []
    # since i cant update and delete at runtime, it gives an error
    # so i assign it to a list and then delete it at the end of the loop
    reverse_map = reverse_memory_read()
    # ill add a check to see if theres any duplicates
    # to print the "stable" in the else
    duplicate = False  # this is to check later to print stable or not
    for status_verification in status:
        for task_dictionary in status[status_verification].values():
            task_to_compare = task_dictionary.get("Task").strip()
            if task_to_compare in seen_tasks:
                print("\n System:")
                print(f"'{task_to_compare}' in '{status_verification}' is a duplicate, deleting...\n")
                duplicate = True
                reverse_uuid = reverse_map[task_to_compare]  # reverse mapping
                # i get the uuid by going to the reverse map dictionary, and since
                # tasks are the keys and the values uuid, i can just input the task_tocompare
                # since ill get the uuid value from that key
                tasks_to_delete.append((reverse_uuid, status_verification))
            else:
                seen_tasks.add(task_to_compare)
    if not duplicate and _ == "found":
        print("\n System:\n - Stable \n")
    if tasks_to_delete:
        for uuid_value, status_key in tasks_to_delete:
            # here since i appended in () im basically unpacking
            # a tuple
            try:
                del status[status_key][uuid_value]
                update_memory(status)
            except (KeyError):
                print("\n System:")
                print("Error deleting/finding the uuid and task.")
    update_memory(status)
    


def get_user_input():
    status, _ = read_memory()
    while True:
        # this function is only used for the "add" functionality
        # utilise questionarily to choose visually the status, removing needs for splitting
        # aswell as facilitating ux
        status_choices = questionary.select("Select a status:",
                                            choices=status.keys(),
                                            style=custom_style
                                            )
        status_input = status_choices.ask()
        try:
            task_input = input("Input task ")
            return status_input, task_input
        except (TypeError):
            print("Can't add non-iterable object (such as nothing)")
            break


def add_task(INPstatus, task_input):
    status, _ = read_memory()
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
        print("Invalid status. Please enter 'finished', 'unfinished', or 'pending'.")


def view_tasks():
    status, _ = read_memory()  # get memory from read_memory function
    while True:
        status_input = questionary.select("\nEnter status to view (finished, unfinished, pending)"
                                          ",\nPress Control + C to exit:",
                                          choices=status.keys(),
                                          style=custom_style).ask()
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
        elif status_input is None:
            print("Exiting view tasks.")
            break


def remove_task():
    status, _ = read_memory()  # get memory from read_memory function
    reverse_map = reverse_memory_read()
    # get the user input and convert it to lowercase
    while True:
        status_input = questionary.select("\n Select status to delete task from (finished, unfinished, pending)"
                                          ",\nHit Control + C to exit: ",
                                          choices=status.keys(),
                                          style=custom_style).ask()
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
                # as the variable which is a list
                # i also add a failcheck for if they dont contain anything so it wont
                # highlight, i also seperated options and answers, so options
                # only contains the actual select list whilst answers
                # contains the .ask(), this allows me to change the questions
                # whilst keeping the core code intact
                for task_overview in status[status_input].values():
                    task_to_Show = task_overview.get("Task", "Couldnt find task")
                    list_to_show.append(task_to_Show)
                options = questionary.select("Choose a task:",
                                             choices=list_to_show,
                                             style=custom_style)
                answer = options.ask()
                confimration = input("Are you sure? Y/N ").upper()
                if confimration == "Y":
                    try:
                        reverse_uuid = reverse_map[answer]
                        del status[status_input][reverse_uuid]
                        update_memory(status)
                        print(f"Removing task: {answer}")
                    except (KeyError):
                        print("\n System: \n Error deleting/finding the uuid and task.")
                else:
                    print("\n System: \nCanceling deletion")
                    break
                if answer is None:
                    print("\n System: \n exiting task deletion.")
                    break
        elif status_input is None:
            print("\n System: \n exiting task deletion.")
            break


def update_task():
    status, _ = read_memory()
    reverse_map = reverse_memory_read()
    tasks_to_update = []
    status_to_show = set(status.keys())
    while True:
        status_input = questionary.select("\nSelect status to update (finished, unfinished, pending)"
                                          ",\nPress Control + C to exit:",
                                          choices=status.keys(),
                                          style=custom_style).ask()
        # get the user input and convert it to lowercase
        if status_input in status:
            if not status[status_input]:  # quick check if its empty
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
                    task_to_update = task_overview.get("Task", "Couldnt find task")
                    tasks_to_update.append(task_to_update)
                tasks_choices = questionary.select(
                    f"\n Pick a task in '{status_input}' to update:",
                    choices=tasks_to_update,
                    style=custom_style
                )
                update_answer = tasks_choices.ask()
                try:
                    reverse_uuid = reverse_map[update_answer]  # get the mapped uuid
                except (KeyError):
                    "Cancelling update"
                    break
                if status_input in status_to_show:
                    status_to_show.remove(status_input)
                status_to_go = questionary.select(
                    "Select a status to update to",
                    choices=status_to_show,
                    style=custom_style
                ).ask()
                print(f"\n Updating '{update_answer}' from '{status_input}' to '{status_to_go}'...")
                print(f"Attempting to delete original '{update_answer}' in '{status_input}'...")
                try:
                    task_data_to_update = status[status_input][reverse_uuid]
                    del status[status_input][reverse_uuid]
                    print("Deleting...")
                    status[status_to_go][reverse_uuid] = task_data_to_update
                    update_memory(status)
                except (KeyError):
                    print("\n System: \n Error deleting/finding the uuid and task.")
                break
        elif status_input is None:
            print("Exiting update tasks.")
            break


def terminal_interface():
    choices = ["add", "view", "remove", "update", "exit"]
    user_choices = questionary.select(
        "(Arrow keys are utilised throughout the cli)",
        choices=choices,
        style=custom_style
    )
    user_input = user_choices.ask()
    return user_input


# Main program loop
initialise_reverse_map()
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
    elif user_input == "update":
        update_task()
    elif user_input is None:
        print("Exiting the todo list terminal interface.")
        break
