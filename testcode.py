import json
import uuid
from datetime import datetime
import inquirer
import questionary
from prompt_toolkit.styles import Style  # this is for styling prompts

status = {
    "done": {},
    "unfinished":{},
    "pending":{}
}
sample_task = {"uuid": "uuid",
               "date": "date",
               "task": "task"}

custom_style = Style([
                 ("qmark", "fg:#ff9d00 bold"),  # question mark colour
                 (("pointer", "fg:#000000")),  # pointer colour
                 ("highlighted", "bg:#ffffff fg:#000000"),  # highlight color
                    ])

dictionary = {"key": "value",
              "key2": "value2",
              "key2": "value3" }

print(dictionary)
del dictionary["key2"]
print(dictionary)