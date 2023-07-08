FROM python:3.10.12-slim-bookworm
RUN apt update && apt -y install build-essential ffmpeg libsm6 libxext6
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 app:app
