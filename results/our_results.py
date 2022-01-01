import collections
import numpy as np

height = 416
width = 416
with open('predicted.txt') as f:
    pred = f.readlines()
pred_dict = dict()
for item in pred:
    key = item.split(' ')[0].strip()
    value = item.split(' ')[1:]
    if len(value) == 0:
        pred_dict[key] = []
    for val in value:
        if not pred_dict.get(key, None):
            pred_dict[key] = []
        box = [float(i) for i in val.split(',')[:-3]]
        x1 = int((box[0] - box[2] / 2.0) * width)
        y1 = int((box[1] - box[3] / 2.0) * height)
        x2 = int((box[0] + box[2] / 2.0) * width)
        y2 = int((box[1] + box[3] / 2.0) * height)
        pred_dict[key].append({'class': val.split(',')[-1].strip(), 'box': [x1, y1, x2, y2]})
with open('labels.txt') as f:
    labels = f.readlines()
labels_dict = dict()
for item in labels:
    key = item.split(' ')[0].strip()
    value = item.split(' ')[1:]
    for val in value:
        if not labels_dict.get(key, None):
            labels_dict[key] = []

        labels_dict[key].append({'class': val.split(',')[-1].strip(), 'box': [int(i) for i in val.split(',')[:-1]]})

labels_dict = collections.OrderedDict(sorted(labels_dict.items()))
pred_dict = collections.OrderedDict(sorted(pred_dict.items()))
num_figures_count = 0
num_figures_total = 0
num_class_count = 0
num_class_total = 0
MSE = 0
for key in labels_dict.keys():
    num_figures_count += len(labels_dict[key]) - len(pred_dict[key])
    num_figures_total += len(labels_dict[key])
    labeled_box_list = [labels_dict[key][i]['box'] for i in range(len(labels_dict[key]))]
    pred_box_list = [pred_dict[key][i]['box'] for i in range(len(pred_dict[key]))] + (
            len(labels_dict[key]) - len(pred_dict[key])) * [[0, 0, 0, 0]]

    for index, item in enumerate(pred_dict[key]):
        _class = item['class']
        try:
            labeled_class = labels_dict[key][index]['class']
            num_class_total += 1
            num_class_count += 1 if _class == labeled_class else 0
        except IndexError:
            break
    np_label = np.array(labeled_box_list)
    np_pred = np.array(pred_box_list)
    min_list = ([(abs(item - np_label)).mean(axis=1) for item in np_pred])
    error = sorted([np.min(i) for i in min_list])[:min(len(pred_dict[key]), len(labels_dict[key]))]
    MSE += sum(error)

print('Right number of figures in an image:', (num_figures_total - num_figures_count) / num_figures_total)
print('--------------------------')
print('Predicting the correct class:', (num_class_count) / num_class_total)
print('--------------------------')
print('Average distance between bounding boxes:', MSE / num_class_total)
