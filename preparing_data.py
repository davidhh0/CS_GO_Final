import os
import glob
with open('train.txt' , "r") as f:
    df = f.readlines()
width = 680
height = 384

for i in glob.glob('images/*.txt'):
    os.remove(i)


for image in df:
    file = image.split(' ')[0]
    if len(image.split(' ')[1:]) == 0:
        with open(f"images_text/" + file.split('\\')[-1].split('.')[0] + '.txt', "a+") as f:
            f.write('')
    for cordi in image.split(' ')[1:]:
        if cordi == '\n' or cordi == '':
            continue
        _class = cordi.split(',')[-1]
        coordinates = cordi.split(',')[:-1]
        write = _class + ' ' + ' '.join(coordinates)
        with open(f"images_text/"+file.split('\\')[-1].split('.')[0] +'.txt' , "a+") as f:
            f.write(write+'\n')