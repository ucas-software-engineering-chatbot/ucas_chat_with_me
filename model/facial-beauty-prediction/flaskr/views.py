#coding: utf-8

from uuid import uuid4
from flask import request
from werkzeug.exceptions import RequestEntityTooLarge
from flaskr.findstar import find_similar_star
from PIL import Image
from base64 import encodebytes
from flaskr.score_predictor import get_score
import io
from flaskr import app
from flask_uploads import UploadSet, configure_uploads, IMAGES, UploadNotAllowed
from flaskr import config
import json
from flask_cors import *

photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)



@app.errorhandler(413)
@cross_origin()
@app.errorhandler(RequestEntityTooLarge)
def app_handle_413(e):
    return json.dumps({"status": "failed", "reason": "the file is too large"}),404


@app.route('/facescore', methods=['POST', 'OPTIONS'])
@cross_origin()
def facescore():
    data = {
        "status": "failed",
    }
    # # print(request.method)
    # print(request.form)
    # print(request.data)
    # print(request.method)
    # print(request.values)
    # print(request.headers)
    # print(request.args)
    # print(request.json)
    if request.method == 'POST' and 'photo' in request.files:
        # print(request.files)
        print(request.files.get('photo'))
        # try:
        filename = photos.save(request.files.get('photo'), name="{}.".format(str(uuid4())))
        score = get_score("flaskr/uploads/{}".format(filename))
        # except UploadNotAllowed:
        #     return json.dumps({"status": "failed", "reason": "the file is not a image"}),404
        # except Exception:
        #     return json.dumps({"status": "failed", "reason": "unknown"}),404
        if score == config.NO_HUMAN_FACE:
            data["reason"] = "no human faces detected"
        elif score == config.MULTI_FACES_DETECTED:
            data["reason"] = "multi faces detected"
        else:
            data["status"] = "succeed"
            data["score"] = score
            return json.dumps(data),200
    else:
        data["reason"] = "method is not post or didn't have photo in request"
    # print(data)
    return json.dumps(data),404
    # print(request)
    # return HttpResponse(json.dumps(data))




def get_response_image(image_path):
    pil_img = Image.open(image_path, mode='r') # reads the PIL image
    byte_arr = io.BytesIO()
    pil_img.save(byte_arr, format='PNG') # convert the PIL image to byte array
    encoded_img = encodebytes(byte_arr.getvalue()).decode('ascii') # encode as base64
    return encoded_img


@app.route('/starface', methods=['POST'])
@cross_origin()
def starface():
    data = {"status": "failed"}
    if request.method == 'POST' and 'photo' in request.files:
        try:
            filename = photos.save(request.files.get('photo'), name="{}.".format(str(uuid4())))
            starnname, starimg, value = find_similar_star("flaskr/uploads/{}".format(filename))
        except UploadNotAllowed:
            return json.dumps({"status": "failed", "reason": "the file is not a image"}),404
        except Exception:
            return json.dumps({"status": "failed", "reason": "unknown"}),404
        if value == config.NO_HUMAN_FACE:
            data["reason"] = "no human faces detected"
        elif value == config.MULTI_FACES_DETECTED:
            data["reason"] = "multi faces detected"
        else:
            data["status"] = "succeed"
            data["star_name"] = starnname
            data["star_image"] = get_response_image(starimg)
            data["value"] = value
            data["format"] = "PNG"
            return json.dumps(data),200
    else:
        data["reason"] = "method is not post or didn't have photo in request"
    return json.dumps(data),404


# def init_app():
#     app = Flask(__name__)
#     photos = UploadSet('photos', IMAGES)
#     app.config['UPLOADED_PHOTOS_DEST'] = 'uploads'
#     app.config['MAX_CONTENT_LENGTH'] = 15 * 1024 * 1024
#     configure_uploads(app, photos)



if __name__ == '__main__':
    # WSGIServer(('127.0.0.1', 3000), app).serve_forever()
    app.run(host="127.0.0.1", port=3000, debug=True)
