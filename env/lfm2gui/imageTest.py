import tkinter as tk
import tkinter.font as tkFont
import tkinter.ttk as ttk
from tkinter import PhotoImage
from PIL import Image, ImageTk, ImageOps
import os

def getStarIcon(i):
    return PhotoImage(file=".\\env.\\lfm2gui\\icons\\" + str(i) + "stars.png")
def addImage(list, i):
    #add photo to list as unique item
    list.append(getStarIcon(i).subsample(shrink,shrink))
    #place photo via list address list[i] so vars do not overwrite
    tk.Label(window, image=list[i]).place(x=0, y=(200/shrink*i))

#GUI CREATE
shrink = 3
window = tk.Tk()
#window.geometry('334x403') #xy window size string
window.geometry('1000x100') #xy window size string
window.title("Star Icons")

#create treeview
columnNames = ["0", "1", "2", "3", "4", "5"]
treeviewStars = ttk.Treeview(window, columns=columnNames)#,show ="headings")

for column in columnNames:
    treeviewStars.heading(column, text=column)

treeviewStars.pack(fill=tk.BOTH, expand=True)

#load images
size = (200, 20)
with Image.open(".\\env.\\lfm2gui\\icons\\0stars.png") as img0stars, \
    Image.open(".\\env.\\lfm2gui\\icons\\1stars.png") as img1stars, \
    Image.open(".\\env.\\lfm2gui\\icons\\2stars.png") as img2stars, \
    Image.open(".\\env.\\lfm2gui\\icons\\3stars.png") as img3stars, \
    Image.open(".\\env.\\lfm2gui\\icons\\4stars.png") as img4stars, \
    Image.open(".\\env.\\lfm2gui\\icons\\5stars.png") as img5stars:

    stars0 = ImageTk.PhotoImage(ImageOps.contain(img0stars, size))
    stars1 = ImageTk.PhotoImage(ImageOps.contain(img1stars, size))
    stars2 = ImageTk.PhotoImage(ImageOps.contain(img2stars, size))
    stars3 = ImageTk.PhotoImage(ImageOps.contain(img3stars, size))
    stars4 = ImageTk.PhotoImage(ImageOps.contain(img4stars, size))
    stars5 = ImageTk.PhotoImage(ImageOps.contain(img5stars, size))

#image creation and placement loop
#images = []
#for i in range(6):
#    addImage(images, i)
treeviewStars.insert(parent="", \
                     index=tk.END, \
                        values=(stars0, stars1, stars2, stars3, stars4, stars5), \
                            tags=("tag1"))
#for column in columnNames:
#    treeviewStars.insert(parent="", index=tk.END, image = stars1)
treeviewStars.tag_configure("tag1", image=stars0)


#main loop
window.mainloop()
