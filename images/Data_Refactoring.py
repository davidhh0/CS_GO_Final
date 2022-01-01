import glob
import os
import xml.etree.cElementTree as ET


def delete_all_text_files():
    for i in glob.glob('../images/*.xml'):
        os.remove(i)


def create_one_xml(file_name, width, height, cordi):
    root = ET.Element("annotation")
    folder = ET.SubElement(root, "folder")
    ET.SubElement(root, "filename").text = file_name
    ET.SubElement(root, "path").text = file_name
    source = ET.SubElement(root, "source")
    ET.SubElement(source, "database").text = "custom_David_Yuval"
    size = ET.SubElement(root, "size")
    ET.SubElement(size, "width").text = str(width)
    ET.SubElement(size, "height").text = str(height)
    ET.SubElement(size, "depth").text = "3"
    ET.SubElement(root, "segmented").text = "0"
    for item in cordi:
        object = ET.SubElement(root, "object")

        ET.SubElement(object, "name").text = "CT" if item[-1] == "0" else "Terrorist"
        ET.SubElement(object, "pose").text = "Unspecified"
        ET.SubElement(object, "truncated").text = "0"
        ET.SubElement(object, "difficult").text = "0"
        ET.SubElement(object, "occluded").text = "0"
        bnbox = ET.SubElement(object, "bnbox")
        ET.SubElement(bnbox, "xmin").text = item[0]
        ET.SubElement(bnbox, "ymin").text = item[1]
        ET.SubElement(bnbox, "xmax").text = item[2]
        ET.SubElement(bnbox, "ymax").text = item[3]

    tree = ET.ElementTree(root)
    tree.write(f"{file_name.split('.')[0]}.xml")


def text_to_xml():
    images = glob.glob("../images_text/*.txt")
    for image in images:

        with open(image, "r") as f:
            text = f.readlines()
            cordi = []
            if len(text) == 0:
                print(image)
                try:
                    os.remove("../images/" + image.split('\\')[-1].split('.')[0] + ".jpg")
                except:
                    pass
                continue
            for item in text:
                split = item.split(' ')
                _class = split[0]
                xmin = split[1]
                xmax = split[3]
                ymin = split[2]
                ymax = split[4]
                cordi.append([xmin, ymin, xmax, ymax, _class])
            create_one_xml(image.split('\\')[-1].split('.')[0] + '.jpg', 680, 384, cordi)


delete_all_text_files()
text_to_xml()
