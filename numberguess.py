import random
import tkinter

# This is a simple number guessing game where the user has to guess a number
# between 1 and 20.


def guess_number():
    correctnumber = random.randint(1, 20)  
    # Randomly select a number between 1 and 20
    attempts = 0  # Initialize attempts counter
    print("Welcome to the Number Guessing Game!")
    print(correctnumber)  
    # For debugging purposes, you can see the correct number
    guess = input("Guess the number between 1 and 20.") 
    guess = int(guess)  # Convert input to integer
    # Input from user
    print(guess)   # Debugging output to see the guess
    while guess != correctnumber:  # Loop until the guess is correct
        print("Incorrect guess. Try again.")
        if guess < correctnumber:
            print("Your guess is too low.")
        elif guess > correctnumber:
            print("Your guess is too high.")
        attempts += 1  # Increment attempts
        print(attempts, "attempts so far.")
        print(correctnumber)  # Debugging output to see the correct number
        guess = input("Guess the number between 1 and 20.")
        guess = int(guess)
        print(guess)  # Debugging output to see the new guess
    else:
        print("Correct! The number was,", correctnumber)


guess_number()  

