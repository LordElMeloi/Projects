import string 
import random

password_length = int(input("Enter the lenght of the password you want: "))

print('''Choose from the options below
      1. letters
      2. Numbers
      3. special characters
      4. exit''')

option_chosen = ""

    
while True:
    
    option = int(input("Pick a number from the options given: "))
    if option == 1:
        option_chosen += string.ascii_letters
    
    elif option == 2:
        option_chosen += string.digits

    elif option == 3:
        option_chosen += string.punctuation

    elif option == 4:
        break

    else:
        print("Input a valid option")

password = []

for i in range(password_length):
    randomchar = random.choice(option_chosen)
    password.append(randomchar)

print("The random password is " + "".join(password))