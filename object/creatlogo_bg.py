#encoding: utf-8
import os
import uuid
import cv2
import random
import numpy as np
import PIL.Image as Image
import PIL.ImageDraw as ImageDraw
import xml.etree.ElementTree as ET
from lxml import etree, objectify

def writeXmlRoot(anno):
    #写基础字段
    E = objectify.ElementMaker(annotate=False)
    anno_tree = E.annotation(    #根目录
        E.folder(anno['folder']),        #根目录内容
        E.filename(anno['filename']),
        E.size(
            E.width(anno['width']),  #子目录内容
            E.height(anno['height']),
            E.depth(anno['channel'])
        ),
    )
    return anno_tree  #anno_tree.append(writeXmlSubRoot(anno))

def writeXmlSubRoot(anno, bbox_type='xyxy'):
    #增加xml的子字段
    """bbox_type: xyxy (xmin, ymin, xmax, ymax); xywh (xmin, ymin, width, height)"""
    assert bbox_type in ['xyxy', 'xywh']
    if bbox_type == 'xywh':
        xmin, ymin, w, h = anno['bndbox']
        xmax = xmin+w
        ymax = ymin+h
    else:
        xmin, ymin, xmax, ymax = anno['bndbox']
    E = objectify.ElementMaker(annotate=False)
    anno_tree = E.object(             #根目录
        E.name(anno['name']),  #根目录内容
        E.bndbox(
            E.xmin(xmin),             #子目录内容
            E.ymin(ymin),
            E.xmax(xmax),
            E.ymax(ymax)
        ),
    )
    return anno_tree

def writeXml(anno_tree, xml_name):
    etree.ElementTree(anno_tree).write(xml_name, pretty_print=True)

def getAllFilse(folder):
    rtn = list()
    for dirname, _, imgs in os.walk(folder):
        for img in imgs:
            rtn.append(os.path.join(dirname, img))
    return rtn

def crop(img, fraction_h = 0.8, fraction_w = 0.8, flag_ul=True):
    '''
    随机裁剪图
    :param img:  带alpha通道的车标图
    :param fraction_h: 宽比例
    :param fraction_w:  高比例
    :param flag_ul:  从左上角开始
    :return:
    '''
    pass

def paste(img_logo, img_bg, loc=None):
    '''
    合并图
    :param img_logo: logo图
    :param img_bg: 背景图
    :param loc: 放置位置,None or (left, top) or (left, top, right, bottom)默认None为图片左上角
    :return:
    '''
    if isinstance(img_logo, np.ndarray):
        element = Image.fromarray(cv2.cvtColor(img_logo, cv2.COLOR_BGRA2RGBA))
    if isinstance(img_bg, np.ndarray):
        img_bg = Image.fromarray(cv2.cvtColor(img_bg, cv2.COLOR_BGRA2RGBA))
    img_bg.paste(img_logo, loc, img_logo.split()[-1])
    return img_bg
def rsz(img, fraction=0.8):
    '''
    缩放
    :param img: 带alpha通道的图
    :param fraction: 等比缩放比例
    :return:
    '''
    pass

if __name__ == '__main__':
    logo_folder = 'logos' #logo alpha 图
    bg_folder = 'bgs'   #背景图
    dst_folder = 'rst'
    logos_path = getAllFilse(logo_folder)
    bgs_path = getAllFilse(bg_folder)
    num_for_each_logo = 100

    if not os.path.exists(dst_folder):
        os.makedirs(dst_folder)
    #单张背景图上贴一个logo
    basic_info = dict()
    class_loc = dict()
    flag_two = True
    for logo_path in logos_path:
        # img_logo = cv2.imread(logos_path, cv2.IMREAD_UNCHANGED)
        img_logo = Image.open(logo_path)

        flag_two = True
        for idx in np.random.choice(range(len(bgs_path)), 40, replace=False): #从中任选150个不重复的样本
            class_loc['1'] = list()
            bg_path = bgs_path[idx]
            img_bg = Image.open(bg_path)
            img_w, img_h = img_bg.size
            if np.random.randint(10, 20)%3==0:
                flag_two = False
                rst_w = np.random.choice(range(img_w/4, img_w), 1) #随机抽取k个logo,可重复
                rst_h = np.random.choice(range(img_h/4, img_h), 1)
                img_bg = img_bg.resize((rst_w, rst_h))
                img_w, img_h = img_bg.size
            start_w = img_w / 15
            start_h = img_h / 15

            img_name = 'create_'+str(uuid.uuid4())[:6] + '.jpg'
            basic_info['folder'] = 'create'
            basic_info['filename'] = img_name
            basic_info['width'] = img_w
            basic_info['height'] = img_h
            basic_info['channel'] = 3

            if flag_two: #原图放置两个logo
                for x in np.random.choice(range(start_w, img_w - start_w), 2): #从中间位置任意选择两个位置
                    for y in np.random.choice(range(start_h, img_h - start_h), 1):
                        img_tmp = img_bg.copy()
                        logo_rsz_x = np.random.choice(range(start_w/2, img_w-x), 1)
                        logo_rsz_y = np.random.choice(range(start_h/2, img_h-y), 1)
                        logo_rsz = min(logo_rsz_x, logo_rsz_y)
                        logo_tmp = img_logo.resize((logo_rsz, logo_rsz))
                        img_tmp = paste(logo_tmp, img_tmp, (x, y))
                        class_loc['1'].append([x, y, x + logo_rsz[0], y + logo_rsz[0]])
            else: #裁剪后的图放置1个logo
                for x in np.random.choice(range(start_w, img_w - start_w), 1): #从中间位置任意选择两个位置
                    for y in np.random.choice(range(start_h, img_h - start_h), 1):
                        img_tmp = img_bg.copy()
                        logo_rsz_x = np.random.choice(range(start_w/2, img_w-x), 1)
                        logo_rsz_y = np.random.choice(range(start_h/2, img_h-y), 1)
                        logo_rsz = min(logo_rsz_x, logo_rsz_y)
                        logo_tmp = img_logo.resize((logo_rsz, logo_rsz))
                        img_tmp = paste(logo_tmp, img_tmp, (x, y))
                        class_loc['1'].append([x, y, x + logo_rsz[0], y + logo_rsz[0]])

            img_tmp = img_tmp.convert('RGB')
            img_tmp.save(os.path.join(dst_folder, img_name))

            anno_tree = writeXmlRoot(basic_info)  # 基础信息

            for obj, locs in class_loc.items():  # 单个label
                for idx, loc in enumerate(locs):
                    xmin, ymin, xmax, ymax = loc
                    object = dict()
                    object['name'] = obj
                    object['bndbox'] = list()
                    object['bndbox'] = [xmin, ymin, xmax, ymax]
                    anno_tree.append(writeXmlSubRoot(object, bbox_type='xyxy'))
            xml_name = img_name.replace('.jpg', '.xml')
            writeXml(anno_tree, os.path.join(dst_folder, xml_name))
