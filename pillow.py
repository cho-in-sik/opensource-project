from PIL import Image, ImageFont, ImageDraw


target_img = Image.open("latte.png")

def loadfont(fontsize=50):
	ttf = 'NotoSansKR-VariableFont_wght.ttf'
	return ImageFont.truetype(font=ttf, size=fontsize)


titlefontObj = loadfont(fontsize=200)
title_text = "The Beauty of Mountain"
out_img = ImageDraw.Draw(target_img)
out_img.text(xy=(15,15), text=title_text, fill=(237, 230, 211), font=titlefontObj)

target_img.save("/Users/choi/Desktop/clone/please.jpg")
