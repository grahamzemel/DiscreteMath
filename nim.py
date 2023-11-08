def nim(chipCount, maxTake):
    modVar = maxTake + 1
    if(chipCount % modVar == 0):
        return -1
    else:
        return (chipCount % modVar)
    
while True:
    count = int(input("How many chips are there on the table initially? \n"))
    max = int(input("What is the maximum number of chips you can take on your turn? \n"))
    if(count > 0 and max > 0):
        while True:
            takes = nim(count, max)
            if(takes == -1):
                print("Robot would like you to go first!")
            else:
                count -= takes
                if(count <= 0):
                    print("Robot wins!")
                    break
                else: 
                    print("Remaining chips after robot's turn: " + str(count))
            humanTake = int(input("How many would you like to take from the pile? \n"))
            if(humanTake > 0 and humanTake <= max):
                count -= humanTake
                if(count <= 0):
                    print("You win!")
                    break
            else:
                print("Please enter a positive number less than or equal to the maximum.")
                continue
            print("Remaining chips: " + str(count))
        break
    else:
        print("Please enter a positive number for both.")