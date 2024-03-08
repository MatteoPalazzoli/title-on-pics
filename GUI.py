from PIL import Image, ImageFont, ImageDraw, ImageEnhance
import textwrap
import tkinter as tk
from tkinter import filedialog
from tkinter import Button
from tkinter import ttk
import os

#constants
W, H = (304, 405)
titleSize, subtitleSize = (50, 30)
titleH, subtitleH = (H*25/91, H*54/91)
lineWidthTitle, lineWidthSubt = (13, 25) #max characters per row

#file browsing
def browseFiles():
    global filename
    global path
    viewBtn["state"] = "disabled"
    path = filedialog.askopenfilename(initialdir = __file__,
                                          title = "Choose the pic")
    fileLabel.configure(text="Chosen pic: " + path)
    filename = os.path.basename(path)
    filename = os.path.splitext(filename)[0]

#editing foto
def compute():

    #open pic
    image = Image.open(path)
    imW, imH = image.size
    image = image.crop(((imW-W)/2, (imH-H)/2, (imW-W)/2+W, (imH-H)/2+H))
    
    #lower the brightness
    enhancer = ImageEnhance.Brightness(image)
    image = enhancer.enhance(0.5)
    draw = ImageDraw.Draw(image)
    
    #put the title
    text = titleTextArea.get()
    myFont = ImageFont.truetype(__file__+"/../bn.ttf", titleSize)
    text = textwrap.fill(text, lineWidthTitle)
    offset = 0;
    for line in text.splitlines():
        (left, top, right, bottom) = draw.textbbox([0,0], text = line, font = myFont)
        draw.text(((W-(right - left))/2, titleH + offset), line, fill = "white", font = myFont)
        offset += titleSize
        
    #put the subtitle
    text = subtitleTextArea.get()
    myFont = ImageFont.truetype(__file__+"/../Songbird.otf", subtitleSize)
    text = textwrap.fill(text, lineWidthSubt)
    offset = 0;
    for line in text.splitlines():
        (left, top, right, bottom) = draw.textbbox([0,0], text = line, font = myFont)
        draw.text(((W-(right-left))/2, subtitleH + offset), line, fill = "white", font = myFont)
        offset += subtitleSize
        
    #save the image
    image = image.convert('RGB');
    image.save(__file__+"/../car_"+filename+".jpeg")
    #msgbox = tk.messagebox.showinfo(title= "OK", message="Your pic has been saved.")
    resLabel.configure(text="File saved.")
    viewBtn["state"] = "normal"

def open_pic():
    #view the image
    image = Image.open(__file__+"/../car_"+filename+".jpeg")
    image.show()

#open a window
window = tk.Tk()
window.title("AutoCarousel")
window.geometry("450x200")

#layout
window.columnconfigure(0, weight=1)
window.columnconfigure(1, weight=2)

# view the window elements

#file choice
fileBtn = ttk.Button(window, text = "Choose photo", command = browseFiles)
fileBtn.grid(column=0, row=0, columnspan=1, sticky=tk.W, padx=5, pady=5)

fileLabel = ttk.Label(window, text = "")
fileLabel.grid(column=1, row=0, sticky=tk.E, padx=5, pady=5)

# title input
titleLabel = ttk.Label(window, text="Your title: ")
titleLabel.grid(column=0, row=1, sticky=tk.W, padx=5, pady=5)
titleTextArea = ttk.Entry(window)
titleTextArea.grid(column=1, row=1, sticky=tk.W, padx=5, pady=5)

#subtitle input
subtitleLabel = ttk.Label(window, text="Your subtitle: ")
subtitleLabel.grid(column=0, row=2, sticky=tk.W, padx=5, pady=5)
subtitleTextArea = ttk.Entry(window)
subtitleTextArea.grid(column=1, row=2, sticky=tk.W, padx=5, pady=5)

# focus
titleTextArea.focus()

# show the bottom line
goBtn = ttk.Button(window, text="GO", command = compute)
goBtn.grid(column=0, row=3, sticky=tk.W, padx=5, pady=5)#.pack(side = tk.LEFT)

resLabel = ttk.Label(window, text = "")
resLabel.grid(column=1, row=3, sticky=tk.W, padx=5, pady=5) #.pack(side = tk.LEFT)

viewBtn = ttk.Button(window, text="Open result", command = open_pic)
viewBtn["state"] = "disabled"
viewBtn.grid(column=1, row=3, sticky=tk.E, padx=5, pady=5) #.pack(side = tk.RIGHT)

# spin
window.mainloop()
