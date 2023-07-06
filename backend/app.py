from flask import Flask, request, render_template
from flask_cors import CORS
import traceback
import time
import numpy as np
import cv2
from ultralytics import YOLO


app = Flask(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

# YOLOv8 model
model = None


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
    except:
        print("Error happened when reading image!")
        traceback.print_exc()
        return "Unsupported image!", 400

    # step 2: prediction
    try:
        results = model(img)
    except:
        print("Error happened during prediction!")
        traceback.print_exc()
        return "Prediction server error!", 500

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
    except:
        print("Error happened when prepare output!")
        traceback.print_exc()
        return "Internal server error!", 500

    return ret


if __name__ == "__main__":

    # load YOLOv8 model
    model = YOLO('yolov8m.pt')  # load pretrained YOLOv8 model

    app.run(host='0.0.0.0', port=11280, debug=False)


