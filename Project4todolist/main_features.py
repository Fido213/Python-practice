import uuid
from datetime import datetime
import questionary
import reverse_memory_family
import memory_management_family
import cli_interface
from cli_interface import custom_style
# this file contains the main features of the todo list terminal interface
# such as adding, viewing, removing and updating tasks


def get_user_input():
    status, _ = memory_management_family.read_memory()
    while True:
        # this function is only used for the "add" functionality
        # utilise questionarily to choose visually the status, removing needs for splitting
        # aswell as facilitating ux
        status_choices = questionary.select("Select a status:",
                                            choices=status.keys(),
                                            style=custom_style
                                            )
        status_input = status_choices.ask()
        if status_input is None:
            print("\n System: \n Exiting add task.")
            break
        try:
            task_input = input("Input task ")
            if not task_input:
                error_message = cli_interface.system_message("no character")
                print(error_message)
            else:
                return status_input, task_input
        except KeyboardInterrupt:
            print("\n System: \n Exiting add task.")
            break
        except Exception as e:
            error_message = cli_interface.system_message("error")
            print(f"{error_message} '{e}'")
            break


def check_task_exists(task):
    status, _ = memory_management_family.read_memory()
    for nested_status in status.values():
        for task_overview in nested_status.values():
            task_to_check = task_overview.get("Task", "")
            if task == task_to_check:
                return "Duplicate"
    return "Unique"


def add_task(INPstatus, task_input):
    status, _ = memory_management_family.read_memory()
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
        memory_management_family.update_memory(status)
        reverse_memory_family.update_reverse_memory_cache(task_input, unique_id)
        print(f"Task '{task_input}' added to '{INPstatus}' list at {datetime.now()}.")
        # print(f"Current '{INPstatus}' list: {status[INPstatus]}")
        # this is used for debugging purposes
    else:
        error_message = cli_interface.system_message("invalid")
        print(error_message)


def view_tasks():
    status, _ = memory_management_family.read_memory()  # get memory from read_memory function
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
    status, _ = memory_management_family.read_memory()  # get memory from read_memory function
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
                if answer is None:
                    print("\n System: \n exiting task deletion.")
                    break
                confimration = input("Are you sure? Y/N ").upper()
                if confimration == "Y":
                    try:
                        reverse_uuid = reverse_memory_family.read_reverse_memory_cache(answer)
                        del status[status_input][reverse_uuid]
                        memory_management_family.update_memory(status)
                        print(f"Removing task: {answer}")
                    except (KeyError):
                        error_message = cli_interface.system_message("delete error")
                        print(error_message)
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
    status, _ = memory_management_family.read_memory()
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
                tasks_to_update = []
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
                    reverse_uuid = reverse_memory_family.read_reverse_memory_cache(update_answer)
                    # get the mapped uuid from cache
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
                    memory_management_family.update_memory(status)
                except (KeyError):
                    error_message = cli_interface.system_message("delete error")
                    print(error_message)
                break
        elif status_input is None:
            print("Exiting update tasks.")
            break
