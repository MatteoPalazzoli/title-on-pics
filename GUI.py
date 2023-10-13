from PIL import Image, ImageFont, ImageDraw, ImageEnhance
import textwrap
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog

#constants
W, H = (304, 405)
titleSize, subtitleSize = (50, 30)
titleH, subtitleH = (H*25/91, H*54/91)
lineWidthTitle, lineWidthSubt = (13, 25) #max characters per row

#file browsing
def browseFiles():
    global filename
    filename = filedialog.askopenfilename(initialdir = __file__,
                                          title = "Choose the pic")
    fileLabel.configure(text="Chosen file: " + filename)

#editing foto   
def compute():

    #open the pic
    image = Image.open(filename)
    imW, imH = image.size

    # crop to size W x H, centered
    image = image.crop(((imW-W)/2, (imH-H)/2, (imW-W)/2+W, (imH-H)/2+H))
    
    #lower the brightness to half
    enhancer = ImageEnhance.Brightness(image)
    image = enhancer.enhance(0.5)
    draw = ImageDraw.Draw(image)
    
    #title
    text = titleTf.get()
    myFont = ImageFont.truetype(__file__+"/../bn.ttf", titleSize)
    text = textwrap.fill(text, lineWidthTitle)
    offset = 0;
    for line in text.splitlines():
        (left, top, right, bottom) = draw.textbbox([0,0], text = line, font = myFont)
        draw.text(((W-(right - left))/2, titleH + offset), line, fill = "white", font = myFont)
        offset += titleSize
        
    #subtitle
    text = subtitleTf.get()
    myFont = ImageFont.truetype(__file__+"/../Songbird.otf", subtitleSize)
    text = textwrap.fill(text, lineWidthSubt)
    offset = 0;
    for line in text.splitlines():
        (left, top, right, bottom) = draw.textbbox([0,0], text = line, font = myFont)
        draw.text(((W-(right-left))/2, subtitleH + offset), line, fill = "white", font = myFont)
        offset += subtitleSize
        
    #saving
    image = image.convert('RGB');
    image.save(__file__+"/../car_result.jpeg")
    msgbox = tk.messagebox.showinfo(title= "OK", message="Your pic has been saved.")

#window
window = tk.Tk()
window.title("AutoCarousel GUI v1.0")
window.geometry("600x200")

fileFrame = tk.Frame(window)
fileFrame.pack()
top = tk.Frame(window)
bot = tk.Frame(window)
top.pack()
bot.pack()

btn = tk.Button(fileFrame, text = "Choose photo", fg = "blue", command = browseFiles)
btn.pack(side = tk.LEFT)
fileLabel = tk.Label(fileFrame, text = "", width = 100, height = 4)
fileLabel.pack(side = tk.LEFT)

titleLabel = tk.Label(top, text="Your title: ")
titleLabel.pack(side= tk.LEFT)
titleTf = tk.Entry(top)
titleTf.pack(side=tk.LEFT)

subtitleLabel = tk.Label(bot, text="Your subtitle: ")
subtitleLabel.pack(side= tk.LEFT)
subtitleTf = tk.Entry(bot)
subtitleTf.pack(side= tk.LEFT)

tk.Button(window, text="GO", command = compute).pack()

window.mainloop()

