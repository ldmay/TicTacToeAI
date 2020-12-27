
#A 5x5 tic tac toe game with (hopefully) a minimax ai algorithm
#line of 4 needed to win

import random
import numpy as np


SIZE = 5


class Board:
    """A 5x5 board to play tic tac toe"""
    
    Lines = []
    def __init__(self):

        self.Lines = []

        for i in range(SIZE): 
            self.Lines.append([0] * SIZE)
        self.Lines = np.asarray(self.Lines)



#Creating the run function, which controls the game 
def run():
    print("Welcome to Tic Tac Toe. \nThe game is played by entering integers between 0 and 15, representing fields in the board.")
    print("The corresponding locations are shown below. \n")
    ex = Board()
    for row in range(ex.Lines.shape[0]):
        for col in range(ex.Lines.shape[1]):
            ex.Lines[row,col] = row * SIZE + col
    display(ex)
    print("\n")

    game = Board()
    display(game)
    win = False
    mode = settings()
    player = random.randint(1,2)

    #PvP game
    while not win and not mode:        

        display(ex)
        player = update(game, player)
        win = check_win(game)

    #Computer game
    while not win and mode:

        if player == 1: 
            display(ex)
            player = update(game, player)
            player = comp_update(game, player)

        elif player == 2:
            comp_update(game, 1)
            display(ex)
            update(game, 2)
            
        win = check_win(game)


#Displays the board. 
def display(board):
    print(board.Lines)
    

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

    #checking row of for in horizontal direction
    for row in range(SIZE):
        line = game.Lines[row,:]
        if line[0] == line[1] == line[2] == line[3] != 0 or line[1] == line[2] == line[3] == line[4] != 0:
           print("Player " + str(line[1]) + " has won in row " + str(row))
           return True

    #checking vertical
    for col in range(SIZE):
        line = game.Lines[:,col]
        if line[0] == line[1] == line[2] == line[3] != 0 or line[1] == line[2] == line[3] == line[4] != 0:
           print("Player " + str(line[1]) + " has won in column " + str(col))
           return True

    #checking diagonal  
    #negative direction
    field = game.Lines[1,1]
    if field != 0 and (game.Lines[2,2] == field and game.Lines[3,3] == field and game.Lines[4,4] == field or 
                       game.Lines[2,2] == field and game.Lines[3,3] == field and game.Lines[0,0] == field):
        print("Player " + str(field) + " has won in negative diagonal.")
        return True

    field = game.Lines[0,1]
    if field != 0 and game.Lines[1,2] == field and game.Lines[2,3] == field and game.Lines[3,4] == field:
        print("Player " + str(field) + " has won in negative diagonal.")
        return True

    field = game.Lines[1,0]
    if field != 0 and game.Lines[2,1] == field and game.Lines[3,2] == field and game.Lines[4,3] == field:
        print("Player " + str(field) + " has won in negative diagonal.")
        return True

    #positive direction
    field = game.Lines[1,3]
    if field != 0 and (game.Lines[0,4] == field and game.Lines[2,2] == field and game.Lines[3,1] == field or 
                       game.Lines[2,2] == field and game.Lines[3,1] == field and game.Lines[4,0] == field):
        print("Player " + str(field) + " has won in positive diagonal.")
        return True

    field = game.Lines[1,4]
    if field != 0 and game.Lines[2,3] == field and game.Lines[3,2] == field and game.Lines[4,1] == field:
        print("Player " + str(field) + " has won in positive diagonal.")
        return True

    field = game.Lines[3,0]
    if field != 0 and game.Lines[2,1] == field and game.Lines[1,2] == field and game.Lines[0,3] == field:
        print("Player " + str(field) + " has won in positive diagonal.")
        return True
        


#Creating the update function, which updates the board 
def update(game, turn):
    #keep a counter which changes every turn to represent the other player

    move = 0

    print("Player " + str(turn) + "'s turn.")
    move = int(input("Enter an integer between 0 and 24\n"))
    

    #to change the board
    #this code finds the field which needs to be edited
    if move > -1 and move < 5: 
        row = 0
        column = move

    elif move > 4 and move < 10:
        row = 1
        column = move - 5

    elif move > 9 and move < 15:
        row = 2
        column = move - 10

    elif move > 14 and move < 20:
        row = 3 
        column = move - 15

    elif move > 19 and move < 25:
        row = 4
        column = move - 20

    else: 
        print("Illegal move. Please enter a valid integer. \n")
        turn = update(game, turn) #if move is illegal, simply call the function again
        return turn #returning Player since calling update has already returned !Player


    #checks whether the move is legal and then edits the board

    if game.Lines[row,column] != 0:
        print("Illegal move. Field is already occupied by token. \n")
        turn = update(game, turn) #if move is illegal, simply call the function again
        return turn #returning Player since calling update has already returned !Player

    else:  
        game.Lines[row,column] = turn

    display(game)
    
    if turn == 2:
        return 1
    elif turn == 1:
        return 2




#updates the board on the computer's move 
def comp_update(game, turn):
    #ai works by ranking each possible field it can drop a token on
    
    #scores:
    CENTRE = 10
    TOKEN = -999
    ONE_AD = 15
    TWO_AD = 30
    PREVENT_WIN = 60
    WIN = 100




    token = turn

    if turn == 2:
        player_token = 1
    else:
        player_token = 2

    print("Computer's turn.")

    score = Board()
        
    for row in range(1,4):
        for col in range(1,4):
            score.Lines[row,col] += CENTRE

    

    #This scoring system is not perfect 
    for row in range(SIZE):
        #Any field with a token gains -999
        for col in score.Lines:
            if game.Lines[row,col] != 0:
                score.Lines[row,col] -= TOKEN

        #Any field adjacent to a token gains 15
        #row
        for col in range(SIZE - 1):
            if game.Lines[row,col] == token:
                score.Lines[row,col+1] += ONE_AD
            if game.Lines[row,SIZE-col] == token:
                score.Lines[row,SIZE-col-1] += ONE_AD


        for col in range(SIZE):
            if row != 4 and col !=4:
                if game.Lines[row,col] == token:
                    score.Lines[row+1,col+1] +=ONE_AD
            elif row!= 0 and col != 0:
                if game.Lines[row,col] == token:
                    score.Lines[row-1,col-1] +=ONE_AD
            elif row != 0 and col != 4:
                if game.Lines[row,col] == token:
                    score.Lines[row-1,col+1] +=ONE_AD
            elif row != 4 and col != 0:
                if game.Lines[row,col] == token:
                    score.Lines[row+1,col-1] +=ONE_AD

    #column 
    for col in range(SIZE - 1):
        for row in range(SIZE - 1):
            if game.Lines[row,col] == token == game.Lines[row+1,col]:
                score.Lines[row+1,col] += ONE_AD
            if game.Lines[SIZE-row,col] == token == game.Lines[SIZE-row-1,col]:
                score.Lines[row-1,col] += ONE_AD

    #fields adjacent to two tokens in a row gain 40
    #row
    for row in range(SIZE):
        for col in range(SIZE-2):
            if game.Lines[row,col+1] == game.Lines[row,col+2] == token:
                score.Lines[row,col] += TWO_AD
            if game.Lines[row,SIZE-col-2] == game.Lines[row,SIZE-col-3] == token:
                score.Lines[row,SIZE-col-1] += TWO_AD

    #column
    for col in range(SIZE):
        for row in range(SIZE-2):
            if game.Lines[row+1,col] == game.Lines[row+2,col] == token:
                score.Lines[row,col] += TWO_AD
            if game.Lines[SIZE-row-2,col] == game.Lines[SIZE-row-3,col] == token:
                score.Lines[SIZE-row-1,col] += TWO_AD

    #diagonal - skip for now 




    #preventing opponent from reaching four in a row and trying to reach four in a row itself
    #checking for row of four
    for row in range(SIZE):
        for col in range(SIZE-2):
            line = game.Lines[row,:]
            if line[col] == line[col+1] == line[col+2]:
                if line[col] == player_token:
                    score.Lines[row,col] += PREVENT_WIN
                elif line[col] == player_token:
                    score.Lines[row,col] += PREVENT_WIN
            elif line[SIZE-col-1] == line[SIZE-col-2] == line[SIZE-col-3] == player_token:
                score.Lines[row,col] += PREVENT_WIN

    #checking for column of four 
    for col in range(SIZE):
        for row in range(SIZE-2):
            line = game.Lines[:,col]
            if line[row] == line[row+1] == line[row+2] == player_token:
                score.Lines[row,col] += PREVENT_WIN
            elif line[SIZE-row-1] == line[SIZE-row-2] == line[SIZE-row-3] == player_token:
                score.Lines[row,col] += PREVENT_WIN

    #checking diagonal  
    #negative direction

    if game.Lines[0,1] == game.Lines[1,2] == game.Lines[2,3] != 0:
        if game.Lines[0,1] == player_token:
            score.Lines[3,4] += PREVENT_WIN
        elif game.Lines[0,1] == token:
            score.Lines[3,4] += WIN
    elif game.Lines[3,4] == game.Lines[1,2] == game.Lines[2,3] != 0:
        if game.Lines[3,4] == player_token:
            score.Lines[0,1] += PREVENT_WIN
        elif game.Lines[3,4] == token:
            score.Lines[0,1] += WIN

    if game.Lines[1,0] == game.Lines[2,1] == game.Lines[3,2] != 0:
        if game.Lines[1,0] == player_token:
            score.Lines[4,3] += PREVENT_WIN
        elif game.Lines[1,0] == token:
            score.Lines[4,3] += WIN
    elif game.Lines[4,3] == game.Lines[2,1] == game.Lines[3,2] != 0:
        if game.Lines[4,3] == player_token:
            score.Lines[1,0] += PREVENT_WIN
        elif game.Lines[4,3] == token:
            score.Lines[1,0] += WIN


    if game.Lines[1,1] == game.Lines[2,2] == game.Lines[3,3] != 0:
        if game.Lines[2,2] == player_token:
            score.Lines[1,1] += PREVENT_WIN
            score.Lines[4,4] += PREVENT_WIN
        elif game.Lines[2,2] == token:
            score.Lines[1,1] += WIN
            score.Lines[4,4] += WIN

    #positive direction

    if game.Lines[1,4] == game.Lines[2,3] == game.Lines[3,2] != 0:
        if game.Lines[1,4] == player_token:
            score.Lines[4,1] += PREVENT_WIN
        elif game.Lines[1,4] == token:
            score.Lines[4,1] += WIN
    elif game.Lines[2,3] == game.Lines[3,2] == game.Lines[4,1] != 0:
        if game.Lines[4,1] == player_token:
            score.Lines[1,4] += PREVENT_WIN
        elif game.Lines[4,1] == token:
            score.Lines[1,4] += WIN

    if game.Lines[3,0] == game.Lines[2,1] == game.Lines[1,2] != 0:
        if game.Lines[3,0] == player_token:
            score.Lines[0,3] += PREVENT_WIN
        elif game.Lines[3,0] == token:
            score.Lines[0,3] += WIN
    elif game.Lines[0,3] == game.Lines[2,1] == game.Lines[1,2] != 0:
        if game.Lines[0,3] == player_token:
            score.Lines[3,0] += PREVENT_WIN
        elif game.Lines[0,3] == token:
            score.Lines[3,0] += WIN

    if game.Lines[1,3] == game.Lines[2,2] == game.Lines[3,1] != 0:
        if game.Lines[2,2] == player_token:
            score.Lines[0,4] += PREVENT_WIN
            score.Lines[4,0] += PREVENT_WIN
        elif game.Lines[2,2] == token:
            score.Lines[0,4] += WIN
            score.Lines[4,0] += WIN

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
    




run()