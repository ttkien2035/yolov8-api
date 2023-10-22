## here is implement REST API
import cv2
import yaml
import json
import numpy as np
from PIL import Image
from io import BytesIO
from typing import Union
from pydantic import BaseModel
import threading
import itertools 
from typing_extensions import Annotated
from fastapi.responses import JSONResponse
from fastapi import FastAPI, Depends, File, UploadFile, Form
from pathlib import Path
from src.yolov8_object import Yolov8Object
from src.status_file import MyHandler
from watchdog.observers import Observer
import time
import cv2
import os
from encryptoenv.EnvFile import EnvFile
from os import environ
EnvFile().create_environment_variables()

is_visualize = True
def read_imagefile(file) -> Image.Image:
    image = Image.open(BytesIO(file))
    return image

with open("./config/cam_config.yaml", "r") as f:
    doc_config = yaml.safe_load(f)
STATUS = doc_config["status"]
time_sleep =int(environ["TIME_SLEEP"]) # time to pause service after detecting number of images
limit_number_image = int(environ["LIMIT_IMAGE"]) # number of images
print("*************** TIME_SLEEP***************", time_sleep)
print("*************** LIMIT_IMAGE***************", limit_number_image)
app = FastAPI(title='Yolov8 Detector')


yolov8 = Yolov8Object()  # create an instance of the Singleton class
observer = Observer()
# Define the default route 
@app.get("/")
async def root(singleton_instance: Yolov8Object = Depends(lambda: yolov8)):
    return {"message": "Welcome to Yolov8 Detector!", "instance_id": id(singleton_instance)}

# input is image link
@app.post("/yolov8/det")
async def extracting(folder_path: str = Form(..., description = "folder path of camera images"),
                    output_folder: str = Form(..., description = "output folder where you want to save result")
                    ):

    info = {}
    result = {}
    event_handler = MyHandler(yolov8, output_folder, limit_number_image, time_sleep)
    try:
        if not folder_path:
            result = JSONResponse(status_code = 474, 
                    content = {"status_code": '474', 
                            "message": STATUS['474'],
                            "result": info
                            })
        else:
            result_status  = yolov8.process_camera(folder_path, output_folder, limit_number_image, time_sleep)
            observer.schedule(event_handler, path=Path(folder_path), recursive=False)
            observer.start()
            while True:
                try:
                    time.sleep(0.3)
                except KeyboardInterrupt:
                    observer.stop()
            result = JSONResponse(status_code = 200, 
                    content = {"status_code": '200',
                            "message": 'succesful',
                            "result": output_folder
                            })
        return result
    except Exception as er:
        time.sleep(0.5)
        return result


# # input is image link
# @app.post("/yolov8/det")
# async def extracting(camera_list: list = Form(..., description = "cam 1, cam 2")
#                     ):

#     info = {}
#     result = {}
#     if not camera_list:
#         result = JSONResponse(status_code = 474, 
#                 content = {"status_code": '474', 
#                         "message": STATUS['474'],
#                         "result": info
#                         })
#     else:
#         threads = []
#         camera_list = camera_list[0].split(',')
#         for camera in camera_list:
#             # config thread
#             threads.append(threading.Thread(target=yolov8.config_cam, args=(camera,)))
#         # Start all threads
#         for thread in threads:
#             thread.start()
#         # Wait for all to complete
#         for thread in threads:
#             thread.join()
#     return result
