import cv2
import numpy as np 
import matplotlib.pyplot as plt

def make_coordinate(image, line_parameters):
    slope, intercept = line_parameters
    y1 = image.shape[0]
    y2 = int(y1*(3/5))
    x1 = int((y1 - intercept)/slope)
    x2 = int((y2 - intercept)/slope)
    return np.array([x1, y1,x2, y2])

def avg_slope_intercept(image, lines):
    left_fit = []
    right_fit = []
    for line in lines:
        x1, y1, x2, y2 = line.reshape(4)
        parameters = np.polyfit((x1,x2), (y1,y2), 1)
        slope = parameters[0]
        intercept = parameters[1]
        if slope < 0:
            left_fit.append((slope, intercept))
        else:
            right_fit.append((slope, intercept))
    left_fit_avg = np.average(left_fit, axis=0)
    right_fit_avg = np.average(right_fit, axis=0)

    left_line = make_coordinate(image, left_fit_avg)
    right_line = make_coordinate(image, right_fit_avg)
    return np.array([left_line, right_line])

def canny_cvt(image):
    height = image.shape[0]
    width =  image.shape[1]
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    blur = cv2.GaussianBlur(gray, (9,9), 2.0, 2.0, 0)
    print(blur[int(height*0.8)])
    canny = cv2.Canny(blur, 0,10)
    return canny

def roi(image):
    height = image.shape[0]
    width =  image.shape[1]
    poly = np.array([
        [(1,height), (width, height), (int(width*0.8),height) , (int(width*0.2),height)]
        ])
    mask = np.zeros_like(image)
    cv2.fillPoly(mask, poly, 255)
    masked_img = cv2.bitwise_and(image, mask)
    return mask

def display_line(image, lines):
    line_image = np.zeros_like(image)
    for line in lines:
        x1, y1, x2, y2 = line.reshape(4)
        cv2.line(line_image, (x1, y1), (x2, y2), (200,0,0), 5)
    return line_image

# img = cv2.imread('/home/pi/autonomus_robo/123.png')
# lane_img = np.copy(img)
# canny_img = canny_cvt(lane_img)
# # r_img = roi(canny_img)
# # lines = cv2.HoughLinesP(r_img, 2, np.pi/180, 100, np.array([]), minLineLength=40, maxLineGap=5)
# lines = cv2.HoughLinesP(canny_img, 2, np.pi/180, 100, np.array([]), minLineLength=5, maxLineGap=5)
# avg_line = avg_slope_intercept(lane_img, lines)
# line_img = display_line(canny_img, avg_line)
# line_img = cv2.cvtColor(line_img, cv2.COLOR_BAYER_GR2RGB)
# combo_img = cv2.addWeighted(lane_img, 0.8, line_img, 1, 1)
# # cv2.imshow('result', r_img)
# cv2.imshow('canny', combo_img); cv2.waitKey(0)

cap = cv2.VideoCapture('/home/pi/autonomus_robo/123_t.mp4')
while cap.isOpened():
    _, frame = cap.read()
    canny_img = canny_cvt(frame)

    # lines = cv2.HoughLinesP(r_img, 2, np.pi/180, 100, np.array([]), minLineLength=40, maxLineGap=5)
    lines = cv2.HoughLinesP(canny_img, 2, np.pi/180, 100, np.array([]), minLineLength=5, maxLineGap=10)
    avg_line = avg_slope_intercept(frame, lines)
    line_img = display_line(canny_img, avg_line)
    line_img = cv2.cvtColor(line_img, cv2.COLOR_BAYER_GR2RGB)
    combo_img = cv2.addWeighted(frame, 0.8, line_img, 1, 1)
    
    cv2.imshow('img', combo_img)
    # cv2.imshow('casdc', canny_img)
    
    cv2.waitKey(1)