def flagFinder(app,isAi): #finds guaranteed flags
    if app.numClicks ==0:
        app.message = "no information" #if we can't see anything we can't identify flags
    else:
        found = False
        for row in range(len(app.board)):
            
            for col in range(len(app.board[0])): #loops through the board
                if app.board[row][col].number==0 or (not app.board[row][col].clicked) :
                    continue #if we can't see the square or there are no adjacent mines skips through
                if len(mines(app,row,col)) == app.board[row][col].number:
                    mine = mines(app,row,col)
                    while len(mine)>0 and app.board[mine[0][0]][mine[0][1]].trueFlag: #skips through any flags the bot already found
                        mine = mine[1:]
                    if len(mine)==0:
                        continue
                    
                    found = True
                    break
            if found:
                break
                    
        if not found and not isAi:
            app.message = "make a move to uncover more information for your hint" #if the user asks for a guaranteed flag 
            #and we dont have enough info, tells the user to make a move to gert more info
        elif found:
            return mine[0] #returns location of the guaranteed flag if there is one
        else:
            return None                   
def mines(app,row,col):
    possible = []
    for rows in range(max(0,row-1),min(row+2,len(app.board))):
        for cols in range(max(0,col-1), min(col+2, len(app.board[0]))):
            if (not app.board[rows][cols].clicked):
                possible.append([rows,cols])
    return possible #finds all possible locations for mines
