#encoding: utf-8
'''
同一张图上复制小的已有的目标
'''
import os
import cv2
import random
from PIL import Image
from lxml import etree, objectify
import xml.etree.ElementTree as ET

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

def getXmls(root_folder):
    return [k for k in os.listdir(root_folder) if k.endswith('xml')==True]

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
        E.name(anno['class_name']),  #根目录内容
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

def parseXml(xml_path):
    tree = ET.parse(xml_path)
    root = tree.getroot()

    basic_info = dict()

    #folder = root.find('folder').text
    name = root.find('filename').text
    size = root.find('size')
    img_w = int(size.find('width').text)
    img_h = int(size.find('height').text)
    img_depth = int(size.find('depth').text)
    #basic_info['src']=folder
    basic_info['filename'] = name
    basic_info['width'] = img_w
    basic_info['height'] = img_h
    basic_info['channel'] = img_depth

    class_loc=dict()
    for obj in root.iter('object'):
        cls = obj.find('name').text
        if cls not in class_loc.keys():
            class_loc[cls]=list()
        xmlbox = obj.find('bndbox')
        x1 = int(float(xmlbox.find('xmin').text))
        x2 = int(float(xmlbox.find('xmax').text))
        y1 = int(float(xmlbox.find('ymin').text))
        y2 = int(float(xmlbox.find('ymax').text))
        xmin=min(x1, x2)
        ymin=min(y1, y2)
        xmax=max(x1, x2)
        ymax=max(y1, y2)
        x1=max(0, xmin)
        y1=max(0, ymin)
        x2=min(img_w, xmax)
        y2=min(img_h, ymax)
        class_loc[cls].append([x1,y1,x2,y2])

    return basic_info,class_loc

def parseXmlOne(xml_name,xml_folder, img_folder,dst_folder):
    #try:
    if True:
        xml_abspath = os.path.join(xml_folder, xml_name)
        basic_info, parts = parseXml(xml_abspath)
        assert len(parts) != 0,"##{} has no objects##".format(xml_name)

        img_name = xml_name.replace('xml', 'jpg')
        img_abspath = os.path.join(img_folder, img_name)
        #if not os.path.exists(img_abspath):
            #img_abspath = img_abspath.replace('jpg', 'JPG')
        img = Image.open(img_abspath)
        img_w = basic_info['width']
        img_h = basic_info['height']

        dst_name = img_name
        basic_info['folder'] = 'paste'
        basic_info['filename'] = dst_name
        anno_tree = writeXmlRoot(basic_info)
        jpg_path = os.path.join(dst_folder, dst_name)
        w_list = list()
        h_list = list()
        for obj, locs in parts.items():  # 扩充roi区域并生成新xml文件
            for idx, loc in enumerate(locs):
                xmin, ymin, xmax, ymax = loc
                w_box = xmax - xmin
                h_box = ymax - ymin
                w_list +=list(range(xmin, xmax))
                h_list +=list(range(ymin, ymax)) #已经有logo的区域
        img_w_list = list(range(img_w))
        img_h_list = list(range(img_h))
        w_list = list(set(img_w_list) - set(w_list))
        h_list = list(set(img_h_list) - set(h_list))
        num_paste = 10
        step = 30

        num_paste = min((min(len(w_list), len(h_list))/step), num_paste) #最少复制数量
        w_list_pst = list()
        h_list_pst = list()
        for i in list(range(int(len(w_list)/step) - 1)):
            w_list_pst.append(random.sample(w_list[i*step:(i+1)*step], 1))
        for j in list(range(int(len(w_list)/step))):
            h_list_pst.append(random.sample(h_list[i * step:(i + 1) * step], 1))


            # img_cover = Image.new('RGB', (w_box, h_box), (255, 255, 255)) #覆盖原区域
            # img.paste(img_cover, (xmin, ymin))
            # logo_path = random.sample(logos, 1)[0]
            # img_logo = Image.open(logo_path)
            # #img_logo = img_logo.resize((w_box, h_box))
            # logo_name = os.path.basename(logo_path).split('.')[0]
            # logo_id = labels.index(logo_name)
            #
            # max_edge = max(w_box, h_box)
            # min_edge_logo = min(img_logo.width, img_logo.height)
            # ratio_logo = img_logo.width * 1.0/img_logo.height
            # if min_edge_logo == img_logo.width: #logo的短边覆盖原标注区域的场边
            #     logo_new_width = max_edge
            #     logo_new_height = int(logo_new_width*1.0 / ratio_logo)
            # else:
            #     logo_new_height = max_edge
            #     logo_new_width = int(logo_new_height * ratio_logo)
            #
            # img_logo = img_logo.resize((logo_new_width, logo_new_height))
            # #img_cover = Image.new('RGB', (w_box, h_box), (255, 255, 255))
            # #img.paste(img_cover, (xmin, ymin))
            # img.paste(img_logo, (xmin, ymin), img_logo.split()[-1])
            #
            # object = dict()
            # object['class_name'] = logo_id #更新标注label为logo_id
            # object['bndbox'] = list()
            # object['bndbox'] = [xmin, ymin, xmin+logo_new_width, ymin+logo_new_height]
            # anno_tree.append(writeXmlSubRoot(object, bbox_type='xyxy'))
        img.save(jpg_path)
        writeXml(anno_tree, os.path.join(dst_folder, dst_name.replace('jpg', 'xml')))
    #except:
    else:
        print ('##{} error##', xml_name)

def getAllFiles(folder):
    rtn = list()
    for sub_folder, _, imgs in os.walk(folder):
        for img in imgs:
            rtn.append(os.path.join(sub_folder, img))
    return rtn

if __name__=='__main__':
    xml_folder = 'crop_xml'
    img_folder = 'crop_img'
    dst_folder = 'cropImg'

    logo_folder = 'select'
    logos = getAllFiles(logo_folder)

    xmls = getXmls(xml_folder)
    task_start(xmls, 1000, xml_folder, img_folder, dst_folder)
    exit()

    for xml_name in xmls:
        xml_abspath = os.path.join(xml_folder, xml_name)
        basic_info, parts = parseXml(xml_abspath)
        assert len(parts) != 0, "##{} has no objects##".format(xml_name)

        img_name = xml_name.replace('xml', 'jpg')
        img_abspath = os.path.join(img_folder, img_name)
        if not os.path.exists(img_abspath):
            img_abspath = img_abspath.replace('jpg', 'JPG')
        img = Image.open(img_abspath)
        img_w = basic_info['width']
        img_h = basic_info['height']

        dst_name = xml_name[:-4] + "_" + str(uuid.uuid4())[:4] + '.jpg'
        basic_info['folder'] = 'cover'
        basic_info['filename'] = dst_name
        anno_tree = writeXmlRoot(basic_info)
        jpg_path = os.path.join(dst_folder, dst_name)
        for obj, locs in parts.items():  # 扩充roi区域并生成新xml文件
            for idx, loc in enumerate(locs):
                xmin, ymin, xmax, ymax = loc
                w_box = xmax - xmin
                h_box = ymax - ymin
                logo_path = random.sample(logos, 1)[0]
                img_logo = Image.open(logo_path)
                img_logo = img_logo.resize((w_box, h_box))
                logo_name = os.path.basename(logo_path).split('.')[0]
                logo_id = labels.index(logo_name)

                img.paste(img_logo, (xmin, ymin), img_logo.split()[-1])

                object = dict()
                object['class_name'] = logo_id  # 更新标注label为logo_id
                object['bndbox'] = list()
                object['bndbox'] = [xmin, ymin, xmax, ymax]
                anno_tree.append(writeXmlSubRoot(object, bbox_type='xyxy'))
        img.save(jpg_path)
        writeXml(anno_tree, os.path.join(dst_folder, dst_name.replace('jpg', 'xml')))

