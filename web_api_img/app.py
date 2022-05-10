import cv2
import flask
from flask import Flask, send_file,jsonify

#pip3 install opencv-python

app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/get_image')
def get_image():
    cam = cv2.VideoCapture(0)
    ret, frame = cam.read()
    if not ret:
        cam.release()
        return jsonify("Error")
    else:
        img_name = "opencv_frame.jpg"
        cv2.imwrite(img_name, frame)
        cam.release()
        return send_file(img_name)


app.run()