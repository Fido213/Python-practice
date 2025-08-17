status = {
    "done": [],
    "unfinished": [],
    "pending": [],
    }
# This is a dictionary, the key is the status and its value is a list in which
# tasks will be appended to


def check_task(INPstatus):
    if INPstatus in status:
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


for loop in range(5):
    # loop to allow the user to enter multiple tasks (debug too)
    if input("do you want to add another task? (yes/no): ").lower() != 'yes':
        break
    else:
        userinput = input("Enter status and task name in order")
        # get the user input and then split it into status and task name
        split_input = userinput.split(" ", 1)
        print(split_input)
        # assign a variable to the status
        status_input = split_input[0]
        task_inputsplit = split_input[1:]  # assign a variable to the task
        # the 1: is like in excel where u select a range of cells from a certain index
        task_input = ' '.join(task_inputsplit)   # join the list into a string
        # simplifies the task name aswell as going from list to string
        check_task(status_input)


print(f"unfished list: {status['pending']}")
