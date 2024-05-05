import os
import textwrap
import tkinter as tk
from PIL import Image, ImageFont, ImageDraw, ImageEnhance
from tkinter import filedialog, Button, ttk
from math import floor

#constants
W, H = (304, 405)
white_color = (255,255,255)
black_color = (0,0,0)
titleSize, subtitleSize = (50, 30)
titleH, subtitleH = (H*25/91, H*54/91)
lineWidthTitle, lineWidthSubt = (13, 25) #max characters per row

color = black_color

#file browsing
def browseFiles():
    global filename
    global path
    viewBtn["state"] = "disabled"
    path = filedialog.askopenfilename(initialdir = __file__,
                                          title = "Choose file")
    fileLabel.configure(text="Chosen file: " + path)
    filename = os.path.basename(path)
    filename = os.path.splitext(filename)[0]

# change padding filling color
def checkbutton_clicked():
    global color
    v = checkbutton_value.get()
    if v == 1:
        color = white_color
        colorLabel.configure(text="(Padding fill is now white)")
    else:
        color = black_color
        colorLabel.configure(text="(Padding fill is now black)")

#editing foto
def compute():

    #open pic
    image = Image.open(path)
    imW, imH = image.size
    
    padding_left = floor((W-imW)/2)
    padding_top = floor((H-imH)/2)
    
    # add paddings if the image is too small
    if padding_left > 0:
        new_img = Image.new(image.mode, (W, imH), color)
        new_img.paste(image, (padding_left, 0))
        image = new_img
        imW = W
    
    if padding_top > 0:
        new_img = Image.new(image.mode, (imW, H), color)
        new_img.paste(image, (0, padding_top))
        image = new_img
        imH = H
    
    # crop image at the center if too large
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
fileBtn = ttk.Button(window, text = "Choose file", command = browseFiles)
fileBtn.grid(column=0, row=0, columnspan=1, sticky=tk.W, padx=5, pady=5)

fileLabel = ttk.Label(window, text = "")
fileLabel.grid(column=1, row=0, sticky=tk.E, padx=5, pady=5)

# title input
titleLabel = ttk.Label(window, text="Title: ")
titleLabel.grid(column=0, row=1, sticky=tk.W, padx=5, pady=5)
titleTextArea = ttk.Entry(window)
titleTextArea.grid(column=1, row=1, sticky=tk.W, padx=5, pady=5)
titleTextArea.focus()

#subtitle input
subtitleLabel = ttk.Label(window, text="Subtitle: ")
subtitleLabel.grid(column=0, row=2, sticky=tk.W, padx=5, pady=5)
subtitleTextArea = ttk.Entry(window)
subtitleTextArea.grid(column=1, row=2, sticky=tk.W, padx=5, pady=5)

# padding checkbox
checkbutton_value = tk.BooleanVar()
checkbutton = ttk.Checkbutton(
    text="White fill",
    variable=checkbutton_value,
    command=checkbutton_clicked
)
checkbutton.grid(column=0, row=3, sticky=tk.W, padx=5, pady=5)
colorLabel = ttk.Label(window, text="(Padding fill is now black)")
colorLabel.grid(column=1, row=3, sticky=tk.W, padx=5, pady=5)

# show the bottom line
goBtn = ttk.Button(window, text="GO", command = compute)
goBtn.grid(column=0, row=4, sticky=tk.W, padx=5, pady=5)

resLabel = ttk.Label(window, text = "")
resLabel.grid(column=1, row=4, sticky=tk.W, padx=5, pady=5)

viewBtn = ttk.Button(window, text="Open result", command = open_pic)
viewBtn["state"] = "disabled"
viewBtn.grid(column=1, row=4, sticky=tk.E, padx=5, pady=5)

# spin
window.mainloop()
