import json
from flaskr import app


def testing_scoring_single_face():
    app.config['TESTING'] = True
    with app.test_client() as c:
        for i in range(1,11):
            resp = c.post('/facescore', data={'photo': open('test_data/face'+str(i)+'.jpeg', 'rb')}, follow_redirects=True)
            data = json.loads(resp.data)
            assert 100 >= data['score'] >= 0


def testing_scoring_multi_faces():
    app.config['TESTING'] = True
    with app.test_client() as c:
        for i in range(1,6):
            resp = c.post('/facescore', data={'photo': open('test_data/multifaces' + str(i) + '.jpeg', 'rb')},
                          follow_redirects=True)
            data = json.loads(resp.data)
            assert data['status'] == "failed" and data["reason"] == "multi faces detected"


def testing_scoring_no_faces():
    app.config['TESTING'] = True
    with app.test_client() as c:
        for i in range(1,6):
            resp = c.post('/facescore', data={'photo': open('test_data/noface' + str(i) + '.jpg', 'rb')},
                          follow_redirects=True)
            data = json.loads(resp.data)
            assert data['status'] == "failed" and data["reason"] == "no human faces detected"


def testing_format():
    app.config['TESTING'] = True
    with app.test_client() as c:
        resp = c.post('/facescore', data={'photo': open('test_data/file2.pdf', 'rb')},
                          follow_redirects=True)
        data = json.loads(resp.data)
        assert data['status'] == "failed" and data["reason"] == "the file is not a image"
        resp = c.post('/facescore', data={'photo': open('test_data/file1.mp3', 'rb')},
                          follow_redirects=True)
        data = json.loads(resp.data)
        assert data['status'] == "failed" and data["reason"] == "the file is not a image"

        resp = c.post('/starface', data={'photo': open('test_data/file2.pdf', 'rb')},
                          follow_redirects=True)
        data = json.loads(resp.data)
        assert data['status'] == "failed" and data["reason"] == "the file is not a image"
        resp = c.post('/starface', data={'photo': open('test_data/file1.mp3', 'rb')},
                          follow_redirects=True)
        data = json.loads(resp.data)
        assert data['status'] == "failed" and data["reason"] == "the file is not a image"



def testing_bigfile():
    app.config['TESTING'] = True
    with app.test_client() as c:
        resp = c.post('/facescore', data={'photo': open('test_data/bigfile.jpeg', 'rb')},
                          follow_redirects=True)
        data = json.loads(resp.data)
        assert data['status'] == "failed" and data["reason"] == "the file is too large"
        resp = c.post('/starface', data={'photo': open('test_data/bigfile.jpeg', 'rb')},
                      follow_redirects=True)
        data = json.loads(resp.data)
        assert data['status'] == "failed" and data["reason"] == "the file is too large"


def testing_star_face_single_face():
    app.config['TESTING'] = True
    with app.test_client() as c:
        resp = c.post('/starface', data={'photo': open('test_data/face1.jpeg', 'rb')},
                          follow_redirects=True)
        data = json.loads(resp.data)
        assert data['status'] == "succeed" \
               and data["star_name"] == "范冰冰" \
               and 0.72 <= data["value"] <= 1 \

        resp = c.post('/starface', data={'photo': open('test_data/face2.jpeg', 'rb')},
                      follow_redirects=True)
        data = json.loads(resp.data)
        assert data['status'] == "succeed" \
               and data["star_name"] == "王俊凯" \
               and 0.72 <= data["value"] <= 1

        resp = c.post('/starface', data={'photo': open('test_data/face3.jpeg', 'rb')},
                      follow_redirects=True)
        data = json.loads(resp.data)
        assert data['status'] == "succeed" \
               and data["star_name"] == "泰勒·斯威夫特" \
               and 0.72 <= data["value"] <= 1

        resp = c.post('/starface', data={'photo': open('test_data/face4.jpeg', 'rb')},
                      follow_redirects=True)
        data = json.loads(resp.data)
        assert data['status'] == "succeed" \
               and data["star_name"] == "刘诗诗" \
               and 0.72 <= data["value"] <= 1

        for i in range(5,11):
            resp = c.post('/starface', data={'photo': open('test_data/face' + str(i) + '.jpeg', 'rb')},
                          follow_redirects=True)
            data = json.loads(resp.data)
            assert data['status'] == "succeed" and 0 <= data["value"] <= 1

def testing_star_face_multi_faces():
    app.config['TESTING'] = True
    with app.test_client() as c:
        for i in range(1,6):
            resp = c.post('/starface', data={'photo': open('test_data/multifaces' + str(i) + '.jpeg', 'rb')},
                          follow_redirects=True)
            data = json.loads(resp.data)
            assert data['status'] == "failed" and data["reason"] == "multi faces detected"

def testing_star_face_no_faces():
    app.config['TESTING'] = True
    with app.test_client() as c:
        for i in range(1,6):
            resp = c.post('/starface', data={'photo': open('test_data/noface' + str(i) + '.jpg', 'rb')},
                          follow_redirects=True)
            data = json.loads(resp.data)
            assert data['status'] == "failed" and data["reason"] == "no human faces detected"
