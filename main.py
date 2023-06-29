import cv2

thres = 0.45  # Threshold to detect object

classNames = []
classFile = 'coco.names'
with open(classFile, 'rt') as f:
    classNames = f.read().rstrip('\n').split('\n')

configPath = 'ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'
weightsPath = 'frozen_inference_graph.pb'

net = cv2.dnn_DetectionModel(weightsPath, configPath)
net.setInputSize(320, 320)
net.setInputScale(1.0 / 127.5)
net.setInputMean((127.5, 127.5, 127.5))
net.setInputSwapRB(True)

videoFile = r'D:\sampl vid\UNM Surveillance Video of Shooting.mp4'  # Add an 'r' before the string to treat it as a raw string

cap = cv2.VideoCapture(videoFile)
if not cap.isOpened():
    print("Error opening video file")

while True:
    success, img = cap.read()
    if not success:
        break

    classIds, confs, bbox = net.detect(img, confThreshold=thres)

    if len(classIds) != 0:
        for classId, confidence, box in zip(classIds.flatten(), confs.flatten(), bbox):
            classId = int(classId) - 1  # Convert classId to integer and subtract 1 for 0-based indexing
            className = classNames[classId] if classId >= 0 and classId < len(classNames) else 'Unknown'
            cv2.rectangle(img, box, color=(0, 255, 0), thickness=2)
            cv2.putText(img, className.upper(), (box[0]+10, box[1]+30),
                        cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(img, str(round(confidence*100, 2)), (box[0]+200, box[1]+30),
                        cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow('Video Object Detection', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to exit
        break

cap.release()
cv2.destroyAllWindows()
