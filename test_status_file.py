from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess as sp

class MyHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        print(event.event_type, event.src_path)

    def on_created(self, event):
        print("on_created", event.src_path)
        print(event.src_path.strip())
        # if((event.src_path).strip() == ".\test.xml"):        
        #     print("Execute your logic here!")
 
event_handler = MyHandler()
observer = Observer()
observer.schedule(event_handler, path=r'D:\ttkien2035\yolov8_api\data\cam2', recursive=False)
observer.start()


while True:
    try:
        pass
    except KeyboardInterrupt:
        observer.stop()