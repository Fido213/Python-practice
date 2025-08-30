import json
import uuid
from datetime import datetime
import inquirer

dictionary_test = {"key1": ["value1:2020", "another_value1:2021"], "key2": "value2"}

questions = [
    inquirer.List(
        "status",
        message="Select the status of the task",
        choices=["done", "unfinished", "pending"],
    ),
    inquirer.Text(
        "task",
        message="Enter the task description",
    ),
]

answers = inquirer.prompt(questions)
print(answers["status"] + " " + answers["task"])
