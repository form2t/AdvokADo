from PIL import Image
from PIL import ImageFont
from PIL import ImageColor
from PIL import ImageDraw


def create_image(txt):
    image_mode = 'RGB'
    image_size = (800, 400)
    image_color = "#ffffff"
    font_size = 13
    font_color = "#000000"
    #count(exp), sum(exp), sum(gold), sum(stock), sum(hp), sum(lastHit), sum(knockout), userName
    lst = ['count', 'exp', 'gold', 'stock', 'hp', 'lastHit', 'knockout', 'userName']

    tmp = '\t'.join(lst).expandtabs(10)
    txt = txt.expandtabs(10)
    txt = tmp + '\n' + txt
    img = Image.new(mode=image_mode, size=image_size, color=image_color)
    font = ImageFont.truetype("courbd.ttf", size=font_size)

    fill = ImageColor.getrgb(color=font_color)
    draw = ImageDraw.Draw(im=img, mode=image_mode)
    draw.text(xy=(10, 10), text=txt, fill=fill, font=font,)
    img.save('result.png')


#if __name__ == '__main__':
 #   data = ["Vesknam", "38", "2698", "35", "33", "-5480", "43", "0"]
  #  str = "\t".join(data)
   # print(str)
    #create_image(str)

