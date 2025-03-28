# Color detector (name from "Mantis Shrimp")
import cv2

def find_colors(image, color_range):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    color_mask = cv2.inRange(hsv, color_range[0], color_range[1])
    contours, _ = cv2.findContours(color_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    return contours