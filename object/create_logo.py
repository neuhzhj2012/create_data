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


labels = ['ABT', 'AC-Schnitzer', 'Agile-Automotive', 'ALPINA', 'Apollo', 'Arash', 'ARCFOX', 'BAC', 'Caterham', 'Conquest', 'Dacia', 'Datsun', 'DMC', 'Donkervoort', 'DS', 'Faraday Future', 'Fisker', 'FM-Auto', 'GAZ', 'GLM', 'GMC', 'GTA', 'Gumpert', 'Hennessey', 'Icona', 'Inferno', 'Italdesign', 'Jannarelly', 'Jeep', 'KTM', 'LeSEE', 'LOCAL MOTORS', 'Lorinser', 'Lucid', 'LUXGEN', 'MAGNA', 'Mahindra', 'Mazzanti', 'MELKUS', 'MINI', 'Moia', 'nanoFLOWCELL', 'NEVS', 'Noble', 'Polestar', 'Radical', 'RENOVO', 'Rezvani', 'Rimac', 'Rinspeed', 'Scion', 'SIN CARS', 'smart', 'SPIRRA', 'SSC', 'SWM斯威汽车', 'TOROIDION', 'Tramontana', 'TVR', 'Vanda Electric', 'Venturi', 'VLF-Automotive', 'WEY', 'W-Motors', 'YAMAHA', 'Zenvo', '阿尔法·罗密欧', '阿斯顿·马丁', '艾康尼克', '安凯客车', '奥迪', '巴博斯', '拜腾', '宝骏', '宝马', '宝腾', '宝沃', '保斐利', '保时捷', '北京', '北汽道达', '北汽幻速', '北汽绅宝', '北汽威旺', '北汽制造', '奔驰', '本田', '比速汽车', '比亚迪', '标致', '别克', '宾利', '宾尼法利纳', '布加迪', '昌河汽车', '昶洧', '车和家', '成功汽车', '大迪', '大发', '大众', '道奇', '电咖', '东风', '东风启辰', '东风英菲尼迪', '东南', '法拉利', '菲亚特', '丰田', '弗那萨利', '福迪汽车', '福汽新龙马', '福特', '福田', '福田乘用车', '谷歌', '观致', '光冈', '广汽传祺', '广汽吉奥', '广汽新能源', '广通客车', '国金汽车', '哈飞', '哈飞汽车', '哈弗', '海格', '海马', '汉腾汽车', '悍马', '合众', '恒天', '红旗', '华晨华颂', '华晨金杯', '华晨中华', '华凯', '华利', '华普', '华颂', '华泰', '黄海', '霍顿', '吉利帝豪', '吉利汽车', '吉利全球鹰', '吉利英伦', '佳跃', '江淮汽车', '江铃', '江铃集团轻汽', '捷豹', '捷途', '金龙', '金旅', '九龙', '君马汽车', '卡尔森', '卡升', '卡威', '卡威汽车', '开利', '开瑞', '开瑞汽车', '凯佰赫', '凯迪拉克', '凯翼', '康迪全球鹰电动汽车', '科尼赛克', '克莱斯勒中国', '坤行汽车', '拉达', '兰博基尼', '蓝旗亚', '朗世', '劳斯莱斯', '雷丁', '雷克萨斯', '雷诺', '雷诺三星', '理念', '力帆汽车', '莲花汽车', '猎豹汽车', '林肯', '铃木', '零跑汽车', '领克', '领志', '陆地方舟', '陆风汽车', '路虎', '路特斯', '绿驰', '玛莎拉蒂', '迈巴赫', '迈凯伦', '明君汽车', '摩根', '纳智捷', '南京金龙', '南京依维柯', '讴歌', '欧宝', '欧联', '帕加尼', '佩奇奥', '奇点汽车', '奇瑞', '奇瑞新能源', '祺智', '启辰', '前途汽车', '乔治·巴顿', '庆铃汽车', '日产', '荣威', '如虎', '瑞驰新能源', '瑞迈', '萨博', '赛麟', '厦门金龙', '厦门金旅', '陕汽通家', '上海', '上汽大通', '上汽集团', '上汽通用别克', '世爵', '首望', '曙光汽车', '双环', '双龙', '思铭', '斯巴鲁', '斯达泰克', '斯柯达', '斯太尔', '苏州金龙', '塔塔', '泰卡特', '泰克鲁斯·腾风', '特斯拉', '腾势', '威马汽车', '威蒙积泰', '威兹曼', '潍柴英致', '蔚来', '沃尔沃', '沃克斯豪尔', '五菱', '五十铃', '西雅特', '夏利', '现代中国', '小鹏汽车', '鑫源', '雪佛兰', '雪铁龙', '野马汽车', '一汽海马', '一汽红旗', '一汽吉林', '一汽马自达', '依维柯', '蓥石', '永源汽车', '游侠', '宇通客车', '驭胜', '御捷', '裕路', '云度', '云雀', '长安', '长安标致雪铁龙', '长安跨越', '长安铃木', '长安欧尚', '长安汽车', '长安轻型车', '长城汽车', '长江EV', '浙江卡尔森', '正道汽车', '之诺', '知豆电动车', '中兴', '众泰汽车']


if __name__ == '__main__':
    xml_folder = 'xmls'
    jpg_folder = 'jpgs'
    if not os.path.exists(xml_folder):
        os.makedirs(xml_folder)
    if not os.path.exists(jpg_folder):
        os.makedirs(jpg_folder)


    logo_folder = 'D:\\Autohome\\carlogo\\Data\\Logos_select'
    logos = getAllFiles(logo_folder)

    resolution_list = [240, 360,480,560,640,720,960,1280]
    num_list = list(range(3,7)) #水平方向上的logo数量

    for _ in list(range(790)):
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


