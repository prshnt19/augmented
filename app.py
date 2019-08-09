import os
from flask import Flask, render_template, request

import numpy as np
import cv2
#import os
from scipy.interpolate import UnivariateSpline

app=Flask(__name__)
'''
poll_data={
    'question':'Select Image Format of the Converted file',
    'fields':['jpg','png','bmp']
}
'''
APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@app.route("/")
def index():
    return render_template("upload1.html")

@app.route("/upload", methods=['POST'])
def upload():
    option=request.form['option']
    print(option)
    #vote=request.args.get('field')
    #print(vote)
    target=os.path.join(APP_ROOT, 'images/')
    print(target)

    if not os.path.isdir(target):
        os.mkdir(target)

    for file in request.files  .getlist("file"):
        print(file)
        filename=file.filename
        destination="/".join([target, filename])
        print(destination)
        file.save(destination)
        for f in os.listdir("./images"):
            #if f.endswith(".jpg"):
            img_rgb = cv2.imread(f)
            img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2GRAY)
            img_blur = cv2.GaussianBlur(img_gray, (21, 21), 0, 0)
            img_blend = cv2.divide(img_gray, img_blur, scale=256)

            # if available, blend with background canvas
            #if self.canvas is not None:
            #    img_blend = cv2.multiply(img_blend, self.canvas, scale=1. / 256)

            #return
            x=cv2.cvtColor(img_blend, cv2.COLOR_GRAY2RGB)
            cv2.imshow('img',x)
            cv2.waitKey(0)
            cv2.imwrite("./generated/img."+option,x)
            #print("file generated")
        for f in os.listdir("./images"):
            if f.endswith(".jpg"):
                #print("generate location")
                #print(f)
                os.remove("./images/"+f)

    return render_template("complete.html")

if __name__=="__main__":
    app.run(port=4555, debug=True)
