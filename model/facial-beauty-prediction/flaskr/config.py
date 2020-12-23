from flaskr.starface.face_model import FaceModel
from keras.models import load_model
import dlib
import tensorflow as tf

img_height, img_width, channels = 350, 350, 3

face_model = FaceModel()

model_path = "./flaskr/data/mmod_human_face_detector.dat"
cnn_face_detector = dlib.cnn_face_detection_model_v1(model_path)

model = load_model("./flaskr/mse-15-0.1046.h5")

graph = tf.get_default_graph()

NO_HUMAN_FACE = -1
MULTI_FACES_DETECTED = -2
