#encoding: utf -8
import os, uuid
import random
from PIL import Image, ImageDraw
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


def getAllFiles(folder):
    rtn = list()
    for sub_folder, _, imgs in os.walk(folder):
        for img in imgs:
            rtn.append(os.path.join(sub_folder, img))
    return rtn

def create_img_alpha(img_wh):
    img_w, img_h = img_wh
    pil_img = Image.new('RGBA', (img_w, img_h), (255, 255, 255, 0))
    return pil_img
def draw(img_pil,element, cord):
    img_w = img_pil.width
    img_h = img_pil.height
    x = cord[0]
    y = cord[1]
    # img_draw = ImageDraw.Draw(img_pil)
    img_draw = img_pil

    img_draw.paste(element, cord, element.split()[-1])
    return img_draw


labels = ['ABT', 'Agile-Automotive', 'ALPINA', 'Apollo', 'ARCFOX', 'BAC', 'Caterham', \
          'Dacia', 'Datsun', 'Donkervoort', 'Faraday Future', 'Fisker', 'FM-Auto', 'GAZ', \
          'GLM', 'GMC', 'GTA', 'Gumpert', 'Hennessey', 'Italdesign', 'Jeep', 'KTM', \
          'Lorinser', 'Lucid', 'MAGNA', 'Mazzanti', 'MELKUS', 'MINI', 'Polestar', 'RENOVO', \
          'Scion', 'SIN CARS', 'SSC', 'TOROIDION', 'TVR', 'Venturi', 'YAMAHA', 'Zenvo', \
          '阿尔法·罗密欧', '阿斯顿·马丁', '艾康尼克', '奥迪', '保斐利', '北汽制造', '奔驰', \
          '比亚迪', '布加迪', '成功汽车', '大迪', '道奇', '东风', '法拉利', '菲亚特', '丰田', \
          '福田', '哈弗', '悍马', '恒天', '红旗', '华利', '华普', '华泰', '黄海', '佳跃', \
          '江铃', '金龙', '金旅', '卡尔森', '卡升', '卡威', '开瑞', '凯佰赫', '凯翼', '兰博基尼',\
          '蓝旗亚', '朗世', '劳斯莱斯', '雷诺三星', '路虎', '路特斯', '绿驰', '玛莎拉蒂', \
          '摩根', '启辰', '日产', '荣威', '萨博', '上海', '世爵', '曙光汽车', '思铭', '斯太尔', \
          '蔚来', '沃尔沃', '五十铃', '现代中国', '鑫源', '一汽吉林', '依维柯', '正道汽车', \
          '中兴']


if __name__ == '__main__':
    xml_folder = 'xmls'
    jpg_folder = 'jpgs'
    if not os.path.exists(xml_folder):
        os.makedirs(xml_folder)
    if not os.path.exists(jpg_folder):
        os.makedirs(jpg_folder)


    logo_folder = 'C:\\Users\\huangzhongjie\\Desktop\\select'
    logos = getAllFiles(logo_folder)

    resolution_list = [240, 360,480,560,640,720,960,1280]
    num_list = list(range(3,7)) #水平方向上的logo数量

    for _ in list(range(10)):
        name = str(uuid.uuid4())
        jpg_path = os.path.join(jpg_folder, name+'.jpg')
        xml_path = os.path.join(xml_folder, name+'.xml')
        img_w, img_h = random.sample(resolution_list, 2)
        print(img_w, img_h)
        img_640_480 = create_img_alpha([img_w, img_h])

        basic_info = dict()
        basic_info['folder'] = 'create'
        basic_info['filename'] = name + '.jpg'
        basic_info['width'] = img_w
        basic_info['height'] = img_h
        basic_info['channel'] = 3
        anno_tree = writeXmlRoot(basic_info)

        num_horizon = random.sample(num_list, 1)[0]
        step = int(img_w/num_horizon)
        step = min(step, img_h)
        print(step)
        img_pil = img_640_480
        for i in list(range(int(img_h/step))):
            for j in list(range(int(img_w/step))):
                ratio = 0.8
                logo_path = random.sample(logos, 1)[0]
                img_logo = Image.open(logo_path)
                logo_w = img_logo.width
                logo_h = img_logo.height
                img_logo = img_logo.resize((int(step * ratio), int(step * ratio)))
                loc = [j * step, i * step, j * step + int(step *ratio), i * step  + int(step *ratio)]
                cord = loc[:2]
                xmin, ymin, xmax, ymax = loc
                print(i,j, loc)

                img_pil = draw(img_pil, img_logo, cord)

                logo_name = os.path.basename(logo_path).split('.')[0]
                object = dict()
                object['name'] = labels.index(logo_name)
                object['bndbox'] = list()
                object['bndbox'] = [xmin, ymin, xmax, ymax]
                anno_tree.append(writeXmlSubRoot(object, bbox_type='xyxy'))

        writeXml(anno_tree, xml_path)

        if img_pil.format == 'PNG':
            img_pil = img_pil.convert("RGB")
        if img_pil.mode =='RGBA':
            img_pil = img_pil.convert('RGB')
        img_pil.save(jpg_path)


