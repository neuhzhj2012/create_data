#encoding: utf-8
import os
import cv2
import gevent
import random
import numpy as np
from lxml import etree, objectify
import xml.etree.ElementTree as ET
from multiprocessing import Process
from gevent import monkey

monkey.patch_all()
classes = [str(i) for i in list(range(101))]

def colormap(rgb=False):
    color_list = np.array(
        [
            255, 0, 0,
            255, 255, 0,
            0, 0, 255,
            255, 0, 255,
            218, 112, 214,
            50, 205, 50,
            255, 192, 203,
            0, 139, 139,
            219, 112, 147,
            218, 165, 32,
            0, 255, 255,
            255, 20, 147,
            255, 165, 0,
            0, 0, 139,
            128, 0, 128,
            95, 158, 160,
            148, 0, 211,
            100, 149, 237,
            123, 104, 238,
            135, 206, 235,
            127, 255, 170,
            255, 99, 71,
            205, 133, 63,
            205, 92, 92,
            255, 215, 0,
            220, 20, 60
        ]
    ).astype(np.uint8)
    color_list = color_list.reshape((-1, 3))
    if not rgb:
        color_list = color_list[:, ::-1]
    return color_list

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

    folder = root.find('folder').text
    name = root.find('filename').text
    size = root.find('size')
    img_w = int(size.find('width').text)
    img_h = int(size.find('height').text)
    img_depth = int(size.find('depth').text)
    basic_info['src']=folder
    basic_info['filename'] = name
    basic_info['width'] = img_w
    basic_info['height'] = img_h
    basic_info['channel'] = img_depth

    class_loc=dict()
    for obj in root.iter('object'):
        cls = obj.find('name').text
        if cls not in classes :
            continue
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
    # try:
    if True:
        xml_abspath = os.path.join(xml_folder, xml_name)
        basic_info, parts = parseXml(xml_abspath)
        assert len(parts) != 0,"##{} has no objects##".format(xml_name)

        img_name = xml_name.replace('xml', 'jpg')
        img_abspath = os.path.join(img_folder, img_name)
        if not os.path.exists(img_abspath):
            img_abspath = img_abspath.replace('jpg', 'JPG')
        img = cv2.imread(img_abspath)
        img_h, img_w = img.shape[:2]

        for obj, locs in parts.items():
            for idx, loc in enumerate(locs):
                dst_name = xml_name[:-4] + "_" + str(idx) + '.jpg'
                dst_abspath = os.path.join(dst_folder, dst_name)
                x1, y1, x2, y2 = loc
                box_w = x2 - x1
                box_h = y2 - y1
                ratio = box_w * 1.0 / box_h

                crop_w = random.sample(list(range(int(img_w / 10), int(img_w / 5))), 1)[0]
                crop_h = random.sample(list(range(int(img_h / 10), int(img_h / 5))), 1)[0]

                ratio_crop = crop_w * 1.0 / crop_h
                if ratio_crop < 0.3 or ratio_crop > 5:
                    ratio_crop = ratio
                crop = min(crop_h, crop_w)
                if (crop == crop_h):
                    crop_w = int(crop * ratio_crop)
                else:
                    crop_h = int(crop * 1.0 / ratio_crop)

                w_buff = int(abs(crop_w - box_w) / 2)
                h_buff = int(abs(crop_h - box_h) / 2)
                crop_x1 = max(x1 - w_buff, 0)
                crop_x2 = min(x2 + w_buff, img_w)
                crop_y1 = max(y1 - h_buff, 0)
                crop_y2 = min(y2 + h_buff, img_h)  #裁剪位置

                xmin = x1 - crop_x1 #标注区域
                xmax = x2 - crop_x1
                ymin = y1 - crop_y1
                ymax = y2 - crop_y1


                img_crop = img[crop_y1:crop_y2, crop_x1:crop_x2, :]
                cv2.imwrite(dst_abspath, img_crop)

                basic_info['folder'] = 'crop'
                basic_info['width'] = crop_x2 - crop_x1 + 1
                basic_info['height'] = crop_y2 - crop_y1 + 1

                object = dict()
                object['class_name'] = obj
                object['bndbox'] = list()
                object['bndbox'] = [xmin, ymin, xmax, ymax]
                anno_tree = writeXmlRoot(basic_info)
                anno_tree.append(writeXmlSubRoot(object, bbox_type='xyxy'))
                writeXml(anno_tree, os.path.join(dst_folder, dst_name.replace('jpg', 'xml')))
    # except:
    else:
        print ('##{} error##', xml_name)

def process_start(xml_list,xml_folder, img_folder,dst_folder):
    tasks = []
    for idx, xmlinfo in enumerate(xml_list):
        tasks.append(gevent.spawn(parseXmlOne, xmlinfo,xml_folder, img_folder,dst_folder, ))
    gevent.joinall(tasks)  # 使用协程来执行

def task_start(filepaths, batch_size=5, xml_folder='./Annotations', img_folder='JPEGImages', dst_folder='./tmp'):  # 每batch_size条filepaths启动一个进程
    num=len(filepaths)

    if not os.path.exists(dst_folder):
        os.makedirs(dst_folder)

    for idx in range(num // batch_size):
        url_list = filepaths[idx * batch_size:(idx + 1) * batch_size]
        p = Process(target=process_start, args=(url_list,xml_folder, img_folder,dst_folder,))
        p.start()

    if num % batch_size > 0:
        idx = num // batch_size
        url_list = filepaths[idx * batch_size:]
        p = Process(target=process_start, args=(url_list, xml_folder, img_folder, dst_folder,))
        p.start()

if __name__=='__main__':
    xml_folder = '100_xml'
    img_folder = '100_img'
    dst_folder = 'cropImg'

    if not os.path.exists(dst_folder):
        os.makedirs(dst_folder)

    xmls = getXmls(xml_folder)
    #xmls = ['00043251505971_3832319_16.jpg.xml']
    cmap = colormap()

    task_start(xmls, 1000, xml_folder, img_folder, dst_folder)
    exit()
