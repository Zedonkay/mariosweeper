import copy
from cmu_graphics import *
import PIL.Image
class cell(): #creates the cell class
    def __init__(self): #initializes a default cell
        self.flower = CMUImage(PIL.Image.open("images/turtle.png"))
        self.hasFlower = False
        self.number = None
        self.clicked = False
        self.safe = False
        self.trueFlag = False
        self.hasFlag = False
        self.extraLifes = 0
        self.color = rgb(222,88,23)
        self.guessFlag = False
    def __repr__(self): #used for debugging
        return f"{self.hasFlower},{self.number},{self.clicked}"
    def setFlower(self,flower): #puts a flower at the desired position
        self.hasFlower = flower
    def makeSafe(self): #makes a square safe
        self.safe = True
    def isSafe(self): #returns if a square is safe
        return self.safe
    def addNumber(self,number): #writes a number to the cell
        self.number= number
    def clickSquare(self): #clicks a cell
        self.clicked = True
        self.color = rgb(253,222,202)
    def checkFlower(self): #checks if the cell has a flower
        return self.hasFlower
    def flag(self,app,isAi): #flags a cell
        if not self.hasFlag: #if the cell does not already have a flag
            if app.flagCount>0: #if there are still flags available to the user
                app.flagPlace.play()
                app.flagCount-=1
                self.hasFlag = True #places them
            elif isAi: #if there are no available flags but the bot is saying there must be a flag here
                app.message = "you have incorrect flags" #tells the user that they have placed some incorrect flags

        elif self.trueFlag and not isAi: #if the bot has placed a flag there and the user tries to remove it
            app.message = "this is a guaranteed flag" #tells hte user this flag is guaranteed
        elif self.trueFlag:
            pass
        else: #if there was a flag there, but the user tries to remove it
            self.hasFlag = False
            app.flagCount+=1
            app.flagRemove.play()
            self.color = rgb(222,88,23) #removes the flag
        
        
    def drawCell(self,left,top,width,height,app): #draws each cell
        self.left = left
        self.top = top
        self.width = width
        self.height = height
        if self.clicked:
            self.border = rgb(222,88,23)
        else:
            self.border = rgb(253,222,202)
        drawRect(left,top,width,height,border = self.border,fill = self.color)
        if self.clicked:
            if not (self.number==0):
                if app.size==16:
                    fontSize = 50
                else:
                    fontSize = 35
                drawLabel(f"{self.number}",left+width//2,top+height//2,font = "Super Mario 256", size = fontSize,fill = rgb(79,166,2))
        elif self.hasFlag:
            drawImage(self.flower,left,top ,width = width,height = height)
    def getCellLeftTop(self): #gets the left and top of the cell
        return (self.left,self.top)    
    def inCell(self,x,y): #checks if a position is in a cell
        return (self.left<x<self.left+self.width) and (self.top<y<self.top+self.height)
class button(): #button class
    def __init__(self,label): #initializes a button with a label
        self.label = label
    def drawButton(self,cX, cY, width, height): #draws a button at the desired position

        self.cX = cX
        self.cY = cY
        self.width = width
        self.height = height
        drawRect(cX+2,cY+2,width+2,height+2,fill = 'black',align ='center')
        drawRect(cX,cY,width,height,fill = rgb(253,222,202),align ='center')
        drawLabel(self.label, cX,cY,fill = rgb(137,76,47),font = "Super Mario 256",size = 40)
    def inButton(self,x,y):  #returns if a position is inside the button
        return (self.cX-self.width//2<x<self.cX+self.width//2) and (self.cY-self.height//2<y<self.cY+self.height//2)
