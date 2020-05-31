import os
import random
from captcha.image import ImageCaptcha,ImageFilter

def random_color(start, end, opacity=None):
    red = random.randint(start, end)
    green = random.randint(start, end)
    blue = random.randint(start, end)
    if opacity is None:
        return (red, green, blue)
    return (red, green, blue, opacity)

if __name__ == '__main__':
    dst_folder = 'rst'
    num = [str(i) for i in range(10)] + [chr(i) for i in range(65, 91)]
    # num = [str(i) for i in range(9)] + [chr(i) for i in range(97, 122)]
    print (num)
    num_create = 5 #总的图片数
    num_txt = 4 #单个验证码数量

    # image = ImageCaptcha(width=120, height=40, font_sizes=(25,28))
    imag = ImageCaptcha( height=70, font_sizes=(50,58))
    for i in list(range(num_create)):
        txt = ''.join(random.sample(num, num_txt)) #验证码内容
        # image.generate(txt)
        # image.write(txt,os.path.join(dst_folder, txt+'.jpg'))
        # continue
        background = random_color(238, 255)
        color = random_color(10, 200, random.randint(220, 255))
        background = (255, 255, 255)
        color = (5, 39, 175)
        im = imag.create_captcha_image(txt, color, background)
        # im.create_noise_dots(im, color)
        imag.create_noise_curve(im, color)
        image = im.filter(ImageFilter.SMOOTH)
        im.save(os.path.join(dst_folder, txt+'.jpg'))