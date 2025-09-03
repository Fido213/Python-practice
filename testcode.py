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

status_asked = input("pick a status ")
def user_input():
    choices = set(status.keys())
    if status_asked in choices:
        choices.remove(status_asked)
    status_input = questionary.select("Choose a status:",
        choices=choices,
        style=custom_style
    )
    answer = status_input.ask()
    task_input = input("Input task")
    return answer, task_input


def add():
    answer, task_input = user_input()
    status[answer][uuid.uuid4()] = task_input


add()
print(status)