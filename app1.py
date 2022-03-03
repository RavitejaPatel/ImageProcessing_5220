from flask import Flask
import werkzeug
werkzeug.cached_property = werkzeug.utils.cached_property
import flask.scaffold
flask.helpers._endpoint_from_view_func = flask.scaffold._endpoint_from_view_func
#import flask_restful
from flask_restplus import Api, Resource,reqparse
from werkzeug.datastructures import FileStorage
from flask import Flask, flash, request, redirect, url_for, render_template,send_from_directory
import urllib.request
import os
from werkzeug.utils import secure_filename
from PIL import Image,ImageOps
import cv2
import numpy as np 
from flask import send_file

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static'
APP_ROOT = os.path.dirname(os.path.abspath(__file__))

api = Api(app)
upload_parser = api.parser()
upload_parser.add_argument('file', 
                           location='files',
                           type=FileStorage)
@api.route('/upload/')
@api.expect(upload_parser)
class UploadDemo(Resource):
    def post(self):
        args = upload_parser.parse_args()
        file = args.get('file')
        print(file.filename)
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return "Uploaded file is " + file.filename
parser = reqparse.RequestParser()
parser.add_argument('mode', help='Specify your mode')
parser.add_argument('filename',help='Specify your mode' )

@api.route('/flip/')
class FlipDemo(Resource):
    @api.doc(parser=parser)
    def post(self):
        args = parser.parse_args()
        mode= args.get('mode')
        filename = args.get('filename')
        print(filename)
        #filename = request.files['image']

        # open and process image
        #print(request.form)
        #print(filename)
        #filename=filename.split("/")
        #filename=filename[2]
        #print(filename)
        target = os.path.join(APP_ROOT,"static\\")
        #print("bye")
        #print(target)
        destination = "".join([target, filename])
        #print("bye1")

        img = Image.open(destination)
        #print("bye2")

        if mode == 'horizontal':
            img = img.transpose(Image.FLIP_LEFT_RIGHT)
        elif mode == 'vertical':
            img = img.transpose(Image.FLIP_TOP_BOTTOM)
        elif mode == 'left':
            img = img.rotate(90)
        elif mode == 'gs':
            img = ImageOps.grayscale(img)
        elif mode == 'tl':
            #MAX_SIZE = (500, 500)
            #img.thumbnail(MAX_SIZE)
            img=cv2.imread(destination)
            h,w=img.shape[0:2]
            base_size=h+20,w+20,3
            base=np.zeros(base_size,dtype=np.uint8)
            cv2.rectangle(base,(0,0),(w+20,h+20),(0,128,0),30) # really thick white rectangle
            base[10:h+10,10:w+10]=img # this works
            nd_array=base
            nd_array=cv2.cvtColor( nd_array, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(nd_array)
            #print("hi")
        else:
            img = img.rotate(-90)

        # save and return image
        destination = "".join([target, 'temp.png'])
        if os.path.isfile(destination):
            os.remove(destination)
        img.save(destination)

        #return display_image('temp.png')
        filename = secure_filename("temp.png")
        return filename
@api.route('/view')
class viewDemo(Resource):
    @api.response(200, 'Image returned.')
    def get(self):
        target = os.path.join(APP_ROOT,"static\\")
        return send_from_directory(target,"temp.png")
if __name__ == '__main__':
    app.run()
