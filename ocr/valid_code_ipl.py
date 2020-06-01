import os
import random
from PIL.ImageDraw import Draw
from captcha.image import ImageCaptcha,ImageFilter

def random_color(start, end, opacity=None):
    red = random.randint(start, end)
    green = random.randint(start, end)
    blue = random.randint(start, end)
    if opacity is None:
        return (red, green, blue)
    return (red, green, blue, opacity)

def create_noise_curve(image, color):
    w, h = image.size
    x1 = random.randint(0, int(w / 5))
    x12 = random.randint(int(w / 4), w - int(w / 4))
    x2 = random.randint(w - int(w / 5), w)
    y1 = random.randint(int(h / 5), h - int(h / 5))
    y1 = random.randint(0, int(h / 5))
    y12 = random.randint(int(h / 4), h - int(h / 4))
    y2 = random.randint(y1, h - int(h / 5))
    points = [x1, y1, x2, y2]
    points1 = [x1, y1, x12, y12]
    points2 = [x12, y12, x2, y2]
    # points = [x1, y1, x12, y12, x2, y2]
    # print(points)
    end = random.randint(20, 20)
    start = random.randint(20, 20)
    start, end=-20, 170
    Draw(image).arc(points, start, end, fill=color,width=3)
    # Draw(image).arc(points2, start, end, fill=color)
    # Draw(image).line(points, fill=color,joint='curve')
    return image

if __name__ == '__main__':
    dst_folder = 'rst'
    num = [str(i) for i in range(10)] + [chr(i) for i in range(65, 91)] + [chr(i) for i in range(97, 123)]
    # num = [str(i) for i in range(9)] + [chr(i) for i in range(97, 122)]
    print (num)
    num_create = 2000 #总的图片数
    num_txt = 4 #单个验证码数量

    # image = ImageCaptcha(width=120, height=40, font_sizes=(25,28))
    img = ImageCaptcha( height=70, fonts=['data/Deng.ttf','data/simfang.ttf','data/simhei.ttf'], font_sizes=(30,43))
    img = ImageCaptcha( height=70, fonts=['data/Deng.ttf'], font_sizes=(40,43))
    img = ImageCaptcha( height=70, font_sizes=(30,38))
    for i in list(range(num_create)):
        txt = ''.join(random.sample(num, num_txt)) #验证码内容
        # image.generate(txt)
        # image.write(txt,os.path.join(dst_folder, txt+'.jpg'))
        # continue
        background = random_color(238, 255)
        color = random_color(10, 200, random.randint(220, 255))
        background = (255, 255, 255)
        background_noise = (241, 241, 215)
        color = (95, 137, 180)
        im = img.create_captcha_image(txt, color, background)
        img.create_noise_dots(im, background_noise,width=5)
        # imag.create_noise_curve(im, color)
        im = create_noise_curve(im, color)
        # print(txt)
        # im = im.filter(ImageFilter.SMOOTH)
        im.save(os.path.join(dst_folder, txt+'.jpg'))