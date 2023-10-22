# YOLOV8 API
## DESCRIPTION
Detect object in image using yolov8


## REQUIREMENTS (TESTED)
- Python 3.8
## Code structure
```bash
├── config              # config file for project
├── model               # store models for project
├── src    
│   ├── yolov8_object.py       # yolov8 api
│   │
│   ├── status_file.py           # function to check status system file
├── main.py             # here is implement REST API
└── README.md           # guidline for develop
└── requirements.txt    # requirements to set up project
    
```
## INSTALLATION
    1. Create virtual environment in anaconda:
        ```
        conda create --name "yolov8" python=3.8
        ```
    2. Activate environment
        ```
        conda activate "yolov8"
        ```
    3. Install library:
        ```
        pip install -r requirements.txt
        ```
 - If using GPU, please install pytorch-gpu: https://pytorch.org

## HOW TO RUN

### Run API server:
```
uvicorn main:app
```
### Run ENCRYPT FILE
```
encryptoenv -a "TIME_SLEEP=180" "LIMIT_IMAGE=20" -E
```
if you want to change config time_sleep and limit_image, you remove env folder and run this command again.
## BACKLOG
## FURTHER IMPROVEMENT
## DEPLOYMENT