#FROM ultralytics/ultralytics
FROM python:3.8.18
COPY requirements.txt requirements.txt
# Install PyPI packages
RUN --mount=type=cache,target=/root/.cache/pip python3 -m pip install --upgrade pip
RUN --mount=type=cache,target=/root/.cache/pip python3 -m pip install -r requirements.txt
RUN --mount=type=cache,target=/var/lib/apt --mount=type=cache,target=/var/cache/apt \
  DEBIANFRONTEND=noninteractive apt-get update && apt-get install -y -q libgl1
WORKDIR /usr/src/yolov8
COPY . .
CMD ["uvicorn", "main:app"]
