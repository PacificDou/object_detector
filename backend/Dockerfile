FROM python:3.10.12-slim-bookworm
RUN apt update && apt -y install build-essential 
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
RUN apt install -y ffmpeg libsm6 libxext6
CMD ["python", "app.py"]
EXPOSE 11280
