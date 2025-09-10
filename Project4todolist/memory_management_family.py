import os
import json
import reverse_memory_family

# this file contains functions for managing the memory (json) files
# such as reading and writing to them, as well as initialising
# the memory files if they do not exist


def get_memory_path(filename):
    # os.path.abspath(__file__) gets the full path of the current script
    # no matter the working directory
    script_location = os.path.abspath(__file__)
    # os.path.dirname basically gets the directory of the full path
    script_directory = os.path.dirname(script_location)
    # os.path.join takes the directory (absolute path) and joins it with
    # the relative path to the json file, this makes it so that no matter
    # where the user runs the script from, it will always find the json file
    file_path = os.path.join(script_directory, "memory", filename)
    return file_path


def start_dictionary():
    # this function is purely as a failsafe to restart and update
    # the dictionary format
    # this also servers as a cache
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
    JSONmemory = get_memory_path("memory.json")
    # get the path to memory.json in a way that works no matter
    Memory_is_empty = False
    Memory_not_found_or_error = False
    Memory_found = "found"
    try:
        with open(JSONmemory, "r") as file:
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
        print(
            "\n System: \n - Memory file not found/Error decoding it, creating a new one.\n"
        )
        status = start_dictionary()
        Memory_not_found_or_error = True
        return status, Memory_not_found_or_error
        # if the file is not found, create a new dictionary


def update_memory(data):
    JSONmemory = get_memory_path("memory.json")
    temp_file = JSONmemory + ".tmp"
    # Write to a temporary file first
    with open(temp_file, "w") as file:
        json.dump(data, file, indent=4)
    # Replace the original file with the temporary file atomically
    try:
        os.replace(temp_file, JSONmemory)
    except PermissionError:
        print("\n System:\n - Permission error while updating memory file.\n")


def sanitise_function():
    # this function is for clearing out bad data
    status, _ = read_memory()
    seen_tasks = set()
    tasks_to_delete = []
    # since i cant update and delete at runtime, it gives an error
    # so i assign it to a list and then delete it at the end of the loop
    # ill add a check to see if theres any duplicates
    # to print the "stable" in the else
    duplicate = False  # this is to check later to print stable or not
    for status_verification in status:
        for task_dictionary in status[status_verification].values():
            task_to_compare = task_dictionary.get("Task").strip()
            if task_to_compare in seen_tasks:
                print("\n System:")
                print(
                    f"'{task_to_compare}' in '{status_verification}' is a duplicate, deleting...\n"
                )
                duplicate = True
                reverse_dictionary = (
                    reverse_memory_family.reverse_memory_read()
                )  # reverse mapping
                reverse_uuid = reverse_dictionary.get(task_to_compare)
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
                print(f"Deleted task with UUID: {uuid_value} from '{status_key}'")
            except KeyError:
                print("\n System:")
                print("Error deleting/finding the uuid and task.")
    update_memory(status)
