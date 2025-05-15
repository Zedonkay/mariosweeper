from hints import *
import copy
from board import *
def move(app,board): #checks to see the next move to do
    if app.numClicks == 0: #breaks board
        return makeFirstMove(app,board)
    elif allMinesFound(app,board): #IF FOUND ALL MINES CLICK ALL OTHER SQUARES
        for row in range(len(board)):
            for col in range(len(board[0])):
                elem = board[row][col]
                if not (elem.trueFlag or elem.hasFlag or elem.clicked):
                    clickBoard(app,board,[(row,col)])
    elif flagFinder(app,True)!=None: # has guaranteed Mines
        return placeFlags(app,board)
    elif falseFlags(app,board)!=[]: #checks for user placed incorrect flags
        falseflags = falseFlags(app,board)
        board[falseflags[0][0]][falseflags[0][1]].flag(app,True)
        return board
    
    elif easyMoves(app,board)!=None: #checks to see if there are any clicks it can make
        clicks = easyMoves(app,board)
        click = clicks[0]
        
        return clickBoard(app,board,[click])

    else: #tries to use reasoning to solve the board
        guesses = getGuessables(app, board) #gets all positions on the board where it can guess
        done = False #stores whether the app has moved with reasoning
        if guesses == None: #if there are no places to guess tell the user there are no legal moves
            app.message = "no legal moves"
            return board 
        for prob in guesses: #goes through the guesses in order of probability (explained in probability function)
            guess = guesses[prob]
            for row in range(max(guess[0]-1,0),min(guess[0]+2,len(board))):
                for col in range(max(guess[1]-1,0),min(guess[1]+2,len(board[0]))):
                    if (not board[row][col].clicked) and (not board[row][col].trueFlag):
                        elem = board[row][col]
                        elem.flag(app,True)
                        elem.trueFlag = True
                        elem.guessFlag = True #guesses a flag adjacent to the number that has flags yet to be placed
                        
                        
                        if mover(app,board)!=None:#recursively tries to finish the board (not looking at new info)
                            done = True #if the board can be finished with this guess, it exits
                            break
                        else: #otherwise it resets the board
                            elem.trueFlag = False
                            elem.guessFlag = False
                if done: #if the board has been finished, exits
                    break
            if done: #if the board has been finished, exits
                break
        if not done:#if after going through everything, there is nothing to do it tells the useer this
            app.message = "no guaranteed moves"
    if board == None: #if after going through everything, there is nothing to do it tells the useer this
        app.message = "no guaranteed moves"
        return app.board
    return board
def easyMoves(app,board): #finds any immediately clickable cells
    for row in range(len(board)):
            for col in range(len(board[0])):
                elem = board[row][col] #looops through every cell in the board
                if (not elem.clicked) or (elem.number ==0) or (not app.board[row][col].clicked):
                    continue
                if len(safeClicks(app,board,row,col,elem.number))>0 : #if there are safeclicks adacent to that cell
                    return safeClicks(app,board, row,col,elem.number) #returns all safe clicks adjacent to that cell 
    return None
def safeClicks(app,board,row,col,num): #finds all safe clicks around a cell
    store = []
    for rows in range(max(0,row-1),min(row+2,len(board))):
        for cols in range(max(0,col-1),min(col+2,len(board[0]))):
            if board[rows][cols].trueFlag: #if we know that there is a guaranteed mine we have found already 
                num-=1 #reduces number of mines we have to look for
            elif not board[rows][cols].clicked:
                store.append([rows,cols]) #stores all unclicked (and un trueflagged) adjacent squares
    if num==0:
        return store #if all mines have been found adjacent to the cell, returns all unclicked (and untrueflagged ) cells adjacent to the original cell
    else:
        return [] #if we haven't found all mines returns an empty list signifying thee are no guaranteed safe clicks
def makeFirstMove(app,board): #makes the first move on the board
    app.drawMario = True
    app.mX,app.mY = app.boardLeft+app.boardWidth//2, app.boardTop + app.boardHeight//2
    board = writeNumbers(placeMines(app, board,(app.size//8)*13,app.size//2,app.size//2))
    app.numClicks+=1
    clickBoard(app,board,[[app.size//2,app.size//2]])
    return board       
def isSolved(board): #checks if we have won the game
    for row in board:
        for elem in row:
            if not (elem.hasFlower or elem.clicked):
                return False #loops through every cell in the baord and if there are any unclicked cells that don't have mines returns false
    return True #if every cell is either clicked or has a mine returns true
def placeFlags(app,board): #places flags on the board where the flag finder tells it to  
    flag1 = flagFinder(app,True)
    board[flag1[0]][flag1[1]].trueFlag = True
    board[flag1[0]][flag1[1]].flag(app,True)
    
    return board
def falseFlags(app,board): #looks for false flags (user incorrectly placed) on the board
    store = []
    for row in range(len(board)):
        for col in range(len(board[0])): #loops through the board
            if board[row][col].hasFlag and not board[row][col].trueFlag and not board[row][col].guessFlag:
                store.append([row,col])
    if store!=[]:
        app.message = f"You do not have sufficient information to guarantee flags at the following locations: {store}"
    return store

def getGuessables(app,board): #comes up with all unfulfilled numbered squares on the board that have been exposed
    guesses = []
    sortedGuesses = dict()
    for row in range(len(board)):
        for col in range(len(board[0])): #loops through the squares on the baord
            if  app.board[row][col].clicked and  board[row][col].number != 0:
                if isGuessable(board,row,col): #if the element is clicked, has a number, and is guessable it adds to a list

                    guesses.append((row,col))
    if guesses == []:
        return None
    for item in guesses: #if there are items in the list of guessables
        itemProb = getProbability(board, item,app)
        sortedGuesses[itemProb] = item
        sortedGuesses = dict(sorted(sortedGuesses.items(),reverse = True))
    
    return sortedGuesses
def isGuessable(board,row,col): #finds if a numbered cell is unfulfilled
    num = board[row][col].number
    for rows in range(max(row-1,0),min(row+2,len(board))):
        for cols in range(max(col-1,0), min(col+2,len(board[0]))):
            if board[rows][cols].trueFlag:
                
                num -=1
    
    return num !=0 #essentially just returns if there are flags adjacent to the square that we have not found yet
def allMinesFound(app,board): #checks if we have found all the mines on the board
    count = 0
    for row in board:
        for elem in row:
            if elem.trueFlag:
                count+=1
    return (count == ((len(board)//8)*13))
def getProbability(board, guess,app): #used to rank what our strongest guess is
    possible = 0
    flags = board[guess[0]][guess[1]].number
    for row in range(max(0,guess[0]-1),min(len(board),guess[0]+2)):
        for col in range(max(0,guess[1]-1), min(guess[1]+2,len(board[0]))):
            if board[row][col].trueFlag:
                print("flag at:", (row,col))
                flags-=1
            elif not board[row][col].clicked :
                possible+=1
    print("flags:", flags, "possible:", possible, "guess:", guess)
    return (flags/possible)**(flags)
#we find how many flags we have to place adjacent to the square and 
#how many possible locations there are for these flags
#by nature of the function, values are first ranked and seperated into buckets by how many flags have left to be placed
#then inside of these buckets osrted by how many possible locations there are
#this is done because guessing one flag is much easier than guessing 2 and so on
#and then guessing one flag in 2 possible squares is less time taking than guessing one in 8

def mover(app,board): #same as the move function except return to be recursive
    if isSolved(board): #base case
        return board
    else:
        if app.numClicks == 0: #breaks board
            board = makeFirstMove(app,board)
        elif flagFinder(app,True)!=None: # has guaranteed Mines
            board = placeFlags(app,board)
        elif falseFlags(app,board)!=[]: #checks for user placed incorrect flags
            falseflags = falseFlags(app,board)
            board[falseflags[0][0]][falseflags[0][1]].flag(app,True)
        elif easyMoves(app,board)!=None: #checks to see if there are any clicks it can make
            clicks = easyMoves(app,board)
            click = clicks[0]
            
            board =  clickBoard(app,board,[click])

        else:
            guesses = getGuessables(app, board)
            if guesses == None:
                return None
            for prob in guesses:
                
                guess = guesses[prob]
                board[guess[0]][guess[1]].trueFlag,board[guess[0]][guess[1]].guessFlag = True,True
                solution = mover(app,board)
                if solution !=None:
                    return solution
                
            return None
        return board

                    
                    
