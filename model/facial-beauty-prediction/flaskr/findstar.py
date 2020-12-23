import cv2
import pickle
import numpy as np
import os
from flaskr import config
from flaskr.starface.utils.utils import compare_embedding

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
class_a_path = os.path.join(BASE_DIR, "data/facebank.pkl")
with open(class_a_path, 'rb') as f:
    names, face_bank = pickle.load(f)
face_model = config.face_model


def find_similar_star(path, data_path='flaskr/starImages'):
    myimg = cv2.imdecode(np.fromfile(path, dtype=np.uint8), cv2.IMREAD_COLOR)  # -1表示cv2.IMREAD_UNCHANGED
    _, _, myface, embedding = face_model(myimg)
    if len(myface) == 0:
        return None, None, config.NO_HUMAN_FACE
    if len(myface) > 1:
        return None, None, config.MULTI_FACES_DETECTED
    # 寻找最相似明星
    idx, value = compare_embedding(embedding[0], face_bank)
    starnname = names[idx]
    # 获取明星脸
    file = os.path.join(data_path, starnname, starnname + ".jpg")
    # starimg = cv2.imdecode(np.fromfile(file, dtype=np.uint8), cv2.IMREAD_COLOR)  # -1表示cv2.IMREAD_UNCHANGED
    # _, _, starface, _ = face_model(starimg)
    # # 人脸对比
    # myface = myface[0]
    # starface = starface[0]
    # h, w = starface.shape[:2]
    # myface = cv2.resize(myface, (w, h))
    # # myface = cv2.GaussianBlur(myface, ksize=(15,15), sigmaX=0)
    # result = np.hstack((myface, starface))
    return starnname, file, value


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--img", '-i', default='/Users/suyuhui/Downloads/1298381.jpg')
    args = parser.parse_args()

    star_name, compare_img, value = find_similar_star(args.img)
    if star_name is None:
        print('检测到多张人脸或未检测到人脸')
        exit(-1)
    print('与您最相似的明星为{}'.format(star_name))
    print('相似度为{}'.format(str(value)))
    cv2.imshow('compare', compare_img)
    cv2.waitKey()
    cv2.destroyAllWindows()
