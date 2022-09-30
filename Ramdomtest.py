import random
computer_number = random.randint(1,100)

for i in range(7):
    user_number = int(input("Enter a number between 1 to 100 "))
    if (user_number == computer_number):
        print (i)
        print("Congratulations !!! You cracked the number in " + str(i) + " attempts")
        print("The number is " + str(computer_number))
        break

    elif (user_number > computer_number):
        print("You entered greater than the random number")
    else:
        print("you entered less than the random number")
print("You need to say all chances exhausted, better luck next time")
print("The correct number is " + str(computer_number))

