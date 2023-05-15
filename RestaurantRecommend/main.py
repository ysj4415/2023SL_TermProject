from tkinter import *

class MainGUI:
    def __init__(self):
        window = Tk()
        window.title('경기도 맛집 추천')
        self.canvas = Canvas(window,bg = 'white', width=400, height=300)
        self.canvas.pack()

        window.mainloop()

MainGUI()