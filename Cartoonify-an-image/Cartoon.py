import cv2
import easygui 
import numpy as np 
import imageio 
import sys
import matplotlib.pyplot as plt
import os
import tkinter as tk
from tkinter import filedialog
from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image

def upto():
    root = tk.Tk()

    var = tk.StringVar(value="Memory")
    option_box = tk.OptionMenu(root, var, "Memory", "Camera")
    option_box.pack()
    
    option_box.configure(bg='pink', fg='white')

    button1 = tk.Button(root, text="Memory", command=memory)
    button1.pack()
    
    button1.configure(bg='violet')

    button2 = tk.Button(root, text="Camera", command=camera)
    button2.pack()
    button2.configure(bg='violet')

    root.mainloop()

def memory():
    Desti=easygui.fileopenbox()
    anime(Desti)
    
def camera():
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()

    cv2.imwrite('captured_image.jpg', frame)
    anime('captured_image.jpg')

    cap.release()
    cv2.destroyAllWindows()


def anime(Desti):
    atfirst = cv2.imread(Desti)
    atfirst = cv2.cvtColor(atfirst, cv2.COLOR_BGR2RGB)

    if atfirst is None:
       print("Can not find any image. Choose appropriate file")
       sys.exit()

    First = cv2.resize(atfirst, (960, 540))

    grayImage = cv2.cvtColor(atfirst, cv2.COLOR_BGR2GRAY)
    Second = cv2.resize(grayImage, (960, 540))

    smoothGray = cv2.medianBlur(grayImage, 5)
    Third = cv2.resize(smoothGray, (960, 540))

    getEdge = cv2.adaptiveThreshold(smoothGray, 255, 
        cv2.ADAPTIVE_THRESH_MEAN_C, 
        cv2.THRESH_BINARY, 9, 9)

    Fourth = cv2.resize(getEdge, (960, 540))

    colorImage = cv2.bilateralFilter(atfirst, 9, 300, 300)
    Fifth = cv2.resize(colorImage, (960, 540))

    cartoonImage = cv2.bitwise_and(colorImage, colorImage, mask=getEdge)

    Sixth = cv2.resize(cartoonImage, (960, 540))

    images=[First, Second, Third, Fourth, Fifth, Sixth]
    fig, axes = plt.subplots(3,2, figsize=(8,8), subplot_kw={'xticks':[], 'yticks':[]}, gridspec_kw=dict(hspace=0.1, wspace=0.1))
    for i, ax in enumerate(axes.flat):
        ax.imshow(images[i], cmap='gray')
        
    plt.show()

def save(Sixth, Desti):
    newName="cartoonified_Image"
    path1 = os.path.dirname(Desti)
    extension=os.path.splitext(Desti)[1]
    path = os.path.join(path1, newName+extension)
    cv2.imwrite(path, cv2.cvtColor(Sixth, cv2.COLOR_RGB2BGR))
    I = "Image saved by name " + newName +" at "+ path
    tk.messagebox.showinfo(title=None, message=I)
    
top=tk.Tk()
top.geometry('400x400')
top.title('Make your own cartoon!')
top.configure(background='pink')
label=Label(top,background='#CC6699', font=('calibri',20,'bold'))

upload=Button(top,text="Cartoonify here",command=upto,padx=30,pady=5)
upload.configure(background='#232323', foreground='white',font=('calibri',10,'bold'))
upload.pack(side=TOP,pady=160)

top.mainloop()