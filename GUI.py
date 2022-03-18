from PIL import Image, ImageFont, ImageDraw, ImageEnhance
import textwrap
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog

#costanti
W, H = (304, 405)
titleSize, subtitleSize = (50, 30)
titleH, subtitleH = (H*25/91, H*54/91)
lineWidthTitle, lineWidthSubt = (13, 25) #max caratteri per riga

#scelta del file
def browseFiles():
    global filename
    filename = filedialog.askopenfilename(initialdir = __file__,
                                          title = "Scegli la foto")
    fileLabel.configure(text="File scelto: " + filename)

#editing foto   
def compute():
    #apertura foto
    image = Image.open(filename)
    imW, imH = image.size
    image = image.crop(((imW-W)/2, (imH-H)/2, (imW-W)/2+W, (imH-H)/2+H))
    #inscurimento
    enhancer = ImageEnhance.Brightness(image)
    image = enhancer.enhance(0.5)
    draw= ImageDraw.Draw(image)
    #titolo
    text = titleTf.get()
    myFont = ImageFont.truetype(__file__+"/../bn.ttf", titleSize)
    text = textwrap.fill(text, lineWidthTitle)
    offset = 0;
    for line in text.splitlines():
        w, h = draw.textsize(line, font = myFont)
        draw.text(((W-w)/2, titleH + offset), line, fill = "white", font = myFont)
        offset += titleSize
    #sottotitolo
    text = subtitleTf.get()
    myFont = ImageFont.truetype(__file__+"/../Songbird.otf", subtitleSize)
    text = textwrap.fill(text, lineWidthSubt)
    offset = 0;
    for line in text.splitlines():
        w, h = draw.textsize(line, font = myFont)
        draw.text(((W-w)/2, subtitleH + offset), line, fill = "white", font = myFont)
        offset += subtitleSize
    #salvataggio
    image.save(__file__+"/../car_result.jpeg")
    msgbox = tk.messagebox.showinfo(title= "Operazione completata", message="La tua foto è stata salvata.")

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

btn = tk.Button(fileFrame, text = "Scegli foto", fg = "blue", command = browseFiles)
btn.pack(side = tk.LEFT)
fileLabel = tk.Label(fileFrame, text = "", width = 100, height = 4)
fileLabel.pack(side = tk.LEFT)

titleLabel = tk.Label(top, text="Titolo: ")
titleLabel.pack(side= tk.LEFT)
titleTf = tk.Entry(top)
titleTf.pack(side=tk.LEFT)

subtitleLabel = tk.Label(bot, text="Sottotitolo: ")
subtitleLabel.pack(side= tk.LEFT)
subtitleTf = tk.Entry(bot)
subtitleTf.pack(side= tk.LEFT)

tk.Button(window, text="Vai!", command = compute).pack()

window.mainloop()

