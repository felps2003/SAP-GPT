import torch
import torchvision
import cv2

model = torch.load("model.pt")

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    image = torchvision.transforms.Resize((416, 416))(frame)

    predictions = model(image)

    detections = torchvision.ops.nms(predictions, 0.45, iou_threshold=0.5)
    for detection in detections:
        x1 = detection[0]
        y1 = detection[1]
        x2 = detection[2]
        y2 = detection[3]
        class_id = detection[4]
        confidence = detection[5]
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(frame, f"Class: {class_id}, Confidence: {confidence}", (x1, y1 + 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    cv2.imshow("Image", frame)

    key = cv2.waitKey(1)
    if key == ord("q"):
        break

cap.release()