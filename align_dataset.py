'''
Author: Mohsen Madani
Date: 5/31/2018
Email: mohsenando@gmail.com
'''

from eye_detector import get_eyes
from utils import rotate_img, rotate_coords
from os import listdir
from os.path import isfile, join
import cv2
import numpy as np
import math


# -- Settings :
W = 400


dataset_path = './clean_dataset/'
new_dataset_path = './align_dataset'

files = [f for f in listdir(dataset_path) if isfile(join(dataset_path, f))]


for file in files:
    image = cv2.imread(dataset_path + file)

    # Add some extra padding
    image = cv2.copyMakeBorder(image, W, W, W, W, cv2.BORDER_CONSTANT)
    try:
        left_eye, right_eye = get_eyes(image)
    except:
        continue
    if (type(left_eye) == type(True) and left_eye == False and right_eye == False):
        continue

    # -- Find slope :
    x1 = left_eye[0] + left_eye[2]/2
    x2 = right_eye[0] + right_eye[2] / 2
    y1 = left_eye[1] + left_eye[3]/2
    y2 = right_eye[1] + right_eye[3] / 2
    slope = (y2 - y1)/(x2 - x1)

    # -- Rotate :
    centerX = image.shape[1] / 2
    centerY = image.shape[0] / 2
    angle = (np.arctan(slope) / np.pi) * 180
    image = rotate_img(image, angle)
    x1 , y1 = rotate_coords(x1, y1, centerX, centerY, angle)
    x2 , y2 = rotate_coords(x2, y2, centerX, centerY, angle)




    # -- Resize :
    length = math.sqrt(math.pow(x2 - x1,2) + math.pow(y2 - y1,2))
    scale = (W / 4) / length
    image = cv2.resize(image, None, fx=scale, fy=scale)
    x1 = int(x1 * scale)
    x2 = int(x2 * scale)
    y1 = int(y1 * scale)
    y2 = int(y2 * scale)


    # -- Crop from center :
    centerX = int( ((x2 + x1) / 2) * (1))
    centerY = int(((y2 + y1) / 2) * (1))
    image = image[(centerY - int(.6*W+1)):(centerY + int(W/0.75 - .6*W+1)), int(centerX - .125*W - .375*W+1):int(centerX + .125*W + (W - .625*W))]



    # -- Save :
    new_name = join(new_dataset_path, file)
    cv2.imwrite(new_name, image)
