from cmu_graphics import *
import os, pathlib, PIL.Image, random, math, string
from board import *
from hints import *
from Classes import *
from bot import *

# ---------------------- App Lifecycle Functions ----------------------

def onAppStart(app):
    """
    Initializes or resets the application state.
    """
    resetApp(app)

def onStep(app):
    """
    Handles periodic updates for the app, such as timers, win/loss animations, and game state checks.
    """
    # Display message timer
    if app.message is not None:
        app.displayTime += 1
    if app.displayTime == 15 * 3:
        app.message = None
        app.displayTime = 0
    # Game timer
    if app.numClicks != 0 and app.game:
        app.time += 1

    # Start game if board size is set
    if app.size is not None:
        app.game = True

    # Win animation
    if app.win:
        if app.winTime < 32:
            app.winTime += 1
        else:
            app.winTime = 0
        app.drawMario = False

    # Loss animation
    if app.loss:
        if app.deathTime < 32:
            app.deathTime += 1
        else:
            app.deathTime = 0
        app.drawMario = False

    # Check for win condition
    if app.game:
        if isSolved(app.board):
            app.game = False
            app.win = True
            app.winSound.play()
            app.drawMario = False

def resetApp(app):
    """
    Sets all starting values for the app. Used to reset or start the app.
    """
    app.deathAnimation = dict()
    app.winAnimation = dict()
    for i in range(33):
        app.deathAnimation[i] = CMUImage(PIL.Image.open("images/death/dead_" + str(i) + ".jpg"))
    for i in range(33):
        app.winAnimation[i] = CMUImage(PIL.Image.open("images/win/win_" + str(i) + ".jpg"))
    app.deathTime = 0
    app.winTime = 0
    app.flag = CMUImage(PIL.Image.open("images/turtle.png"))
    app.mario = CMUImage(PIL.Image.open("images/mario.png"))
    app.drawMario = False
    app.width = 1600
    app.height = 1040
    app.mX = 40
    app.mY = 40
    app.size = None
    app.boardLeft = 400
    app.time = 0
    app.boardWidth = 800
    app.boardTop = 150
    app.boardHeight = 800
    app.openingScreen = True
    app.game = False
    app.flagCount = 0
    runScreen(app)
    app.board = None
    app.loss = False
    app.numClicks = 0
    app.win = False
    app.stepsPerSecond = 13
    app.displayTime = 0
    app.message = None
    app.showInfo = False
    app.closeButton = button('X')
    app.resetClose = False
    app.blockBreak = loadSound("sounds/blockbreak.mp3")
    app.itsMe = loadSound("sounds/itsme.mp3")
    app.lossSound = loadSound("sounds/loss.mp3")
    app.winSound = loadSound("sounds/win.mp3")
    app.flagPlace = loadSound("sounds/placeFlag.mp3")
    app.flagRemove = loadSound("sounds/removeFlag.mp3")
    app.playing = False

# ---------------------- Input Handlers ----------------------

def onKeyPress(app, key):
    """
    Handles key press events.
    """
    if key == 'r':
        resetApp(app)
    elif key == 'm' and app.game and not app.showInfo:
        if move(app, app.board) is not None:
            app.board = move(app, app.board)
        else:
            app.message = "no guaranteed moves"

def onMousePress(app, mouseX, mouseY, button):
    """
    Handles mouse press events (left and right click).
    """
    if app.openingScreen:
        if app.medium.inButton(mouseX, mouseY) and button == 0:
            app.openingScreen = False
            app.size = 16
            app.flagCount = 26
            runBoard(app)
        elif app.hard.inButton(mouseX, mouseY) and button == 0:
            app.openingScreen = False
            app.size = 24
            app.flagCount = 39
            runBoard(app)
        elif app.info.inButton(mouseX, mouseY) and button == 0:
            app.showInfo = True

        if app.showInfo:
            app.closeButton.cX, app.closeButton.cY, app.closeButton.width, app.closeButton.height = 1068, 428, 50, 50
            if app.closeButton.inButton(mouseX, mouseY) and button == 0:
                app.resetClose = True
                app.showInfo = False

    if app.game:
        if app.info.inButton(mouseX, mouseY) and button == 0:
            app.showInfo = True
        if app.showInfo:
            app.closeButton.cX, app.closeButton.cY, app.closeButton.width, app.closeButton.height = 1168, 178, 50, 50
            if app.closeButton.inButton(mouseX, mouseY) and button == 0:
                app.resetClose = True
                app.showInfo = False
            app.drawMario = False
        else:
            for row in range(len(app.board)):
                for col in range(len(app.board[0])):
                    if app.board[row][col].inCell(mouseX, mouseY) and button == 0:
                        if app.numClicks == 0:
                            app.drawMario = True
                            app.itsMe.play(loop=False)
                            app.mX, app.mY = mouseX, mouseY
                            app.board = writeNumbers(placeMines(app, app.board, (app.size // 8) * 13, row, col))
                            app.numClicks += 1
                        clickBoard(app, app.board, [[row, col]])
                    elif app.board[row][col].inCell(mouseX, mouseY) and button == 2 and not (app.numClicks == 0) and not app.board[row][col].clicked:
                        app.board[row][col].flag(app, False)

def onMouseMove(app, mouseX, mouseY):
    """
    Handles mouse movement events.
    """
    if app.numClicks != 0 and app.game:
        if legalMario(mouseX, mouseY, app):
            app.mX, app.mY = mouseX, mouseY

# ---------------------- Helper Functions ----------------------

def legalMario(x, y, app):
    """
    Determines if Mario's current position is legal.
    """
    width, height = getWidthHeight(app)
    if not ((app.boardLeft < x - width // 2) and (app.boardLeft + app.boardWidth > x + width // 2) and
            (app.boardTop < y - height // 2) and (app.boardTop + app.boardHeight > y + height // 2)):
        return False
    for row in app.board:
        for elem in row:
            if not elem.clicked:
                if (elem.inCell(x + width // 2, y + height // 2) or
                    elem.inCell(x + width // 2, y - height // 2) or
                    elem.inCell(x - width // 2, y + height // 2) or
                    elem.inCell(x - width // 2, y - height // 2) or
                    elem.inCell(x, y)):
                    return False
    return True

def getWidthHeight(app):
    """
    Returns the width and height of a cell.
    """
    return (app.boardWidth // app.size, app.boardHeight // app.size)

# ---------------------- Drawing Functions ----------------------

def redrawAll(app):
    """
    Draws all elements on the screen depending on the current app state.
    """
    if app.loss:
        drawGameOver(app)
    elif app.openingScreen:
        drawScreen(app)
        if app.showInfo:
            drawBox(499, 399, 601, 501, 5)
            drawRect(1070, 430, 55, 55, align='center', fill=rgb(222, 88, 23))
            app.closeButton.drawButton(1068, 428, 50, 50)
            drawLabel("Choose what difficulty you want to play", 515, 475, font="Super Mario 256", align="left-top", size=22, fill=rgb(41, 21, 2))
            drawLabel("Medium is a smaller grid with less mines", 515, 510, font="Super Mario 256", align="left-top", size=22, fill=rgb(41, 21, 2))
            drawLabel("Hard is a larger grid with more mines", 515, 545, font="Super Mario 256", align="left-top", size=22, fill=rgb(41, 21, 2))
    elif app.game:
        drawGame(app)
        if app.showInfo:
            drawBox(399, 149, 801, 801, 5)
            drawRect(1170, 180, 55, 55, align='center', fill=rgb(222, 88, 23))
            app.closeButton.drawButton(1168, 178, 50, 50)
            drawLabel("Mario wants to get to Peach, but first he must", 450, 200, font="Super Mario 256", align="left-top", size=22, fill=rgb(41, 21, 2))
            drawLabel("make it through this board without being eaten ", 450, 224, font="Super Mario 256", align="left-top", size=22, fill=rgb(41, 21, 2))
            drawLabel("by a piranha plant. Your job is to find all of ", 450, 248, font="Super Mario 256", align="left-top", size=22, fill=rgb(41, 21, 2))
            drawLabel("the piranha plants and clear all off the remaing ", 450, 272, font="Super Mario 256", align="left-top", size=22, fill=rgb(41, 21, 2))
            drawLabel("space on the board so Mario and Peach can live ", 450, 296, font="Super Mario 256", align="left-top", size=22, fill=rgb(41, 21, 2))
            drawLabel("happily ever after here.", 450, 320, font="Super Mario 256", align="left-top", size=22, fill=rgb(41, 21, 2))
            drawLabel("How to Play", 450, 380, font="Super Mario 256", align="left-top", size=28, fill=rgb(41, 21, 2))
            drawLabel("1. If the board is blank, click a random square", 470, 410, font="Super Mario 256", align="left-top", size=20, fill=rgb(41, 21, 2))
            drawLabel("2. The numbers tell you the number of adjacent flowers", 470, 430, font="Super Mario 256", align="left-top", size=20, fill=rgb(41, 21, 2))
            drawLabel("3. Rightclicking a square throws a shell at a cell", 470, 450, font="Super Mario 256", align="left-top", size=20, fill=rgb(41, 21, 2))
            drawLabel("- Do this to kill suspected flowers", 500, 470, font="Super Mario 256", align="left-top", size=20, fill=rgb(41, 21, 2))
            drawLabel("4. If you believe a square is safe, left to reveal it", 470, 490, font="Super Mario 256", align="left-top", size=20, fill=rgb(41, 21, 2))
            drawLabel("5. Keep going until every square has a shell or is clicked", 470, 510, font="Super Mario 256", align="left-top", size=20, fill=rgb(41, 21, 2))
            drawLabel("6. If you ever need help, click m for the computer to play", 470, 530, font="Super Mario 256", align="left-top", size=20, fill=rgb(41, 21, 2))
            drawLabel("7. If you want to exit back to home, click r", 470, 550, font="Super Mario 256", align="left-top", size=20, fill=rgb(41, 21, 2))
    elif app.win:
        drawImage(app.winAnimation[app.winTime], 0, 0, width=app.width, height=app.height)
        drawLabel(f"YAY! ", 200, 60, size=25, font="Super Mario 256")
        drawLabel(f"{app.time // 15} seconds!", 200, 90, size=25, font="Super Mario 256")

    if app.drawMario:
        drawMario(app)

def loadSound(relativePath):
    """
    Loads a sound file from a relative path.
    """
    absolutePath = os.path.abspath(relativePath)
    url = pathlib.Path(absolutePath).as_uri()
    return Sound(url)

def drawGameOver(app):
    """
    Draws the death screen.
    """
    drawImage(app.deathAnimation[app.deathTime], 0, 0, width=app.width, height=app.height)
    drawLabel("You Died :(", app.width - 200, 90, size=50, fill='black', font="Super Mario 256")

def runScreen(app):
    """
    Initializes the opening screen buttons.
    """
    app.info = button("i")
    app.medium = button("medium")
    app.hard = button("hard")

def drawScreen(app):
    """
    Draws the opening screen.
    """
    drawRect(0, 0, app.width, app.height, fill=rgb(160, 181, 250))
    title = "MARIOSWEEPER"
    index = 0
    distances = [55, 42, 32, 30, 40, 45, 45, 36, 36, 36, 36, 36]
    colors = [rgb(0, 158, 219), rgb(255, 210, 2), rgb(229, 40, 15), rgb(70, 173, 55)]
    for char in title:
        drawLabel(char, 150 + sum(distances[0:index]) * 3, 200, font="Super Mario 256", size=150, fill=colors[(index % 4)], border='black')
        index += 1
    drawBox(500, 400, 600, 500, 5)
    drawInfo(app)
    app.medium.drawButton(app.width // 2, 650 - 100, 200, 100)
    app.hard.drawButton(app.width // 2, 650 + 100, 200, 100)

def runBoard(app):
    """
    Initializes the game board.
    """
    app.board = initializeBoard(app.size)

def drawMario(app):
    """
    Draws Mario at his current position.
    """
    width, height = getWidthHeight(app)
    drawImage(app.mario, app.mX, app.mY, align='center', width=width, height=height)

def drawGame(app):
    """
    Draws the main game screen.
    """
    drawRect(0, 0, app.width, app.height, fill=rgb(160, 181, 250))
    drawRect(app.boardLeft - 1, app.boardTop - 1, app.boardWidth + 2, app.boardHeight + 2, fill=rgb(253, 222, 202))
    if app.displayTime != 0:
        drawBox(200, 968, 1200, 60, 5)
        drawLabel(app.message, 800, 998, size=20, font="Super Mario 256", fill=rgb(41, 21, 2))
    width, height = getWidthHeight(app)
    for row in range(app.size):
        for col in range(app.size):
            app.board[row][col].drawCell(app.boardLeft + (width * col), app.boardTop + height * row, width, height, app)
    title = "MARIOSWEEPER"
    index = 0
    distances = [55, 42, 32, 30, 40, 45, 45, 36, 36, 36, 36, 36]
    colors = [rgb(0, 158, 219), rgb(255, 210, 2), rgb(229, 40, 15), rgb(70, 173, 55)]
    for char in title:
        drawLabel(char, 400 + sum(distances[0:index]) * 2, 70, font="Super Mario 256", size=100, fill=colors[(index % 4)], border='black')
        index += 1
    drawBox(1300, 200, 200, 100, 5)
    drawLabel(f"{app.flagCount}", 1362, 250, align='center', font="Super Mario 256", fill=rgb(253, 222, 202), size=50)
    drawImage(app.flag, 1437, 250, width=50, height=50, align='center')
    drawBox(100, 200, 200, 100, 5)
    drawLabel(f"Time:{(app.time // 15)}", 200, 250, align='center', font="Super Mario 256", fill=rgb(253, 222, 202), size=40)
    drawInfo(app)

def drawInfo(app):
    """
    Draws the info button.
    """
    app.info.drawButton(1525, 975, 50, 50)
    drawBox(1500, 950, 50, 50, 3)
    drawLabel("i", 1528, 980, font="Super Mario 256", size=30, fill=rgb(253, 222, 202))
    drawCircle(1525, 963, 4, fill=rgb(253, 222, 202))

def drawBox(left, top, width, height, circleR):
    """
    Draws a stylized box used throughout the game.
    """
    drawRect(left - 3, top - 3, width + 6, height + 6, fill=rgb(253, 222, 202))
    drawRect(left, top, width + 3, height + 3, fill=rgb(7, 1, 30))
    drawRect(left, top, width, height, fill=rgb(222, 88, 23))
    drawCircle(left + 12, top + 12, circleR, fill=rgb(7, 1, 30))
    drawCircle(left + 10, top + 10, circleR, fill=rgb(253, 222, 202))
    drawCircle(left + width - 8, top + 12, circleR, fill=rgb(7, 1, 30))
    drawCircle(left + width - 10, top + 10, circleR, fill=rgb(253, 222, 202))
    drawCircle(left + width - 8, top + height - 8, circleR, fill=rgb(7, 1, 30))
    drawCircle(left + width - 10, top + height - 10, circleR, fill=rgb(253, 222, 202))
    drawCircle(left + 12, top + height - 8, circleR, fill=rgb(7, 1, 30))
    drawCircle(left + 10, top + height - 10, circleR, fill=rgb(253, 222, 202))

# ---------------------- Main Entry Point ----------------------

def main():
    """
    Runs the application.
    """
    runApp()

main()