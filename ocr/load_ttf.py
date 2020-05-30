#encoding: utf-8
import os, cv2
import numpy as np
import PIL.Image as Image
import PIL.ImageFont as ImageFont
import PIL.ImageDraw as ImageDraw

class MYFONT():
    def __init__(self, font_path='data'):
        self._Deng_path = 'Deng.ttf'
        # self._Dengb_path = 'Dengb.ttf'
        self._FZYTK_path = 'FZYTK.ttf'
        self._simfang_path = 'simfang.ttf'
        self._simhei_path = 'simhei.ttf'
        self._SIMLI_path = 'SIMLI.ttf'
        # self._simsun_path = 'simsun.ttf'
        self.__loadFont__(font_path)

    def __loadFont__(self, font_path):
        self.Deng_font = ImageFont.truetype(os.path.join(font_path, self._Deng_path), 23, encoding="unic")
        self.FZYTK_font = ImageFont.truetype(os.path.join(font_path, self._FZYTK_path), 23, encoding="unic")
        self.simfang_font = ImageFont.truetype(os.path.join(font_path, self._simfang_path), 23, encoding="unic")
        self.simhei_font = ImageFont.truetype(os.path.join(font_path, self._simhei_path), 23, encoding="unic")
        self.Deng_font = ImageFont.truetype(os.path.join(font_path, self._SIMLI_path), 23, encoding="unic")

    def getFonts(self):
        return [self.Deng_font, self.FZYTK_font, self.simfang_font,self.simhei_font, self.Deng_font]

    def setFontSize(self, font, font_size=71):
        return font.font_variant(size=font_size, encoding='unic')

    def getFontSize(self, var_font):
        return var_font.size

    def getTxtCord(self, txt, font):  # 大字体的坐标信息：[x,y,w,h]
        offset = font.getoffset(txt)
        size = font.getsize(txt)
        return offset + size  # x,y,w,h

    def getNewImage(self, imgwh):
        img_w, img_h = imgwh

        # pil_img = Image.new('RGBA', (img_w, img_h), (0, 0, 0, 0))
        pil_img = Image.new('RGB', (img_w, img_h), (255, 255, 255))
        return pil_img

    def getAlphaNewImage(self, imgwh):
        img_w, img_h = imgwh

        # pil_img = Image.new('RGBA', (img_w, img_h), (255, 255, 255, 255))
        pil_img = Image.new('RGB', (img_w, img_h), (255, 255, 255))
        return pil_img

    # def getTxtPartBase(self, pil_img, txt, txt_cord, txt_font):
    def getTxtPartBase(self, txt, txt_cord, txt_font):
        '''
        将文字写在图片上，白底黑字
        :param imgwh: 目标图分辨率
        :param txt: 待写的文字list变量
        :param txt_cord: 对应坐标
        :param txt_font: 对应字体
        :return: 结果图
        '''
        pil_img = self.getAlphaNewImage((txt_cord[0] + txt_cord[2], txt_cord[1] + txt_cord[3]))
        pil_img_draw = ImageDraw.Draw(pil_img)

        # for idx in range(len(txts)):
        #     pil_img_draw.text(txt_cords[idx], txts[idx], txt_colors[idx], font=txt_fonts[idx])

        pil_img_draw.text(txt_cord, txt, (0, 0 , 0), font=txt_font)
        return pil_img

    def mergeElewithRoi(self, element, src_img, box): #合并元素至src_img图像上
        if isinstance(element, np.ndarray):
            element = Image.fromarray(cv2.cvtColor(element, cv2.COLOR_BGRA2RGBA))
        if isinstance(src_img, np.ndarray):
            src_img = Image.fromarray(cv2.cvtColor(src_img, cv2.COLOR_BGRA2RGBA))
        # src_img.paste(element, box, element.split()[-1])
        src_img.paste(element, box)
        return src_img