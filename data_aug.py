import numpy as np
import random
import cv2


def draw_rect(im, cords, color=None):
    im = im.copy()
    cords = cords.reshape(-1, 4)
    if not color:
        color = [255, 255, 255]
    for cord in cords:
        pt1, pt2 = (cord[0], cord[1]), (cord[2], cord[3])
        pt1 = int(pt1[0]), int(pt1[1])
        pt2 = int(pt2[0]), int(pt2[1])
        im = cv2.rectangle(im.copy(), pt1, pt2, color, int(max(im.shape[:2]) / 200))
    return im


class RandomHorizontalFlip(object):
    def __init__(self, prob=1):
        self.prob = prob

    def __call__(self, img, bboxes=None):
        if random.uniform(0, 1) < self.prob:
            return img, bboxes
        img_center = np.array(img.shape[:2])[::-1] / 2
        img_center = np.hstack((img_center, img_center))
        img = img.astype('float64')
        if not bboxes:
            return img,bboxes
        bboxes = bboxes.astype('float64')
        img = img[:, ::-1, :]
        img = img.astype('uint8')
        if len(bboxes) == 0:
            return img, bboxes
        bboxes[:, [0, 2]] += 2 * (img_center[[0, 2]] - bboxes[:, [0, 2]])
        box_w = abs(bboxes[:, 0] - bboxes[:, 2])
        bboxes[:, 0] -= box_w
        bboxes[:, 2] += box_w

        return img, bboxes