# Object Detection App using Ultralytics YOLOv8

This simple app illustrates how to build a object detection web service.


## Backend (Python 3)

* [Ultralytics YOLOv8](https://github.com/ultralytics/ultralytics) is used as the object detector.  
* Currently, YOLOv8-m is used, which is based on the trade off between performance and speed.
* [Flask](https://flask.palletsprojects.com/en/2.3.x/) is used as the backend framework.  
* A simple web UI is provided as the frontend, where users can upload an image, send requests to server, view visualized results.  

### APIs
1. Retrieve the web page
* URL: /
* Method: GET
* parameter: none
* return: index.html

2. Request for object detection
* URL: /api/det
* Method: POST
* parameter: image data (bytes)
* return: list of object with sample format {"xyxy": [x1, y1, x2, y2], "cls": 1, "conf": 0.96, "name": "bus""}


### Installation guide

1. Local test (better to run in a new virtual env)
```sh
cd backend
pip install -r requirements.txt
python app.py
```

2. GCP App Engine
```sh
gcloud app deploy
```

