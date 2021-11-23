from tkinter import *
from tkinter.ttk import Entry, Button, OptionMenu
from PIL import Image, ImageTk
import random
import tkinter.filedialog
import os


class Tiles():
    def __init__(self,  grid_row, grid_col):
        self.tiles = []
        self.grid_col = grid_col
        self.grid_row = grid_row
        self.gap = None 
        self.moves = 0

    def add(self, tile):
        self.tiles.append(tile)

    def getTile(self, *pos):
        for tile in self.tiles:
            if tile.pos == pos:
                return tile

    def getTileAroundGap(self):
        gRow, gCol = self.gap.pos
        return self.getTile(gRow, gCol - 1), self.getTile(gRow, gCol + 1), self.getTile(gRow - 1, gCol), self.getTile(
            gRow + 1, gCol)

    def changeGap(self, tile):
        try:
            gPos = self.gap.pos
            self.gap.pos = tile.pos
            tile.pos = gPos
            self.moves += 1
        except:
            pass

 
    def slide(self, key):
        left, right, top, down = self.getTileAroundGap()
        if key == 'Up': self.changeGap(down)
        if key == 'Down': self.changeGap(top)
        if key == 'Right': self.changeGap(left)
        if key == 'Left': self.changeGap(right)
        if key == 's': self.shuffle()
        self.show()


    def shuffle(self):
        random.shuffle(self.tiles)
        i = 0  
        for row in range(self.grid_row):
            for col in range(int(self.grid_col)):
                self.tiles[i].pos = (row, col)
                i += 1
    def shup(self):
        i = 0 
        for row in range(self.grid_row):
            for col in range(int(self.grid_col)):
                self.tiles[i].pos = (row, col)
                i += 1
    def show(self):
        for tile in self.tiles:
            if self.gap != tile:
                tile.show()


    def setGap(self, index):
        self.gap = self.tiles[index]

    def isCorrect(self):

        for tile in self.tiles:
            if not tile.isCorrectPos(): return False
        return True


class Tile(Label):
    def __init__(self, parent, tileImage, pos):
        Label.__init__(self, parent, image=tileImage)

        self.image = tileImage
        self.pos = pos
        self.curPos = pos

    def show(self):
        self.grid(row=self.pos[0], column=self.pos[1])

    def isCorrectPos(self):
        return self.pos == self.curPos


class Board(Frame):
    MAX_BOARD_SIZE = 500

    def __init__(self, parent, image, grid_row, grid_col,win,sf, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.grid_col = grid_col
        self.grid_row = grid_row
        self.win = win
        self.image = self.openImage(image)
        self.menu()
        self.tileSize = self.image.size[0] / self.grid_row
        self.tiles = self.createTiles()

        self.tiles.show()
        self.bindKeys()
        self.shuffle(sf)
    def getTiles(self):
        return self.tiles
    def shuffle(self,sf):
        if sf ==True:
            self.tiles.shuffle()
            self.tiles.show()
    def openImage(self, image):
        image = Image.open(image)  
        imageSize = min(image.size)  
        if imageSize > self.MAX_BOARD_SIZE:  
            image = image.resize((self.MAX_BOARD_SIZE, self.MAX_BOARD_SIZE), Image.ANTIALIAS) 
        if image.size[0] > image.size[1]:
            image = image.crop((0, 0, image.size[1], image.size[1]))
        elif image.size[0] < image.size[1]:
            image = image.crop((0, 0, image.size[0], image.size[0]))
        return image


    def bindKeys(self):
        self.bind_all('<Key-Up>', self.slide)
        self.bind_all('<Key-Down>', self.slide)
        self.bind_all('<Key-Left>', self.slide)
        self.bind_all('<Key-Right>', self.slide)
        self.bind_all('<s>', self.slide)

    def slide(self, event):
        self.tiles.slide(event.keysym)
        
        if self.tiles.isCorrect():
            self.win(self.tiles.moves)
    def donothing(self):
        a=100
    def menu(self):
        a =100
         
    def createTiles(self):

        tiles = Tiles(self.grid_row,self.grid_col/2)  
    
        for row in range(self.grid_row):
            for col in range(int(self.grid_col/2)):

                x0 = col * self.tileSize
                y0 = row * self.tileSize
                x1 = x0 + self.tileSize
                y1 = y0 + self.tileSize
                tileImage = ImageTk.PhotoImage(self.image.crop((x0, y0, x1, y1)))
                tile = Tile(self, tileImage, (row, col))  
                tiles.add(tile)
        tiles.setGap(-1)
  
        for row in range(self.grid_row):
            i = 0
            for col in range(int(self.grid_col/2),self.grid_col):

                x0 = i * self.tileSize
                i+=1
                y0 = row * self.tileSize
                x1 = x0 + self.tileSize
                y1 = y0 + self.tileSize
                img = self.image.crop((x0, y0, x1, y1))
                tileImage = ImageTk.PhotoImage(img)
                tile = Tile(self, tileImage, (row, col)) 
                tile.show()

        return tiles


class Main():
    def __init__(self, parent):
        self.parent = parent
        self.image = StringVar()
        self.winText = StringVar()
        self.grid = IntVar()
        self.createWidgets()
        self.sf = False
    def createWidgets(self):

        self.mainFrame = Frame(self.parent)
        Label(self.mainFrame, text='Sliding Puzzle', font=('ink Free', 65)).pack(padx=10, pady=10)  
        frame = Frame(self.mainFrame)
        Label(frame, text='Images',font=('ink Free',15)).grid(sticky=W)
        Entry(frame, textvariable=self.image, width=50).grid(row=0, column=1, padx=10, pady=10)
        Button(frame, text='Browse', command=self.browse).grid(row=0, column=2, pady=10, padx=10)

        Label(frame, text='Grid',font=('ink Free',15)).grid(sticky=W)
        OptionMenu(frame, self.grid, *[2, 3, 4, 5, 6, 7, 8, 9, 10]).grid(row=1, column=1, padx=10, pady=10, sticky=W)
        frame.pack(padx=10, pady=10)

        Button(self.mainFrame, text='Start',command=self.start).pack(padx=10, pady=10)
        Button(self.mainFrame, text='Exit', command=self.exit).pack(padx=10, pady=10)
        Button(self.mainFrame, text='Shuffle', command=self.shuffle).pack(padx=20, pady=10)
        self.mainFrame.pack()
        self.board = Frame(self.parent)
        self.winFrame = Frame(self.parent)
        Label(self.winFrame, textvariable=self.winText, font=('', 50), padx=10, pady=10)
        Label(self.winFrame, text='you win',font=('ink Free',50),fg='red').pack(padx=10, pady=10)
        Button(self.winFrame, text='Play Again', command=self.playAgain).pack(padx=10, pady=10)
    def start(self):
        self.root = Toplevel()
        image = self.image.get()
        self.mainFrame1 = Frame(self.root)
        grid_col, grid_row = self.grid.get(), self.grid.get()
        if os.path.exists(image):
            self.board = Board(self.root, image, grid_row, grid_col*2, self.win,self.sf)
            self.mainFrame1.pack_forget()
            self.board.pack()

        self.root.mainloop()
    def exit(self):
      root.destroy()
    def shuffle(self):
        self.sf = True
        self.board.shuffle(self.sf)
        self.sf = False


    def browse(self):
        self.image.set(tkinter.filedialog.askopenfilename(title="Select Image",initialdir="../", filetypes=(("png file","*.png" ), ("jpg File", "*.jpg"))))

    def win(self, moves):
        self.board.pack_forget()
        self.winFrame.pack()

    def playAgain(self):
        self.board.pack_forget()
        self.winFrame.pack_forget()       
        self.mainFrame.pack()


if __name__ == "__main__":
    root = Tk()
    root.title('GR6')
    Main(root)
    root.mainloop()
