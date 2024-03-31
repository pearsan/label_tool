# import pymongo
from flask import Flask, jsonify, request, session, sessions, flash, send_file, url_for, send_from_directory
# from pymongo import message
# from werkzeug.security import check_password_hash, generate_password_hash
# from werkzeug.utils import secure_filename
# from torchvision.utils import save_image, make_grid

#from flask_jwt_extended import JWTManager, jwt_required, create_access_token
#from pymongo import MongoClient
#from bson.objectid import ObjectId
# from flask_jwt_extended import JWTManager, jwt_required, create_access_token
# from pymongo import MongoClient
# from bson.objectid import ObjectId
import os
#import gridfs
# from detectors.DB import *
# import easyocr
import numpy as np
import cv2
from PIL import Image
import io
import uuid
import json
from flask import Flask, jsonify, request, session, sessions, flash, send_file, url_for, send_from_directory, redirect, render_template
import os
import urllib.request
# from werkzeug.utils import secure_filename
import json
import cv2
from PIL import Image
import io
#import matplotlib.pyplot as plt
import numpy as np
import copy
#from tool import *
#from normalize import Normalize
from collections import defaultdict
import json
import config


# app = Flask(__name__)

# @app.route('/')
# def home():
#     return render_template('index.html')

basedir = os.path.abspath(os.path.dirname(__file__))
uploads_path = os.path.join(basedir, 'uploads')

app = Flask(__name__)
app.config.from_object(config)

app.config['UPLOAD_FOLDER'] = 'static/uploads/tt4'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
#normalize_obj = Normalize()


def image_to_byte_array(image:Image):
  imgByteArr = io.BytesIO()
  image.save(imgByteArr, format=image.format)
  imgByteArr = imgByteArr.getvalue()
  return imgByteArr


basedir = os.path.abspath(os.path.dirname(__file__))
uploads_path = os.path.join(basedir, 'uploads')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def add_JSON_detect(d,box):
    region = {
        "shape_attributes": {
          "name": "polygon",
          "all_points_x": [
            float(box[0][0]),
            float(box[1][0]),
            float(box[2][0]),
            float(box[3][0])
          ],
          "all_points_y": [
            float(box[0][1]),
            float(box[1][1]),
            float(box[2][1]),
            float(box[3][1])
          ]
        },
        "region_attributes": {
          "name": d
        }
      }
    return region

def to_JSON(regions,img_name,size):


    res = {
        img_name: {
            "filename": img_name,
            "size": size,
            "regions": regions,
            "file_attributes": {}
          }
        }

    return res

def get_box_img(box, image):
    img = Image.open(io.BytesIO(image))
    width, height = img.size
    img = np.array(img)
    b = np.array(box, dtype=np.int16)
    xmin = np.min(b[:, 0])
    ymin = np.min(b[:, 1])
    xmax = np.max(b[:, 0])
    ymax = np.max(b[:, 1])
    crop_img = img[ymin:ymax, xmin:xmax, :].copy()

    return crop_img, xmin, ymin, xmax, ymax, height, width


@app.route('/api/images/upload', methods=['GET', 'POST'])
def upload():
    file = request.files['inputFile']
    path = os.path.join(app.config['UPLOAD_FOLDER'], (file.filename).split('.')[0])
    if os.path.isdir(path) == False:
        os.mkdir(path)
    file.save(os.path.join(path, file.filename))
    return jsonify({'message': 'Upload file successful'}), 201


@app.route('/api/images/uploads/<image_file>', methods=['GET'])
def get_img(image_file):
    """Get image preview, return image"""
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], image_file)
    if (os.path.exists(os.path.join(file_path, f'{image_file}.png'))):
        print("File has existed")
    return send_from_directory(file_path, f'{image_file}.png', as_attachment=True)

@app.route('/api/images/crop/<image_file>', methods=['GET', 'POST'])
def crop_characters(image_file):
    """ Crop characters from image which are annotated
        params:
        --image_file:
    """
    # Read image
    folder_path = os.path.join(app.config['UPLOAD_FOLDER'], image_file)
    image_file_path = os.path.join(folder_path, image_file +'.png')
    img = Image.open(image_file_path)

    if request.method == 'GET':
        # Read anntations from json
        image_file_json = os.path.join(folder_path, image_file +'.json')
        with open(image_file_json, 'r') as f:
            data = f.read()
        page_annotation = json.loads(data)
        bboxes = page_annotation["bboxes"] 

        # Crop all characters in image
        for box in bboxes:
            x_min, y_min, x_max, y_max = box['x_min'], box['y_min'], box['x_max'], box['y_max']
            print(x_min, y_min, x_max, y_max)

            img_box_crop = img.crop((x_min, y_min, x_max, y_max))
            characters_path = os.path.join(folder_path, f'characters/img_{box["id"]}')
            
            if os.path.exists(characters_path) == False:
                os.mkdir(characters_path)   
            print(characters_path)
            img_box_crop.save(os.path.join(characters_path, f'img_{box["id"]}.png'))
            json_path = os.path.join(characters_path, f'img_{box["id"]}.json')
            property_of_image = {"has_threshold":False, "size": img_box_crop.shape, "no_cnts":-1, "threshold":127}
            with open(json_path, 'w') as json_file:
                json.dump(property_of_image, json_file)

    
    elif request.method == 'POST':
        box = request.json
        print("Drawboxes", box)
        x_min, y_min, x_max, y_max = box['x_min'], box['y_min'], box['x_max'], box['y_max']
        print(x_min, y_min, x_max, y_max)

        img_box_crop = img.crop((x_min, y_min, x_max, y_max))
        characters_path = os.path.join(folder_path, f'characters/img_{box["id"]}')

        if os.path.exists(characters_path) == False:
            os.mkdir(characters_path)   
        print(characters_path)
        img_box_crop.save(os.path.join(characters_path, f'img_{box["id"]}.png'))
        json_path = os.path.join(characters_path, f'img_{box["id"]}.json')
        property_of_image = {"has_threshold":False, "size": img_box_crop.shape, "no_cnts":-1, "threshold":127}
        with open(json_path, 'w') as json_file:
            json.dump(property_of_image, json_file)
    return jsonify({'message: crop successfull'}), 200


@app.route('/api/image/getlabel/<image_file>', methods=['GET'])
def getlabel(image_file):
    """ Get label and annonation of characters in image from file json 
        params: 
        --image_file: <str>
    """

    file_path = os.path.join(app.config['UPLOAD_FOLDER'], image_file + '/' + image_file +'.json')
    with open(file_path, 'r') as f:
        data = f.read()
    obj = json.loads(data)
    return jsonify(message="successful", data=obj), 200


@app.route('/api/image/label/<image_file>', methods=['POST'])
def saveLabel(image_file):
    data = request.json['data']
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], image_file + '/' + image_file + '.json')
    with open(file_path, 'w') as f:
        json.dump(data, f)

    return jsonify(message="Save successfull", data=data), 200

@app.route('/api/images', methods=['GET'])
def getAllImages():
    images = []
    for file in os.listdir(app.config['UPLOAD_FOLDER']):
        d = os.path.join(app.config['UPLOAD_FOLDER'], file)
        if os.path.isdir(d):
            print(d)
            temp = {
            "id": file,
            "user_id": 1,
            "filename": file,
            }
            images.append(temp)
    return jsonify(message="successful", data=images), 200

if __name__ == '__main__':
    # app.run(port=config.PORT, debug=config.DEBUG)
    port = int(os.environ.get('PORT', 5001))
    app.run(debug=True, host='0.0.0.0', port=port)
