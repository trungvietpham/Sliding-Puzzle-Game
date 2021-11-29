from tkinter import *
from tkinter.ttk import Entry, Button, OptionMenu
from PIL import Image, ImageTk
import random
import tkinter.filedialog
import os



class Tiles():
  def __init__(self, grid):
    self.tiles = []
    self.grid = grid
    self.gap = None  #define in func setGap below
    self.moves=0

  def add(self, tile):
    self.tiles.append(tile)

  def getTile(self, *pos):
    for tile in self.tiles:
      if tile.pos == pos:
          return tile

  def getTileAroundGap(self):
    gRow, gCol = self.gap.pos
    return self.getTile(gRow, gCol-1),self.getTile(gRow, gCol+1),self.getTile(gRow-1, gCol),self.getTile(gRow+1, gCol) 

  def changeGap(self, tile):
    try:  
      gPos = self.gap.pos
      self.gap.pos = tile.pos
      tile.pos = gPos
      self.moves+=1
    except:
      pass

  # slide gap follow keyboard, and compare
  def slide(self, key):
    left, right, top, down = self.getTileAroundGap()
    if key=='Up': self.changeGap(down)
    if key=='Down': self.changeGap(top)
    if key=='Right': self.changeGap(left)
    if key=='Left': self.changeGap(right)
    self.show()




  # shuffle function need to be update, check validate shuffle
  def shuffle(self):
      random.shuffle(self.tiles)
      i=0 #iter
      for row in range(self.grid):
        for col in range(self.grid):
            self.tiles[i].pos=(row,col)
            i+=1

  def show(self):
    for tile in self.tiles:
      if self.gap!=tile:
        tile.show()

  # define missing tile? 
  def setGap(self, index): 
    self.gap = self.tiles[index]


  def isCorrect(self):
    for tile in self.tiles:
        if not tile.isCorrectPos(): return False
    return True




class Tile(Label):
  def __init__(self, parent, tileImage, pos):
    Label.__init__(self, parent, image = tileImage)

    self.image = tileImage
    self.pos = pos
    self.curPos = pos

  def show(self):
    self.grid(row = self.pos[0], column=self.pos[1])

  def isCorrectPos(self):
    return self.pos==self.curPos

class Board(Frame):
  MAX_BOARD_SIZE = 500
  def __init__(self, parent, image, grid, win, *args, **kwargs):
    Frame.__init__(self, parent, *args, **kwargs)

    self.parent = parent
    self.grid = grid  
    self.win = win
    self.image = self.openImage(image)
    self.tileSize = self.image.size[0]/self.grid
    self.tiles = self.createTiles()
    self.tiles.shuffle()  #shuffle tiles
    self.tiles.show()
    self.bindKeys()

  def openImage(self, image):
    image = Image.open(image) #Image here is import at line 3
    imageSize = min(image.size)  #get size of image
    if imageSize>self.MAX_BOARD_SIZE:  #if size too big
        image = image.resize((self.MAX_BOARD_SIZE, self.MAX_BOARD_SIZE), Image.ANTIALIAS)  #then resize it 
    if image.size[0] > image.size[1]:
        image = image.crop((0,0, image.size[1], image.size[1]))
    elif image.size[0]< image.size[1]: 
        image = image.crop((0,0, image.size[0], image.size[0]))
    return image

  # function get keyboard event
  def bindKeys(self):
    self.bind_all('<Key-Up>', self.slide)
    self.bind_all('<Key-Down>', self.slide)
    self.bind_all('<Key-Left>', self.slide)
    self.bind_all('<Key-Right>', self.slide)

  #function handle event?   
  def slide(self, event):
    self.tiles.slide(event.keysym)

    #check if correct or not
    if self.tiles.isCorrect():
        self.win(self.tiles.moves)

  # function split default image into n^2 pieces
  def createTiles(self):
    tiles = Tiles(self.grid) #Tiles is a class define above
    for row in range(self.grid):
        for col in range(self.grid):
            x0 = col*self.tileSize
            y0 = row*self.tileSize
            x1 = x0+self.tileSize
            y1 = y0+self.tileSize
            tileImage = ImageTk.PhotoImage(self.image.crop((x0, y0, x1, y1)))
            tile = Tile(self, tileImage, (row, col)) #Tile is a class define above
            tiles.add(tile)
    tiles.setGap(-1)  #can we pass variable into here? 
    return tiles


class Main():
  def __init__(self, parent):
    self.parent = parent

    self.image = StringVar()
    self.winText = StringVar()
    self.grid = IntVar()

    self.createWidgets()

  def createWidgets(self):
    self.mainFrame = Frame(self.parent)
    Label(self.mainFrame, text = 'Sliding Puzzle', font=('', 50)).pack(padx = 10, pady=10)  #pad: offset from center?
    frame = Frame(self.mainFrame)
    Label(frame, text = 'Images').grid(sticky=W)
    Entry(frame, textvariable = self.image, width = 50).grid(row=0, column=1, padx=10, pady=10)
    Button(frame, text='Browse', command=self.browse).grid(row=0, column=2, pady=10, padx= 10)  

    Label(frame, text = 'Grid').grid(sticky=W)
    OptionMenu(frame, self.grid ,*[2,3,4,5,6,7,8,9,10]).grid(row=1, column=1, padx=10, pady=10, sticky=W)
    frame.pack(padx=10,pady=10)

    Button(self.mainFrame, text='Start',command=self.start).pack(padx=10, pady=10)
    self.mainFrame.pack()
    self.board = Frame(self.parent)
    self.winFrame = Frame(self.parent)
    Label(self.winFrame, textvariable=self.winText, font=('', 50), padx=10, pady=10)
    Button(self.winFrame, text='Play Again', command=self.playAgain).pack(padx=10, pady=10)

  # define function run algo?   
  def start(self):
    image = self.image.get()
    grid = self.grid.get()
    if os.path.exists(image):
        self.board = Board(self.parent, image, grid, self.win)
        self.mainFrame.pack_forget()
        self.board.pack()


  # define browse image function:
  def browse(self):
      self.image.set(tkinter.filedialog.askopenfilename(title="Select Image", filetypes=(("png file","*.png" ), ("jpg File", "*.jpg"))))

  def win(self, moves):
    self.board.pack_forget()
    self.winText.set('You are win after {0} moves'.format(moves))
    self.winFrame.pack()

  def playAgain(self):
    self.winFrame.pack_forget()
    self.mainFrame.pack()

if __name__ == "__main__":
  root=Tk()
  Main(root)
  root.mainloop()
