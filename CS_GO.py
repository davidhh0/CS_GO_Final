import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
from data_aug import RandomHorizontalFlip


string = '0.jpg'

with open('train.txt') as f:
    coordinates = f.read()

my_dict = dict()
for item in coordinates.split('\n'):
    if item == '':
        continue
    key = item.split()[0].split('\\')[1].replace('.jpg', '')
    key = int(key)
    value = item.split()[1:]
    value = [tuple([int(i) for i in val.split(',')]) for val in value]
    my_dict[key] = value
t_break = 0
init = 434
for k, v in sorted(my_dict.items()):
    source = 'images\\' + str(k) + '.jpg'
    im = Image.open(source)
    only_cords = [tuple(i[:4]) for i in my_dict[k]]
    only_cords = np.array(only_cords)
    im = np.array(im)
    hor_flip = RandomHorizontalFlip(1)
    img, bboxes = hor_flip(im, only_cords)
for i in range(434):
    source = 'images\\'+ str(i) +  '.jpg'

    only_cords = [tuple(i[:4]) for i in my_dict[source]]
    only_cords = np.array(only_cords)
    im = np.array(im)
    fig, ax = plt.subplots()

    hor_flip = RandomHorizontalFlip(1)

    img, bboxes = hor_flip(im, only_cords)
    image_to_save = Image.fromarray(img)
