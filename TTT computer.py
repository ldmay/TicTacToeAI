#A tic tac toe game 

import random


class Board:
    """The board on which the game is played"""
    Lines = []
    Lines.append(" | | ")
    Lines.append("-----")
    Lines.append(" | | ")
    Lines.append("-----")
    Lines.append(" | | ")

    
        


#Creating the run function, which controls the game 
def run():
    print("Welcome to Tic Tac Toe. \nThe game is played by entering integers between 1 and 9, representing fields in the board.")
    print("The corresponding locations are shown below. \n")
    print("1|2|3")
    print("-----")
    print("4|5|6")
    print("-----")
    print("7|8|9\n")


    game = Board()
    win = False
    player = False
    mode = settings()

    #PvP game
    while not win and not mode:

        player = update(game, player)
        win = check_win(game)

    #Computer game
    while not win and mode:

        player = not update(game, player)
        comp_update(game)
        win = check_win(game)


    

#Creating the settings function, which allows player to set PvC (returns true) or PvP game (returns false)
def settings():
    
    mode = input("Would you like to play versus a player or against a computer? Type P or C.\n")
    
    if mode == "P":
        print("\nInitialising PVP game. \n")
        comp = False
    elif mode == "C":
        print("\nInitialising game versus computer. \n")
        comp = True
    else:
        print("\nInput error. Please type the letter P or C only.")
        comp = settings()
    
    return(comp) 

#Creating the check_win function, which controls for the win condition
def check_win(game):

    line1 = game.Lines[0]
    line2 = game.Lines[2]
    line3 = game.Lines[4]
    
    #checking horizontal
    for i in range(0, 5, 2):
        line = game.Lines[i]
        if line[0] != " " and line[0] == line[2] == line[4]:
            print("Player " + line[0] + " has won.")
            return True

    #checking vertical
    for j in range(0, 5, 2):
        if line1[j] != " " and line1[j] == line2[j] == line3[j]:
            print("Player " + line1[j] + " has won.")
            return True

    #checking diagonal
    if line2[2] != " " and (line1[0] == line2[2] == line3[4] or line1[4] == line2[2] == line3[0]):
        print("Player " + line2[2] + " has won.")
        return True
        


#Creating the update function, which updates the board 
def update(game, Player):
    #keep a counter which changes every turn to represent the other player

    move = 0

    if Player == False:
        char = "X"
    else:
        char = "O"

    print(char + "'s turn.")
    move = int(input("Enter an integer between 1 and 9\n"))
    
    if move < 1 or move > 9:
        print("Illegal move. Please enter a valid integer. \n")
        Player = update(game, Player) #if move is illegal, simply call the function again
        return Player #returning Player since calling update has already returned !Player

    else:

        #to change the board
        #this code finds the field which needs to be edited
        if move < 4: 
            row = 0
            column = (move - 1) * 2

        elif move > 6:
            row = 4
            column = (move - 7) * 2 

        else:
            row = 2
            column = (move - 4) * 2 

        #checks whether the move is legal and then edits the board
        line = list(game.Lines[row])

        if line[column] == "X" or line[column] == "O":
            print("Illegal move. Please enter a valid integer. \n")
            Player = update(game, Player) #if move is illegal, simply call the function again
            return Player #returning Player since calling update has already returned !Player

        else:  
            line[column] = char   
            game.Lines[row] = "".join(line)

            #print the board
            print("\n" + game.Lines[0])
            print(game.Lines[1])
            print(game.Lines[2])
            print(game.Lines[3])
            print(game.Lines[4] + "\n")

            #changes the player 
            return not Player


#updates the board on the computer's move 
def comp_update(game):
    #ai will go second 
    #Ideal move is to place token in corner if player puts it in the middle, or vice versa
    #ai works by ranking each possible field it can drop a token on
    

    char = "O"
    player_char = "X"

    print("Computer's turn.")

    #creating an easily accessible list of the fields of the board 
    #location is a list of strings e.g. ["X", " ", "O", " ", ...]
    location = []
    for x in range(0, 5, 2):
        line = game.Lines[x]
        for y in range(0, 5, 2):
            location.append(line[y])
    
    
    #The center field gains a score of 30
    #Any field in a corner gains a score of 20
    #Other field gains a score of 10
    location_score = [20,10,20,10,30,10,20,10,20]


    #Any field that is occupied by a token gains a score of -999
    #Any field which allows ai to win immediatly by connecting three gains a score of 100
    #Any field which prevents opponent from connecting three gains a score of 50
    #Any field which allows ai to connect two tokens with a possible third gains a score of 25
    for x in range(9):
        score = 0
        if location[x] != " ":
            score -= 999

        location_score[x] += score

        #checking whether there are two of the same tokens in a row
        #current field is on the left
        if (x == 0 or x == 3 or x == 6):
            if (location[x + 1] == location[x + 2]):
                if location[x + 1] == char:
                    location_score[x] += 100
                elif location[x + 1] == player_char: 
                    location_score[x] += 50

        #current field is in the middle 
        if (x == 1 or x == 4 or x == 7):
            if (location[x + 1] == location[x - 1]):
                if location[x + 1] == char:
                    location_score[x] += 120
                elif location[x + 1] == player_char: 
                    location_score[x] += 80

        #current field is on the right 
        if (x == 2 or x == 5 or x == 8):
            if (location[x - 1] == location[x - 2]):
                if location[x - 1] == char:
                    location_score[x] += 120
                elif location[x - 1] == player_char: 
                    location_score[x] += 80

        #checking whether there are two of the same tokens in a column


    #Determining which field has the highest score and placing the computer's token here
    current = 0
    field = 0
    for y in range(9):
        if location_score[y] > current:
            current = location_score[y]
            field = y + 1

    print("Field = " + str(field))
    print("Score = " + str(location_score[field - 1]))
    if field < 4:
        row = 0
    elif field < 7:
        row = 2
    else:
        row = 4

    line = list(game.Lines[row])

    if not field % 3:
        column = 4
    elif not (field + 1) % 3:
        column = 2
    else:
        column = 0

    line[column] = char   
    game.Lines[row] = "".join(line)

    #line1 = game.Lines[0]
    #line2 = game.Lines[2]
    #line3 = game.Lines[4]
   

    ##checking vertical
    #for j in range(0, 4, 2):
    #    if line1[j] != " " and line1[j] == line2[j] == line3[j]:
    #        print("Player " + line1[j] + " has won.")
    #        return True

    ##checking diagonal
    #if line2[2] != " " and (line1[0] == line2[2] == line3[4] or line1[4] == line2[2] == line3[j]):
    #    print("Player " + line2[2] + " has won.")
    #    return True



    #print the board
    print("\n" + game.Lines[0])
    print(game.Lines[1])
    print(game.Lines[2])
    print(game.Lines[3])
    print(game.Lines[4] + "\n")


run()