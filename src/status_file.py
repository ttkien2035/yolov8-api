from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess as sp
from pathlib import Path
import time
import os

class MyHandler(FileSystemEventHandler):
    def __init__(self, yolo, output_folder, limit_number_image, time_sleep):
        self.yolo = yolo
        self.output_folder = output_folder
        self.time_sleep = time_sleep
        self.limit_number_image = limit_number_image
        self.request_count = 1
    def on_any_event(self, event):
        print(event.event_type, event.src_path)

    def on_created(self, event):
        print("on_created", event.src_path)

        for _ in range(10):
            try:
                os.stat(event.src_path)
                
                if self.request_count > self.limit_number_image:
                    time.sleep(self.time_sleep)
                    print(f"*********** SYSTEM TEMPORARILY PAUSE, WILL BE CONTINUE AFTER {str(self.time_sleep)}, LIMIT IMAGES:  {str(self.request_count)}  ***********")
                    self.request_count = 1
                result = self.yolo.detect(Path(event.src_path.strip()), self.output_folder)
                self.request_count +=1
                break
            except OSError:
                time.sleep(.5)
        else:
            print("brrr!")