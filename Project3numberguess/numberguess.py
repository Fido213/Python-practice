import random
import tkinter as tk  # importing tkinter (tk) for GUI applications

# This is a simple number guessing game where the user has to guess a number
# between 1 and 20.

root = tk.Tk()  # Create the main window
root.title("Number Guessing Game")  # Set the title of the window
root.geometry("300x200")
labelWelcom = tk.Label(root, text="Welcome to the Number Guessing Game!")
labelWelcom.pack()  # Add the label to the window
labelInstruction = tk.Label(root, text="Guess a number between 1 and 20:")
labelInstruction.pack()  # Add the label to the window
labelAttempts = tk.Label(root, text="Attempts: 0")
labelAttempts.pack(side=tk.BOTTOM)  # Add the attempts label to the window
Entry = tk.Entry(root, width=25)  # Create an entry widget for user input
Entry.pack()  # Add the entry widget to the window
correctnumber = random.randint(1, 20)  # Randomly select a number between 1
# and 20
attempts = 0  # Initialize attempts counter


# function to handle getting the guess from the user


def get_guess(event):  # Bind this function to an event if needed
    global attempts, correctnumber  # Use global variables
    guess = Entry.get()  # Get the input from the entry widget
    try:
        guess = int(guess)  # Convert input to integer
    except ValueError:
        labelInstruction.config(text="Please enter a valid number.")
        # Handle invalid input
        return None

    attempts += 1
    labelAttempts.config(text=f"Attempts: {attempts}")

    if guess < correctnumber:
        labelInstruction.config(text="Your guess is too low.")
    elif guess > correctnumber:
        labelInstruction.config(text="Your guess is too high.")
    else:
        labelInstruction.config(text=f"Correct! The number was {correctnumber}")
        Entry.config(state="disabled")
        root.after(2000, root.destroy)
        # Closes the window after 2 seconds (root.after is used to delay the
        # execution of the function)


# binding the get_guess function to the Return key press event
Entry.bind("<Return>", get_guess)
root.mainloop()
# Start the main event loop to run the application
