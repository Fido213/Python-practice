import cli_interface as cli
import memory_management_family as mem
import reverse_memory_family as rev
import main_features as main
# this file is the main file that runs the todo list terminal interface
# it imports the cli_interface, memory_management_family, main_features
# and reverse_memory_family modules

# Main program loop
rev.initialise_reverse_map()
rev.initialise_reverse_memory_cache()
while True:
    print("\n ----- Todo List Terminal Interface -----"
          "\nYou can add tasks with 'add', view tasks with 'view', "
          "remove tasks with 'remove', update tasks with 'update' "
          "or exit with 'exit'.")
    mem.sanitise_function()
    # loop to allow the user to enter multiple tasks (debug too)
    user_input = cli.terminal_interface()
    # get the user input and assign it to the user_input variable
    if user_input == 'exit':
        print("Exiting the todo list terminal interface.")
        rev.update_memory_reverse(rev.reverse_memory_Cache)
        break
    elif user_input == 'add':
        try:
            status_input, task_input = main.get_user_input()
            # get the user input and assign it to the status_input and task_input
            main.add_task(status_input, task_input)
        except Exception:
            print("\n... success.")
    elif user_input == 'view':
        main.view_tasks()
    elif user_input == 'remove':
        main.remove_task()
    elif user_input == "update":
        main.update_task()
    elif user_input is None:
        print("Exiting the todo list terminal interface.")
        rev.update_memory_reverse(rev.reverse_memory_Cache)
        break
