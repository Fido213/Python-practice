import json
import os
import memory_management_family  # needed for get_memory_path

# this file contains functions for managing the reverse memory (json) files
# such as reading and writing to them, as well as initialising
# the reverse memory files if they do not exist
# this is used to map task names to their UUIDs for easy lookup

reverse_memory_Cache = {}  # global caching place, deletes on exit


def update_memory_reverse(data):
    reverseJSONmemory = memory_management_family.get_memory_path("reverse_memory.json")
    temp_file = reverseJSONmemory + ".tmp"
    # Write to a temporary file
    with open(temp_file, "w") as file:
        json.dump(data, file, indent=4)
    try:
        # Atomically replace the original file with the temporary file
        os.replace(temp_file, reverseJSONmemory)
    except PermissionError:
        print("\n System:\n - Permission error while updating reverse memory file.\n")


def initialise_reverse_map():
    status, _ = memory_management_family.read_memory()  # get the current normal memory
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
    return reverse_dictionary


def reverse_memory_read():
    reverseJSONmemory = memory_management_family.get_memory_path("reverse_memory.json")
    try:
        with open(reverseJSONmemory, "r") as file:
            # set a context manager to open the file in read mode
            reverse_map = json.load(file)
            return reverse_map
    except (FileNotFoundError, json.JSONDecodeError):
        print("\n System:")
        print("Error opening reverse map. initialising new one")
        reverse_dictionary = initialise_reverse_map()
        return reverse_dictionary


def initialise_reverse_memory_cache():
    global reverse_memory_Cache
    reverse_map = reverse_memory_read()
    for reverse_cache_keys, reverse_cache_values in reverse_map.items():
        reverse_memory_Cache[reverse_cache_keys] = reverse_cache_values


def update_reverse_memory_cache(task, uuidvalue):
    reverse_memory_Cache[task] = uuidvalue


def read_reverse_memory_cache(task):
    reverse_uuid = reverse_memory_Cache.get(task)
    return reverse_uuid
