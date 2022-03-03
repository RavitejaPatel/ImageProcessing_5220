#app.py
from flask import Flask, flash, request, redirect, url_for, render_template,send_from_directory
import urllib.request
import os
from werkzeug.utils import secure_filename
from PIL import Image,ImageOps
import cv2
import numpy as np 
app = Flask(__name__)
 
UPLOAD_FOLDER = 'static'
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
print(APP_ROOT)
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
 
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
 
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
     
 
@app.route('/')
def home():
    print(APP_ROOT)

    return render_template('index.html')
 
@app.route('/upload', methods=['GET','POST'])
def upload_image():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        #print('upload_image filename: ' + filename)
        #flash('Image successfully uploaded and displayed below')
        return render_template('index.html', filename=filename)
    else:
        flash('Allowed image types are - png, jpg, jpeg, gif')
        #return redirect(request.url)
        return render_template('error.html', message="Mode not supported- 404 error "), 404
    
 
@app.route("/flip", methods=["POST"])
def flip():
     filename = request.form['image']
     filename=filename.split("/")
     filename=filename[2]
     print(filename)
     target = os.path.join(APP_ROOT,"static\\")
    #print("bye")
    #print(target)
     destination = "".join([target, filename])
    #print("bye1")
     img = Image.open(destination)
    #print("bye2")
     if 'horizontal' in request.form['mode']:
        mode = 'horizontal'
        img = img.transpose(Image.FLIP_LEFT_RIGHT)
      
     elif 'vertical' in request.form['mode']:
        mode = 'vertical'
        img = img.transpose(Image.FLIP_TOP_BOTTOM)
       
     
     destination = "".join([target, 'temp.png'])
     if os.path.isfile(destination):
        os.remove(destination)
    
     img.save(destination)
 #return display_image('temp.png')
     filename = secure_filename("temp.png")
     return render_template('index.html', filename=filename)



@app.route("/rotatedir", methods=["POST"])
def rotatedir():
    # retrieve parameters from html form
    filename = request.form['image']
    filename=filename.split("/")
    filename=filename[2]
    target = os.path.join(APP_ROOT,"static\\")
    destination = "".join([target, filename])
    img = Image.open(destination)

    if 'left' in request.form['mode']:
        mode = 'left'
        img = img.rotate(90)

    elif 'right' in request.form['mode']:
        mode = 'right'
        img = img.rotate(-90)

    destination = "".join([target, 'temp.png'])
    if os.path.isfile(destination):
        os.remove(destination)
    img.save(destination)
 #return display_image('temp.png')
    filename = secure_filename("temp.png")
    return render_template('index.html', filename=filename)



@app.route("/gstn", methods=["POST"])
def gstn():
    # retrieve parameters from html form
    filename = request.form['image']
    filename=filename.split("/")
    filename=filename[2]
    target = os.path.join(APP_ROOT,"static\\")
    destination = "".join([target, filename])
    img = Image.open(destination)

    if 'gs' in request.form['mode']:
        mode = 'gs'
        img = ImageOps.grayscale(img)

    elif 'tl' in request.form['mode']:
        mode = 'tl'
        img=cv2.imread(destination)
        h,w=img.shape[0:2]
        base_size=h+20,w+20,3
        base=np.zeros(base_size,dtype=np.uint8)
        cv2.rectangle(base,(0,0),(w+20,h+20),(0,128,0),30) # really thick white rectangle
        base[10:h+10,10:w+10]=img # this works
        nd_array=base
        nd_array=cv2.cvtColor( nd_array, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(nd_array)

    else:
        return render_template("error.html", message="Mode not supported (vertical - horizontal)"), 400
    
    # save and return image
    destination = "".join([target, 'temp.png'])
    if os.path.isfile(destination):
        os.remove(destination)
    img.save(destination)

    #return display_image('temp.png')
    filename = secure_filename("temp.png")
    return render_template('index.html', filename=filename)


@app.route("/rotate", methods=["POST"])
def rotate():
    # retrieve parameters from html form
    angle = request.form['angle']
    filename = request.form['image']
    # open and process image
    filename=filename.split("/")
    filename=filename[2]
    # open and process image
    target = os.path.join(APP_ROOT, 'static//')
    destination = "".join([target, filename])

    img = Image.open(destination)
    img = img.rotate(-1*int(angle))

    # save and return image
    destination = "".join([target, 'temp.png'])
    if os.path.isfile(destination):
        os.remove(destination)
    img.save(destination)

    filename = secure_filename("temp.png")
    return render_template('index.html', filename=filename)

@app.route("/crop", methods=["POST"])
def crop():
    # retrieve parameters from html form
    x1 = int(request.form['x1'])
    y1 = int(request.form['y1'])
    
    
    filename = request.form['image']
    #filename = request.files['image']

    # open and process image
    #print(request.form)
    #print(filename)
    filename=filename.split("/")
    filename=filename[2]

    # open image
    target = os.path.join(APP_ROOT, 'static//')
    destination = "".join([target, filename])

    img = Image.open(destination)
    # crop image and show
    if x1>0 and y1>0:
        img = img.resize((y1, x1))
        
        # save and return image
        destination = "".join([target, 'temp.png'])
        if os.path.isfile(destination):
            os.remove(destination)
        img.save(destination)
        #return send_image('temp.png')
        #return display_image('temp.png')
        filename = secure_filename("temp.png")
        return render_template('index.html', filename=filename)
    else:
        return render_template("error.html", message="dimensions not valid"), 400
    return '', 204



@app.route('/display/<filename>',methods=["GET"])
def display_image(filename):
    print('display_image filename: ' + filename)
    #send_from_directory("static", filename)
    #render_template('index.html', filename=filename)
    return redirect(url_for('static', filename=filename), code=301)
    

 
if __name__ == "__main__":
    app.run()
