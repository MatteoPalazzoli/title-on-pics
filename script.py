from PIL import Image, ImageFont, ImageDraw, ImageEnhance
import textwrap

#costanti
W, H = (304, 405)
titleSize, subtitleSize = (50, 30)
titleH, subtitleH = (H*25/91, H*54/91)
lineWidthTitle, lineWidthSubt = (13, 25) #max caratteri per riga

#apertura dell'immagine e ritaglio al centro
image = Image.open(__file__+"/../photo.jpeg")
imW, imH = image.size
image = image.crop(((imW-W)/2, (imH-H)/2, (imW-W)/2+W, (imH-H)/2+H))

#scurisce
enhancer = ImageEnhance.Brightness(image)
image = enhancer.enhance(0.5)
draw = ImageDraw.Draw(image)

#titolo
text = input("AutoCarosello v1.0\nTitolo: ");
myFont = ImageFont.truetype(__file__+"/../bn.ttf", titleSize)
text = textwrap.fill(text, lineWidthTitle)
offset = 0;
for line in text.splitlines():
    w, h = draw.textsize(line, font = myFont)
    draw.text(((W-w)/2, titleH + offset), line, fill = "white", font = myFont)
    offset += titleSize

#sottotitolo
text = input("Sottotitolo: ");
myFont = ImageFont.truetype(__file__+"/../Songbird.otf", subtitleSize)
text = textwrap.fill(text, lineWidthSubt)
offset = 0;
for line in text.splitlines():
    w, h = draw.textsize(line, font = myFont)
    draw.text(((W-w)/2, subtitleH + offset), line, fill = "white", font = myFont)
    offset += subtitleSize

#salvataggio
image.save(__file__+"/../car_result.jpeg")
input("Completato.\nLa tua immagine è stata salvata con il nome di \"car_result.jpeg\".\nPremi un tasto per continuare.")