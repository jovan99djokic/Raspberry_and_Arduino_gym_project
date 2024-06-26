import os
from werkzeug.utils import secure_filename
from flask import request

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def upload_file(app, userPicture):
    # check if the post request has the file part
   if userPicture not in request.files:
      print('No file part')
      #return redirect(request.url)
      return 'None'
   file = request.files[userPicture]
   # If the user does not select a file, the browser submits an
   # empty file without a filename.
   if file.filename == '':
      print('No selected file')
      #return redirect(request.url)
      return 'None'
   if file and allowed_file(file.filename):
      filename = secure_filename(file.filename)
      file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
      return filename
   
def deleteFile(app, filename):
   try:
      os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
   except:
      print('File nije pronadjen')

def writeFile(id):
   file = open("static/rfid.txt", 'w')
   file.write(str(id))
   file.close()

def readFile():
   file = open("static/rfid.txt", 'r')
   id = file.read()
   file.close()
   return id