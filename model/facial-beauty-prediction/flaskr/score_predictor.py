import numpy as np
import cv2
from flaskr import config


def detect_face(filepath):
    im0 = cv2.imread(filepath)
    if im0.shape[0] > 1280:
        new_shape = (1280, im0.shape[1] * 1280 / im0.shape[0])
    elif im0.shape[1] > 1280:
        new_shape = (im0.shape[0] * 1280 / im0.shape[1], 1280)
    elif im0.shape[0] < 640 or im0.shape[1] < 640:
        new_shape = (im0.shape[0] * 2, im0.shape[1] * 2)
    else:
        new_shape = im0.shape[0:2]
    im = cv2.resize(im0, (int(new_shape[1]), int(new_shape[0])))
    dets = config.cnn_face_detector(im, 0)
    if len(dets) == 0:
        return config.NO_HUMAN_FACE
    if len(dets) > 1:
        return config.MULTI_FACES_DETECTED
    rect = dets[0].rect
    height = rect.bottom() - rect.top()
    boundary = round(height*0.5)
    if rect.top() - boundary < 0:
        boundary = rect.top()
    if rect.bottom() + boundary >= int(new_shape[0]):
        boundary = int(new_shape[0]) - rect.bottom()
    if rect.left() - boundary < 0:
        boundary = rect.left()
    if rect.right() + boundary >= int(new_shape[1]):
        boundary = int(new_shape[1]) - rect.right()
    cropped_image = im[rect.top()-boundary:rect.bottom()+boundary,
                    rect.left()-boundary:rect.right()+boundary, :]
    resized_image = cv2.resize(cropped_image, (config.img_height, config.img_width))
    filename = filepath.split('/')[-1]
    cv2.imwrite("uploads/cropped_{}".format(filename), resized_image)
    return resized_image


def get_score(filepath):
    test_x = detect_face(filepath)
    if isinstance (test_x,int):
        return test_x
    # if not test_x.any():
    #     return None
    test_x = test_x / 255.
    test_x = test_x.reshape((1,) + test_x.shape)
    with config.graph.as_default():
        predicted = config.model.predict(test_x)
    base = predicted[0][0]
    if predicted[0][0]>=3.5:
        base = ((base-3.5)/1.5)*10
        score = 90+base
    elif base<3.5 and base>=2.5:
        base = ((3.5-base) / 1) * 30
        score = 90-base
    else:
        base = ((2.5 - base) / 2.5) * 60
        score = 60 - base
    score = round(score)
    # score = round((predicted[0][0]-5.0)*60+40)
    # if score>=100:
    #     score = 95.10
    print(str(score)+", "+str(round(predicted[0][0],2)))
    return score