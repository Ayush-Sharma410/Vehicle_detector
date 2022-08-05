import cv2
from tracker import *
import numpy as np

# Create tracker object
tracker = EuclideanDistTracker()

cap = cv2.VideoCapture("highway.mp4")

# Object detection from Stable camera
object_detector = cv2.createBackgroundSubtractorMOG2(history=200, varThreshold=350)

count_line_position=150
offset=3 #Allowable error between pixels

def centre_handle(x,y,w,h):
    x1=int(w/2)
    y1=int(h/2)
    cx=x+x1
    cy=y+y1
    return cx,cy
detections = []
number_of_light_vehicles=0
number_of_heavy_vehicles=0
while True:
    ret, frame = cap.read()
    height, width, _ = frame.shape

    # Extract Region of interest
    Region_of_interest = frame[340: 720,400: 850]

    # 1. Object Detection
    mask = object_detector.apply(Region_of_interest)
    _, mask = cv2.threshold(mask, 254, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        # Calculate area and remove small elements
        area = cv2.contourArea(cnt)
        if area > 200 and area<900:
            #cv2.drawContours(roi, [cnt], -1, (0, 255, 0), 2)
            x, y, w, h = cv2.boundingRect(cnt)

            cv2.rectangle(Region_of_interest, (x, y), (x + w, y + h), (0, 255, 0), 3)
            center = centre_handle(x, y, w, h)
            detections.append(center)
            cv2.circle(Region_of_interest, center, 4, (0, 0, 255), -1)
            cv2.line(Region_of_interest, (100, count_line_position), (800, count_line_position), (0, 255, 0), 3)
            for (x, y) in detections:
                if y > (count_line_position - offset) and y < (count_line_position + offset):
                    number_of_light_vehicles = number_of_light_vehicles + 1
                    cv2.line(Region_of_interest, (0, count_line_position), (800, count_line_position), (0, 0, 255), 3)
                    detections.remove((x, y))
           # cap = cv2.cvtColor(cap, cv2.COLOR_BGR2RGB)
        cv2.putText(Region_of_interest, 'Total light vehicles:' + str(number_of_light_vehicles), (70, 90), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255),2)


        if area > 900:
            #cv2.drawContours(roi, [cnt], -1, (0, 255, 0), 2)
            x, y, w, h = cv2.boundingRect(cnt)

            cv2.rectangle(Region_of_interest, (x, y), (x + w, y + h), (0, 255, 0), 3)
            center = centre_handle(x, y, w, h)
            detections.append(center)
            cv2.circle(Region_of_interest, center, 4, (0, 0, 255), -1)
            cv2.line(Region_of_interest, (100, count_line_position), (800, count_line_position), (0, 255, 0), 3)
            for (x, y) in detections:

                if y > (count_line_position - offset) and y < (count_line_position + offset):
                    number_of_heavy_vehicles = number_of_heavy_vehicles + 1
                    cv2.line(Region_of_interest, (100, count_line_position), (800, count_line_position), (0, 0, 255), 3)
                    detections.remove((x, y))
           # cap = cv2.cvtColor(cap, cv2.COLOR_BGR2RGB)
        cv2.putText(Region_of_interest, 'Total heavy vehicles:' + str(number_of_heavy_vehicles), (60, 20), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255),2)


    cv2.imshow("Frame", frame)
    cv2.imshow("Mask", mask)
    cv2.imshow("Region_of_interst",Region_of_interest)


    key = cv2.waitKey(10)
    if key == 27:
        break
    print(number_of_heavy_vehicles)
    print(number_of_light_vehicles)
cap.release()
cv2.destroyAllWindows()