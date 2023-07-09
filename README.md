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

1. Local test (Python3 virtual env)
```sh
cd backend && pip install -r requirements.txt && export PORT=11280 && python app.py
```

2. Local test (docker container)
```sh
cd backend && docker build -t object_detector . && docker run --env PORT=11280 -d -p 11280:11280 --name object_detector object_detector

# on mac, use the following command instead (add option --platform linux/amd64)
cd backend && docker build --platform linux/amd64 -t object_detector . && docker run --platform linux/amd64 --env PORT=11280 -d -p 11280:11280 --name object_detector object_detector
```

3. GCP Cloud Run
```sh
cd backend && gcloud run deploy object-detector --port 11280 --cpu 2 --memory 4G --region europe-west6 --max-instances=1 --source .
```

4. Google Kubernetes Engine
```sh
cd backend
PROJECT_ID=$(gcloud config get-value project)
COMMIT_SHA="$(git rev-parse --short=7 HEAD)"

# build a container image on Artifact Registry
gcloud artifacts repositories create my-repository --repository-format=docker --location=europe-west6
gcloud builds submit --tag="europe-west6-docker.pkg.dev/${PROJECT_ID}/my-repository/object-detector:${COMMIT_SHA}" .

# create a Kubernet cluster and connect to it
gcloud container clusters create-auto mycluster --region europe-west6
gcloud container clusters get-credentials mycluster --region europe-west6

# deploy the built container
sed -i -e "s/\$PROJECT_ID/$PROJECT_ID/g" gke.yaml
sed -i -e "s/\$COMMIT_SHA/$COMMIT_SHA/g" gke.yaml
kubectl apply -f gke.yaml
```

