from ultralytics import YOLO
import cv2
import math 
import streamlit as st

run = st.checkbox("Run")
FRAME_WINDOW = st.image([])
cap = cv2.VideoCapture(1)
TH_CONFIDENCE = 0.1

model = YOLO("/home/henrico/Github/SAP-GPT/model/model.pt")

classNames = ["person", "bicycle", "car", "motorbike", "aeroplane", "bus", "train", "truck", "boat",
              "traffic light", "fire hydrant", "stop sign", "parkpiping meter", "bench", "bird", "cat",
              "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella",
              "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball", "kite", "baseball bat",
              "baseball glove", "skateboard", "surfboard", "tennis racket", "bottle", "wine glass", "cup",
              "fork", "knife", "spoon", "bowl", "banana", "apple", "sandwich", "orange", "broccoli",
              "carrot", "hot dog", "pizza", "donut", "cake", "chair", "sofa", "pottedplant", "bed",
              "diningtable", "toilet", "tvmonitor", "laptop", "mouse", "remote", "keyboard", "cell phone",
              "microwave", "oven", "toaster", "sink", "refrigerator", "book", "clock", "vase", "scissors",
              "teddy bear", "hair drier", "toothbrush", "glasses", "wallet",
              ]


# with open("yolo_cfg/yolov3.txt", "r") as file:  
#     classNames = file.readlines()


while run:
    success, img = cap.read()
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = model(img, stream=True)

    for r in results:
        boxes = r.boxes

        for box in boxes:
            confidence = math.ceil((box.conf[0]*100))/100

            if confidence > TH_CONFIDENCE:

                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2) # convert to int values

                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 3)

                cls = int(box.cls[0])
                print("Class name -->", classNames[cls])

                org = [x1, y1]
                font = cv2.FONT_HERSHEY_SIMPLEX
                fontScale = 1
                color = (255, 0, 0)
                thickness = 2
                org_conf = [x2, y2]

                cv2.putText(img, classNames[cls], org, font, fontScale, color, thickness)
                cv2.putText(img, f"{confidence}", org_conf, font, fontScale, color, thickness)

    FRAME_WINDOW.image(img)
