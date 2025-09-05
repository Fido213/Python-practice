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
