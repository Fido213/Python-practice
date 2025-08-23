import json
import uuid
from datetime import datetime

dictionary_test = {
    "key1": ["value1:2020", "another_value1:2021"],
    "key2": "value2"
}

print(dictionary_test["key1"])  # Example usage of the dictionary


user_input = input("Enter something: ")
def check_input():
    if user_input == "key1":
        return user_input
    


def check_input_of_check_input():
    user_input = check_input()
    if user_input in dictionary_test:
        print(f"You entered {user_input}, which is in the dictionary with value {dictionary_test[user_input]}")
        for item in dictionary_test[user_input]:
            print(item.split(":")[0])  # Print only the part before the colon
    else:
        print("You did not enter 'show'")


check_input_of_check_input()
