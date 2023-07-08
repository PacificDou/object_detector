from flask import Flask, request, render_template
from flask_cors import CORS
import traceback
import time
import numpy as np
import cv2
from ultralytics import YOLO
import os
import logging


app = Flask(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

# set logging level
logging.basicConfig(level=logging.DEBUG)

# load YOLOv8 model
model = YOLO('yolov8m.pt')  # load pretrained YOLOv8 model


@app.route("/", methods=["GET"])
def hello_world():
    return render_template('index.html')


@app.route("/api/det", methods=["POST"])
def get_detections():
    # step 1: read image data
    try:
        img_bytes = request.files.get('image').read()
        img_np = np.frombuffer(img_bytes, dtype=np.uint8)
        img = cv2.imdecode(img_np, cv2.IMREAD_COLOR)
        logging.info("input image size: " + str(img.shape))
    except:
        logging.error("Error happened when reading image!")
        traceback.print_exc()
        return "Unsupported image!", 400

    # step 2: prediction
    try:
        results = model(img)
    except:
        logging.error("Error happened during prediction!")
        traceback.print_exc()
        return "Prediction error!", 500

    # step 3: format output
    ret = []
    try:
        cls_names = results[0].names
        for box in results[0].boxes:
            # convert data format, because float32 is not JSON serializable
            xyxy = [float(x) for x in box.xyxy[0]]
            cls = int(box.cls[0])
            conf = float(box.conf[0])
            name = cls_names[int(box.cls[0])]
            ret.append({"xyxy": xyxy, "cls": cls, "conf": conf, "name": name})
        logging.info("{} objects detected".format(len(ret)))
    except:
        logging.error("Error happened when prepare output!")
        traceback.print_exc()
        return "Internal error!", 500

    return ret


if __name__ == "__main__": 
    # CAUTION: initialization of resources should be not put here (except the global variable app)
    # because when gunicorn invokes this script, the __name__ will NOT be __main__
    # ref: https://stackoverflow.com/questions/60332174/gcp-if-name-main-not-working
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 11280)), debug=False)
