import questionary
from prompt_toolkit.styles import Style  # this is for styling prompts
# this file contains the terminal interface for the todo list application
# it uses the questionary library to create a simple and user friendly
# command line interface

# custom style for usage throughout the code
custom_style = Style(
    [
        ("qmark", "fg:#ff9d00 bold"),  # question mark colour
        (("pointer", "fg:#000000")),  # pointer colour
        ("highlighted", "bg:#ffffff fg:#000000"),  # highlight color
    ]
)


def terminal_interface():
    choices = ["add", "view", "remove", "update", "exit"]
    user_choices = questionary.select(
        "(Arrow keys are utilised throughout the cli)",
        choices=choices,
        style=custom_style
    )
    user_input = user_choices.ask()
    return user_input


def system_message(message):
    system_messages = {"error": "An error occurred. Please try again.",
                       "duplicate": "The task already exists. Please add a different task.",
                       "success": "Operation completed successfully.",
                       "not_found": "Item not found.",
                       "invalid": "Invalid status. Please enter 'finished', 'unfinished', or 'pending'.",
                       "exit": "Exiting the todo list terminal interface.",
                       "delete error": "Error deleting/finding the uuid and task.",
                       "no character": "Please add a valid task not an empty string"
                       }
    print("\n System:")
    return system_messages.get(message.lower(), "Unknown system message.")
