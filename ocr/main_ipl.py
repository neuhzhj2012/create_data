#encoding: utf-8
import os, cv2
import uuid
import random

import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageFilter
from load_ttf import MYFONT
from get_content import CONT

from skimage import util

def addNoise(img_pil, mode='gaussian'):
    ''':arg
    mode: gaussian, salt, pepper, s & p, speckle
    '''
    img = np.array(img_pil)
    noise_img = util.random_noise(img, mode=mode)
    plt.subplot(2, 3, 1), plt.title("original")
    # plt.imshow(noise_img)
    # plt.show()
    # cv2.imshow('noise',noise_img)
    # cv2.waitKey(0)
    return  Image.fromarray(noise_img.astype('uint8'), 'RGB')

if __name__ == '__main__':
    ttf_folder = 'data/font'
    dst_folder = 'rst'
    fontObj = MYFONT(ttf_folder) #字库
    contObj = CONT() #文字内容
    fonts = fontObj.getFonts()
    imgwh = [640, 480]
    h_txt_range=list(range(18, 50)) #文字高度范围

    num_create = 5 #总的图片数
    num_conts = 15 #单张图片上文字区域
    width_char = 30#单字符的宽度


    for _ in list(range(num_create)):
        #需要区分是否可重叠
        # w_list = random.sample(list(range(0, imgwh[0]-width_char)), num_conts ) #起点位置
        # h_list = random.sample(list(range(imgwh[1])), num_conts ) #造成垂直方向上字符重叠

        w_list=random.sample(list(range(int(imgwh[0] / width_char) - 1)), num_conts)
        w_list = [k * width_char for k in w_list]

        h_list=random.sample(list(range(int(imgwh[1] / width_char) - 1)), num_conts)
        h_list = [k * width_char for k in h_list]


        img_pil = fontObj.getAlphaNewImage(imgwh)
        # img_pil = addNoise(img_pil)

        # img_pil = img_pil.filter(ImageFilter.BLUR)
        for x, y in zip(w_list, h_list):
            w_cont = random.sample(list(range(x, imgwh[0]-width_char)), 1)[0] #当前文本的宽高信息
            h_cont = random.sample(h_txt_range, 1)[0]
            txt_font = random.sample(fonts, 1)[0]  #字体选择

            num_total = int(w_cont/width_char)
            num_chinese = int(num_total/2)
            num_alpha = int(num_total/5)
            num_num = num_total - num_chinese - num_alpha
            txt = contObj.getContent(w_cont/3, num_chinese, num_alpha, num_num, False)

            txt_font = random.sample(fonts, 1)[0]
            if len(txt) == 8:
                fontObj.setFontSize(txt_font, 20)
            txt_cord = fontObj.getTxtCord(txt, txt_font)
            if (imgwh[0] - x - txt_cord[2] < 0): #需要换行,此时修改起始坐标
                txt_cord = (txt_cord[0] + imgwh[0] - txt_cord[2], txt_cord[1] + y, txt_cord[2], txt_cord[3])
            else:
                txt_cord = (txt_cord[0] + x, txt_cord[1] + y, txt_cord[2], txt_cord[3])
            # print(txt_cord, txt_cord[0]+txt_cord[2], len(txt), txt)

            img_pil = fontObj.getTxtPartBase(img_pil, txt, txt_cord, txt_font)
            # img_pil.save(os.path.join(dst_folder, str(uuid.uuid4()) + '.jpg'))
            # img_pil.show()
        img_pil = addNoise(img_pil)
        img_pil.save(os.path.join(dst_folder, str(uuid.uuid4()) + '.jpg'))

