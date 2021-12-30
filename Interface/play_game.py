# Slide Puzzle

import numpy as np
import re
from tkinter.constants import S, TRUE
import pygame, sys, random,os
import time
from pygame.locals import *
sys.path.append("..")
from Backend.SlidingPuzzle import slidingPuzzleGame

# Khởi tạo các biến ban đầu
# BOARDWIDTH = None # number of columns in the board
# BOARDHEIGHT =  None # number of rows in the board
# TILESIZE = None
WINDOWWIDTH = 800
WINDOWHEIGHT = 600
FPS = 30
BLANK = None

# Khai báo các màu
#                 R    G    B
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BRIGHTBLUE = (0, 50, 255)
DARKTURQUOISE = (3, 54, 73)
GREEN = (0, 204, 0)
YELLOW = (255, 247, 0)

BGCOLOR = DARKTURQUOISE
TILECOLOR = YELLOW
TEXTCOLOR = WHITE
BORDERCOLOR = BRIGHTBLUE
BASICFONTSIZE = 20

BUTTONCOLOR = WHITE
BUTTONTEXTCOLOR = BLACK
MESSAGECOLOR = WHITE

# XMARGIN = None
# YMARGIN = None

UP = "up"
DOWN = "down"
LEFT = "left"
RIGHT = "right"


def main(size, fileFlag=0):
    global FPSCLOCK, DISPLAYSURF, BASICFONT, RESET_SURF, RESET_RECT, NEW_SURF, NEW_RECT, SOLVE_SURF, SOLVE_RECT, astar_surf, astar_rect, bfs_surf, bfs_rect, dfs_surf, dfs_rect, human_surf, human_rect, ids_surf, ids_rect
    global BOARDWIDTH, BOARDHEIGHT, TILESIZE, XMARGIN, YMARGIN, boardsize
    global current_time, start_time, move, move_btn, move_surf, move_rect, time_btn, time_surf, time_rect
    move = 0
    current_time = 0.0
    start_time=0.0
    mainBoard=[]
    if fileFlag==1: mainBoard, size = generateNewPuzzle(0, 1)
    global flag #show or hide when click on solve
    
    BOARDWIDTH = size 
    BOARDHEIGHT = size 
    boardsize = 500 
    flag = 0
    human_flag = 0
    dfs_flag = 0
    bfs_flag = 0
    astar_flag = 0
    ids_flag = 0

    TILESIZE = boardsize // BOARDWIDTH
    # XMARGIN = int((WINDOWWIDTH - (TILESIZE * BOARDWIDTH + (BOARDWIDTH - 1))) / 2)
    # YMARGIN = int((WINDOWHEIGHT - (TILESIZE * BOARDHEIGHT + (BOARDHEIGHT - 1))) / 2)
    XMARGIN = (WINDOWHEIGHT - boardsize-20)//2
    YMARGIN = (WINDOWHEIGHT - boardsize+20)//2

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption("Slide Puzzle")
    BASICFONT = pygame.font.Font("freesansbold.ttf", BASICFONTSIZE)


    # Store the option buttons and their rectangles in OPTIONS.
    offsetButtonY = (WINDOWWIDTH - XMARGIN - boardsize) -100

    time_surf, time_rect = makeTextCenter("Time", BUTTONTEXTCOLOR, BGCOLOR, WINDOWWIDTH - offsetButtonY, 100)
    move_surf, move_rect = makeTextCenter("Move", BUTTONTEXTCOLOR, BGCOLOR, WINDOWWIDTH-offsetButtonY, 200)  

    RESET_SURF, RESET_RECT = makeTextCenter(
        "Reset", BUTTONTEXTCOLOR, BUTTONCOLOR, WINDOWWIDTH - offsetButtonY, 300
    )
    NEW_SURF, NEW_RECT = makeTextCenter(
        "New Game", BUTTONTEXTCOLOR, BUTTONCOLOR, WINDOWWIDTH - offsetButtonY, 330
    )
    SOLVE_SURF, SOLVE_RECT = makeTextCenter(
        "Solve", BUTTONTEXTCOLOR, BUTTONCOLOR, WINDOWWIDTH - offsetButtonY, 360
    )
    human_surf, human_rect = makeTextCenter("Human", BLACK, GREEN, WINDOWWIDTH - offsetButtonY, 400)
    astar_surf, astar_rect = makeTextCenter("A-star", BLACK, GREEN, WINDOWWIDTH - offsetButtonY, 430)
    bfs_surf, bfs_rect = makeTextCenter("BFS", BLACK, GREEN, WINDOWWIDTH - offsetButtonY, 460)
    dfs_surf, dfs_rect = makeTextCenter("DFS", BLACK, GREEN, WINDOWWIDTH - offsetButtonY, 490)
    ids_surf, ids_rect = makeTextCenter("IDS", BLACK, GREEN, WINDOWWIDTH - offsetButtonY, 520)
    global done
    done = False

    if fileFlag==0: mainBoard = generateNewPuzzle(3*size*size)

    SOLVEDBOARD = (
        getStartingBoard()
    )  # a solved board is the same as the board in a start state.
    allMoves = []  # list of moves made from the solved configuration

    global running
    running = True
    text = ""


    while running:  # main game loop

        

        slideTo = None  # the direction, if any, a tile should slide
        msg = "Click tile or press arrow keys to slide."  # contains the message to show in the upper left corner.
        if mainBoard == SOLVEDBOARD:
            msg = "Solved!"
            done = True
            #Call win GUI

        else: 
            done=False
        if done==False: update_time()
        drawBoard(mainBoard, msg)

        checkForQuit()

        if text!= "": 
            drawBoard(mainBoard, "Calculating...")
            pygame.display.update()
            slidingPuzzleGame.run_algo(BOARDHEIGHT, text)
            read_algo_and_show(mainBoard, text)
            text = ""

        for event in pygame.event.get():  # event handling loop
            if event.type == MOUSEBUTTONUP:
                spotx, spoty = getSpotClicked(mainBoard, event.pos[0], event.pos[1])

                if (spotx, spoty) == (None, None):
                    # check if the user clicked on an option button
                    if RESET_RECT.collidepoint(event.pos):
                        resetAnimation(mainBoard, allMoves)  # clicked on Reset button
                        allMoves = []
                    elif NEW_RECT.collidepoint(event.pos):
                        mainBoard = generateNewPuzzle(
                            3*size*size
                        )  # clicked on New Game button
                        allMoves = []
                    elif SOLVE_RECT.collidepoint(event.pos):
                        # NOTE:
                        flag = 1-flag
                        human_flag = 1 - human_flag
                        if size<=3: 
                            dfs_flag = 1-dfs_flag
                            ids_flag = 1-ids_flag
                        if size<=5: 
                            bfs_flag = 1-bfs_flag
                            astar_flag = 1-astar_flag
                        
                        # write_board_to_file(mainBoard)
                        # slidingPuzzleGame.run_algo(BOARDHEIGHT, "HUMAN")
                        # read_algo_and_show(mainBoard, "human")
                        # resetAnimation(
                        #     mainBoard, solutionSeq + allMoves
                        # )  # clicked on Solve button

                        solutionSeq = []
                        allMoves = []

                    if flag==1:
                        write_board_to_file(mainBoard)
                    
                    if astar_flag==1 and astar_rect.collidepoint(event.pos): text="A*"
                    elif bfs_flag==1 and bfs_rect.collidepoint(event.pos): text = "BFS"
                    elif dfs_flag==1 and dfs_rect.collidepoint(event.pos): text = "DFS"
                    elif human_flag==1 and human_rect.collidepoint(event.pos): text="HUMAN"
                    elif ids_flag==1 and ids_rect.collidepoint(event.pos): text = "IDS"


                else:
                    # check if the clicked tile was next to the blank spot

                    blankx, blanky = getBlankPosition(mainBoard)
                    if spotx == blankx + 1 and spoty == blanky:
                        slideTo = LEFT
                    elif spotx == blankx - 1 and spoty == blanky:
                        slideTo = RIGHT
                    elif spotx == blankx and spoty == blanky + 1:
                        slideTo = UP
                    elif spotx == blankx and spoty == blanky - 1:
                        slideTo = DOWN

            elif event.type == KEYUP:
                # check if the user pressed a key to slide a tile
                if event.key in (K_LEFT, K_a) and isValidMove(mainBoard, LEFT):
                    slideTo = LEFT
                elif event.key in (K_RIGHT, K_d) and isValidMove(mainBoard, RIGHT):
                    slideTo = RIGHT
                elif event.key in (K_UP, K_w) and isValidMove(mainBoard, UP):
                    slideTo = UP
                elif event.key in (K_DOWN, K_s) and isValidMove(mainBoard, DOWN):
                    slideTo = DOWN

        if slideTo:
            slideAnimation(
                mainBoard, slideTo, "Click tile or press arrow keys to slide.", 20
            )  # show slide on screen
            makeMove(mainBoard, slideTo)
            allMoves.append(slideTo)  # record the slide
        pygame.display.update()
        FPSCLOCK.tick(FPS)


def update_time():
    global start_time, current_time, done
    if done==False:
        if(move==1): start_time =time.time()
        if(move!=0): current_time = int(time.time() - start_time)

def terminate():
    pygame.quit()
    sys.exit()


def checkForQuit():
    global running
    for event in pygame.event.get(QUIT):  # get all the QUIT events
        terminate()  # terminate if any QUIT events are present
    for event in pygame.event.get(KEYUP):  # get all the KEYUP events
        if event.key == K_ESCAPE:
            #terminate()  # terminate if the KEYUP event was for the Esc key
            running = False
        pygame.event.post(event)  # put the other KEYUP event objects back


def getStartingBoard():
    # Return a board data structure with tiles in the solved state.
    # For example, if BOARDWIDTH and BOARDHEIGHT are both 3, this function
    # returns [[1, 4, 7], [2, 5, 8], [3, 6, BLANK]]
    counter = 1
    board = []
    for x in range(BOARDWIDTH):
        column = []
        for y in range(BOARDHEIGHT):
            column.append(counter)
            counter += BOARDWIDTH
        board.append(column)
        counter -= BOARDWIDTH * (BOARDHEIGHT - 1) + BOARDWIDTH - 1

    board[BOARDWIDTH - 1][BOARDHEIGHT - 1] = BLANK
    return board


def getBlankPosition(board):
    # Return the x and y of board coordinates of the blank space.
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            if board[x][y] == BLANK or board[x][y] == 0 or board[x][y] == "_":
                return (x, y)


def makeMove(board, direction):
    # This function does not check if the direction is valid.
    blankx, blanky = getBlankPosition(board)

    global move, done
    if done==True: move=0
    else: move +=1

    if direction == UP:
        board[blankx][blanky], board[blankx][blanky + 1] = (
            board[blankx][blanky + 1],
            board[blankx][blanky],
        )
    elif direction == DOWN:
        board[blankx][blanky], board[blankx][blanky - 1] = (
            board[blankx][blanky - 1],
            board[blankx][blanky],
        )
    elif direction == LEFT:
        board[blankx][blanky], board[blankx + 1][blanky] = (
            board[blankx + 1][blanky],
            board[blankx][blanky],
        )
    elif direction == RIGHT:
        board[blankx][blanky], board[blankx - 1][blanky] = (
            board[blankx - 1][blanky],
            board[blankx][blanky],
        )


def isValidMove(board, move):
    blankx, blanky = getBlankPosition(board)
    return (
        (move == UP and blanky != len(board[0]) - 1)
        or (move == DOWN and blanky != 0)
        or (move == LEFT and blankx != len(board) - 1)
        or (move == RIGHT and blankx != 0)
    )


def getRandomMove(board, lastMove=None):
    # start with a full list of all four moves
    validMoves = [UP, DOWN, LEFT, RIGHT]

    # remove moves from the list as they are disqualified
    if lastMove == UP or not isValidMove(board, DOWN):
        validMoves.remove(DOWN)
    if lastMove == DOWN or not isValidMove(board, UP):
        validMoves.remove(UP)
    if lastMove == LEFT or not isValidMove(board, RIGHT):
        validMoves.remove(RIGHT)
    if lastMove == RIGHT or not isValidMove(board, LEFT):
        validMoves.remove(LEFT)

    # return a random move from the list of remaining moves
    return random.choice(validMoves)


def getLeftTopOfTile(tileX, tileY):
    left = XMARGIN + (tileX * TILESIZE) + (tileX - 1)
    top = YMARGIN + (tileY * TILESIZE) + (tileY - 1)
    return (left, top)


def getSpotClicked(board, x, y):
    # from the x & y pixel coordinates, get the x & y board coordinates
    for tileX in range(len(board)):
        for tileY in range(len(board[0])):
            left, top = getLeftTopOfTile(tileX, tileY)
            tileRect = pygame.Rect(left, top, TILESIZE, TILESIZE)
            if tileRect.collidepoint(x, y):
                return (tileX, tileY)
    return (None, None)


def drawTile(tilex, tiley, number, adjx=0, adjy=0):
    # draw a tile at board coordinates tilex and tiley, optionally a few
    # pixels over (determined by adjx and adjy)
    left, top = getLeftTopOfTile(tilex, tiley)
    pygame.draw.rect(
        DISPLAYSURF, TILECOLOR, (left + adjx, top + adjy, TILESIZE, TILESIZE)
    )
    textSurf = BASICFONT.render(str(number), True, TEXTCOLOR)
    textRect = textSurf.get_rect()
    textRect.center = left + int(TILESIZE / 2) + adjx, top + int(TILESIZE / 2) + adjy
    DISPLAYSURF.blit(textSurf, textRect)


def makeText(text, color, bgcolor, top, left):
    # create the Surface and Rect objects for some text.
    textSurf = BASICFONT.render(text, True, color, bgcolor)
    textRect = textSurf.get_rect()
    textRect.topleft = (top, left)
    return (textSurf, textRect)


def draw_text(text, color, x_coor, y_coor ):
    textObject = BASICFONT.render(text, True, color)
    textRect = textObject.get_rect()
    textRect.center = (x_coor, y_coor)
    DISPLAYSURF.blit(textObject, textRect)


def button(text_content,text_color,button_color,dx,dy,width=200,height=50):
    btn = pygame.Rect(dx, dy, width, height)
    pygame.draw.rect(DISPLAYSURF, button_color, btn)
    draw_text(text_content, text_color, dx + width // 2, dy + height // 2)
    return btn



def makeTextCenter(text, color, bgcolor, x, y): 
    # create the Surface and Rect objects for some text.
    textSurf = BASICFONT.render(text, True, color, bgcolor)
    textRect = textSurf.get_rect()
    textRect.center = (x, y)
    return (textSurf, textRect)

def drawBoard(board, message):
    DISPLAYSURF.fill(BGCOLOR)
    if message:
        textSurf, textRect = makeText(message, MESSAGECOLOR, BGCOLOR, 5, 5)
        DISPLAYSURF.blit(textSurf, textRect)

    for tilex in range(len(board)):
        for tiley in range(len(board[0])):
            if board[tilex][tiley]:
                drawTile(tilex, tiley, board[tilex][tiley])

    left, top = getLeftTopOfTile(0, 0)
    width = BOARDWIDTH * TILESIZE
    height = BOARDHEIGHT * TILESIZE
    pygame.draw.rect(
        DISPLAYSURF, BORDERCOLOR, (left - 5, top - 5, width + 11, height + 11), 4
    )
    DISPLAYSURF.blit(time_surf,time_rect)
    DISPLAYSURF.blit(move_surf, move_rect)
    #note: thêm btn hiển thị thời gian và move 
    time_btn = button(str(int(current_time)), BLACK, WHITE, WINDOWWIDTH-215, 120, width=100)
    button(str(move), BLACK, WHITE, WINDOWWIDTH-215, 220, width=100)
    DISPLAYSURF.blit(RESET_SURF, RESET_RECT)
    DISPLAYSURF.blit(NEW_SURF, NEW_RECT)
    DISPLAYSURF.blit(SOLVE_SURF, SOLVE_RECT)

    if(flag ==1):
        DISPLAYSURF.blit(human_surf, human_rect)
        if BOARDHEIGHT<=5:
            DISPLAYSURF.blit(astar_surf, astar_rect)
            DISPLAYSURF.blit(bfs_surf, bfs_rect)
        if BOARDHEIGHT<=3:
            DISPLAYSURF.blit(dfs_surf, dfs_rect)
            DISPLAYSURF.blit(ids_surf, ids_rect)


def slideAnimation(board, direction, message, animationSpeed):
    # Note: This function does not check if the move is valid.

    blankx, blanky = getBlankPosition(board)
    if direction == UP:
        movex = blankx
        movey = blanky + 1
    elif direction == DOWN:
        movex = blankx
        movey = blanky - 1
    elif direction == LEFT:
        movex = blankx + 1
        movey = blanky
    elif direction == RIGHT:
        movex = blankx - 1
        movey = blanky

    # prepare the base surface
    drawBoard(board, message)
    baseSurf = DISPLAYSURF.copy()
    # draw a blank space over the moving tile on the baseSurf Surface.
    moveLeft, moveTop = getLeftTopOfTile(movex, movey)
    pygame.draw.rect(baseSurf, BGCOLOR, (moveLeft, moveTop, TILESIZE, TILESIZE))

    for i in range(0, TILESIZE, animationSpeed):
        # animate the tile sliding over
        checkForQuit()
        DISPLAYSURF.blit(baseSurf, (0, 0))
        if direction == UP:
            drawTile(movex, movey, board[movex][movey], 0, -i)
        if direction == DOWN:
            drawTile(movex, movey, board[movex][movey], 0, i)
        if direction == LEFT:
            drawTile(movex, movey, board[movex][movey], -i, 0)
        if direction == RIGHT:
            drawTile(movex, movey, board[movex][movey], i, 0)

        pygame.display.update()
        FPSCLOCK.tick(FPS)


def generateNewPuzzle(numSlides, flag=0):
    # From a starting configuration, make numSlides number of moves (and
    # animate these moves).
    if flag==0: 
    
        board = getStartingBoard()
        drawBoard(board, "")
        pygame.display.update()
        pygame.time.wait(500)  # pause 500 milliseconds for effect
        lastMove = None
        for i in range(numSlides):
            direction = getRandomMove(board, lastMove)
            slideAnimation(
                board, direction, "Generating new puzzle...", animationSpeed=int(BOARDHEIGHT*BOARDHEIGHT*TILESIZE // 30)
            )
            makeMove(board, direction)
            lastMove = direction
            global move
            move=0
        return board

    elif flag==1:#Read data from file
        path = os.path.join(os.path.dirname(__file__), "..", "Backend", "SlidingPuzzle",  "inputOutput", "data.txt")
        file = open(path, "r")
        lines = file.readlines()
        board = []
        size=0
        for line in lines:
            element = re.split(" ", line)
            tmp = []
            for a in element:
                if a=="0": tmp.append(None)
                else: tmp.append(int(a))
            board.append(tmp)
            size+=1
        
        for i in range(0,size):
            for j in range(i, size):
                board[i][j], board[j][i] = board[j][i], board[i][j]
        return (board, size)



def resetAnimation(board, allMoves):
    # make all of the moves in allMoves in reverse.
    revAllMoves = allMoves[:]  # gets a copy of the list
    revAllMoves.reverse()

    for move in revAllMoves:
        if move == UP:
            oppositeMove = DOWN
        elif move == DOWN:
            oppositeMove = UP
        elif move == RIGHT:
            oppositeMove = LEFT
        elif move == LEFT:
            oppositeMove = RIGHT
        slideAnimation(board, oppositeMove, "", animationSpeed=int(TILESIZE / 2))
        makeMove(board, oppositeMove)

# write to file for calculate algorithm
def write_board_to_file(board):
    path = os.path.join(os.path.dirname(__file__), "..", "Backend", "SlidingPuzzle",  "inputOutput", "input.txt")
    file = open(path, "w")
    for i in range(BOARDWIDTH): 
        for j in range(BOARDHEIGHT): 
            if board[j][i] == None:
                file.write("0")
            else:
                file.write(str(board[j][i]))
            file.write(" ")
        file.write('\n')

def read_algo_and_show(board, algorithms):
    path = os.path.join(os.path.dirname(__file__), "..", "Backend", "SlidingPuzzle",  "inputOutput", "solution.txt")
    file = open(path, "r")
    lines = file.readlines()
    text = "Solving by " + algorithms +" algorithm..."
    check_exit = False
    for line in lines:
        move =""
        if line.strip() == "UP": 
            move = DOWN
        elif line.strip() == "DOWN": 
            move = UP
        elif line.strip() == "LEFT": 
            move = RIGHT
        elif line.strip() == "RIGHT": 
            move = LEFT

        if check_exit == True: 
            break

        slideAnimation(board, move, text, animationSpeed=int( BOARDHEIGHT*BOARDHEIGHT*TILESIZE // 30))
        makeMove(board, move)
        update_time()

        for event in pygame.event.get():
            if event.type == KEYUP:
                if event.key == K_q: 
                    check_exit = True
            pygame.event.post(event)
        
    
    
# if __name__ == "__main__":
#     main(3)
