import json
import uuid
from datetime import datetime
import inquirer
import questionary

test_string_correct = "ac33cda7-e302-40ef-ba09-74363c1bd654 : random taskabcdferoinerhakfaslielddd ; date"
test_string_not_correct_order = "random task : uuid ; date"
test_string_not_correct_order_colonsincluded = "random task ; uuid : date"
colours = ["Red", "Green", "Blue"]
answer = questionary.select(
    "Choose a color:",
    choices=colours,
    default=colours[0]  # highlight starts here
).ask()


status = {
    "done": {
        "uuid": {
            "randomuuid": "actualuuid",
            "date": "random date",
            "task": "actual task",
        },
        "uuid2": {
            "randomuuid": "actualuuid",
            "date": "random date",
            "task": "actual task"
        }
    }
}

choices = ["Task A", "Task B", "Task C"]

answer = questionary.select(
    "Choose a task:",
    choices=choices,
    default=choices[0]
).ask()

print("You chose:", answer)
