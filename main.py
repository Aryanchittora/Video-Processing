# Import Libraries below
from flask import Flask, render_template, request, redirect, send_file, url_for
import os
import cv2
from werkzeug.utils import secure_filename

# Define flask 
app = Flask(__name__)

# Define upload_form() and route the webapp 
@app.route('/')
def upload_form():
    return render_template('upload.html')

# Define upload_video() to get video in defined folder and route the webapp  
@app.route('/', methods=['POST'])
def upload_video():
    file = request.files['file']
    filename = secure_filename(file.filename)
    file.save(os.path.join('static/', filename))

    vid_capture = cv2.VideoCapture('static/'+filename)
    width = int(vid_capture.get(3))
    height = int(vid_capture.get(4))
    size = (width, height)
    result = cv2.VideoWriter('static/' + 'blackandwhite.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 30, size, 0)

    try:
        while True:
            status, frame_img = vid_capture.read()
            convert = cv2.cvtColor(frame_img, cv2.COLOR_BGR2GRAY)
            result.write(convert)
            video_file = 'blackandwhite.mp4'
        
    except:
        print('Completed Writing All Frames')
        print(status)
            
            
    return render_template('upload.html', filename=filename)

@app.route('/download')
def download_file():
    vid_path = 'static/blackandwhite.mp4'
    return send_file(vid_path, as_attachment=True)

# Define display_video() to Display video in defined folder and route the webapp  
@app.route('/display/<filename>')
def display_video(filename):
    return redirect(url_for('static', filename=filename))

if __name__ == "__main__":
    app.run(debug=True)
