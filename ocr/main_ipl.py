#encoding: utf-8
import os
import random
from load_ttf import MYFONT
from get_content import CONT

if __name__ == '__main__':
    ttf_folder = 'data/font'
    dst_folder = 'rst'
    fontObj = MYFONT(ttf_folder) #字库
    contObj = CONT() #文字内容
    fonts = fontObj.getFonts()
    imgwh = [640, 480]
    h_txt_range=list(range(18, 50)) #文字高度范围

    num_create = 5 #总的图片数
    num_conts = 7 #单张图片上文字区域


    for _ in list(range(num_create)):
        #需要区分是否可重叠
        w_list = random.sample(list(range(imgwh[0])), num_conts ) #起点位置
        h_list = random.sample(list(range(imgwh[1])), num_conts )

        for x, y in zip(w_list, h_list):
            w_cont = random.sample(list(range(x, imgwh[0])), 1)[0] #当前文本的宽高信息
            h_cont = random.sample(h_txt_range, 1)[0]
            txt_font = random.sample(fonts, 1)[0]  #字体选择

            num_total = int(w_cont/3)
            num_chinese = int(num_total/2)
            num_alpha = int(num_total/5)
            num_num = num_total - num_chinese - num_alpha
            txt = contObj.getContent(w_cont/3, num_chinese, num_alpha, num_num, False)

            txt_font = random.sample(fonts, 1)[0]
            if len(txt) == 8:
                fontObj.setFontSize(txt_font, 20)
            txt_cord = fontObj.getTxtCord(txt, txt_font)
            img_pil = fontObj.getTxtPartBase(imgwh, txt, txt_cord, txt_font)
            # img_pil.show()
            img_pil.save(os.path.join(dst_folder, txt + '.jpg'))

    # for province in provinces: #当前省份内数据扩大10倍
    #     for alpha in contObj.get_province_altha(province) * 50: #每个城市字母下生成500个
    #         nums_3 = ''.join(random.sample(nums, 3)) #3个数字
    #         alpha_2 = ''.join(random.sample(alphas, 2)) #2个字母
    #         tmp = nums_3 + alpha_2
    #         combs_1 = ''.join(random.sample(tmp,len(tmp)))
    #
    #         nums_4 = ''.join(random.sample(nums, 4)) #4个数字
    #         alpha_1 = ''.join(random.sample(alphas, 1)) #2个字母 #1个字母
    #         tmp = nums_4 + alpha_1
    #         combs_2 = ''.join(random.sample(tmp,len(tmp)))
    #
    #         nums_5 = ''.join(random.sample(nums, 5)) #全数字
    #         tmp = nums_5 + alpha_1
    #         combs_3 = ''.join(random.sample(tmp,len(tmp)))
    #         nums_6 = ''.join(random.sample(nums, 6)) #新能源
    #         combs_4 = nums_5
    #         combs_5 = nums_6
    #         txts = [province + alpha + combs_1,province + alpha + combs_2,
    #                 province + alpha + combs_3,province + alpha + combs_4,
    #                 province + alpha + combs_5]
    #         for txt in txts:
    #             print (txt)
    #             txt_font = random.sample(fonts, 1)[0]
    #             if len(txt) == 8:
    #                 txt_font = txt_font.font_variant(size=20, encoding='unic')
    #                 # print (txt_font.size)
    #             txt_cord = fontObj.get_txt_cord(txt, txt_font)
    #             img_pil = fontObj.get_txt_part_base(imgwh, txt, txt_cord, txt_font)
    #             # img_pil.show()
    #             img_pil.save(os.path.join(dst_folder, txt + '.jpg'))
