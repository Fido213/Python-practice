while True:
    user_input = input('Type a number between 1 and 10:')
    user_input = int(user_input)
    if user_input == 100:
        break
    elif user_input % 2 == 0:
        print('GREEN')
    else:
        print('RED')
