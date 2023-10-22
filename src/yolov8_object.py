## here is implement REST API
import cv2
import sys
import time
import json
import yaml
import numpy as np
from ultralytics import YOLO
from PIL import Image
import os
from os import listdir
import logging
from pathlib import Path
import torch
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)
with open("./config/cam_config.yaml", "r") as f:
    cam_config = yaml.safe_load(f)
SOURCES = cam_config["sources"]

logging.getLogger().setLevel(logging.ERROR)
os.environ['CURL_CA_BUNDLE'] = ''
class Yolov8Object():
    __instance__ = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if Yolov8Object.__instance__ == None:
            Yolov8Object()
        return Yolov8Object.__instance__
    
    def __init__(self):
        if Yolov8Object.__instance__ != None:
            raise Exception("Yolov8 Object is a singleton!")
        else:
            Yolov8Object.__instance__ == self
        # Load pretrained model 
        folder_model = os.path.join(os.getcwd(), 'model')
        file = os.listdir(folder_model)
        file_path = os.path.join(os.getcwd(), folder_model, file[0])
        print("*************** MODEL PATH***************", file_path)
        self.model_path = file_path
        self.yolov8_model = YOLO(self.model_path)
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        print("*************** DEVICE ***************", self.device)
        self.yolov8_model = self.yolov8_model.to(self.device)

    def detect(self, image, output_path):
        """_summary_
        """
        image = str(image)
        file_name = image.split('\\')[-1] if '\\' in image else image.split('/')[-1]
        output_folder = os.path.join(os.getcwd(), output_path + '/images')
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        output_image = file_name.split('.')[0] + '_result'
        results = self.yolov8_model(image)
        # print(results)
        object_list = []
        # # Process result list
        # if len(results[0]) == 0:
        #     return None
        for result in results:
            boxes = result.boxes
            # print(boxes)
            for box in boxes:
                result_object = {
                    'bounding_box': box.xywh.tolist(),
                    'class_name': result.names[box.cls.item()],
                    'confidence': round(box.conf[0].item(), 2)
                }
                object_list.append(result_object)
            
            # isualize image
            if len(results[0]) == 0:
                break
            im_array = result.plot()  # plot a BGR numpy array of predictions
            im = Image.fromarray(im_array[..., ::-1])  # RGB PIL image
            im.save(Path(output_folder)/f'{output_image}.jpg')  # save image
        result_data = {
            'file_name': file_name,
            'output_image': output_image,
            'object': object_list 
        }
        # folder_data = os.path.join(os.getcwd(), 'results/data'+ camera)
        folder_data = os.path.join(os.getcwd(), output_path + '/data')
        if not os.path.exists(folder_data):
            os.makedirs(folder_data)
        with open(Path(folder_data)/f'{output_image}.json', 'w', encoding='utf-8') as outfile:
            json.dump(result_data, outfile, ensure_ascii=False)
        print("*********** SUCCESSFULLY DETECTED ***********")
        return result_data

    def process_camera(self, source_path, output_path, limit_number_image, time_sleep):
        images = Path(source_path).glob('*')
        time_start = time.time()
        request_count = 0
        for image in images:
            # check if the image ends with png or jpg or jpeg
            # if (image.endswith(".png") or image.endswith(".jpg")\
            #     or image.endswith(".jpeg")):
                # display
            request_count +=1
            time_process = time.time()
            if request_count > limit_number_image:
                time.sleep(time_sleep)
                request_count = 0
                print(f"*********** SYSTEM TEMPORARILY PAUSE, WILL BE CONTINUE AFTER {str(time_sleep)}, LIMIT IMAGES:  {str(limit_number_image)}  ***********")
                result = self.detect(image, output_path)
                continue
            result = self.detect(image, output_path)
        return True
    
    def config_cam(self, cam ):
        """_summary_
        """
        print(SOURCES)
        source_path = SOURCES[cam]
        # get the path or directory
        images = Path(source_path).glob('*')
        for image in images:
            # check if the image ends with png or jpg or jpeg
            # if (image.endswith(".png") or image.endswith(".jpg")\
            #     or image.endswith(".jpeg")):
                # display
                print("path of image   ", image)
                result = self.detect(image, cam)
                print(result)
        

        return True
    

    
if __name__ == "__main__":
    start_time = time.time()
    image = '/home/ttrungkien/ttkien/side_projects/yolov8_api/data/publicpreview.jpeg'
    yolov8_object = Yolov8Object()
    result = yolov8_object.detect(image)
    print(result)
    print(time.time() - start_time)