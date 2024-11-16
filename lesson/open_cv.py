import numpy as np
import cv2
import matplotlib.pyplot as plt


def default():
    camera_name = "Camera???"
    cv2.namedWindow(camera_name, cv2.WINDOW_NORMAL)
    camera = cv2.VideoCapture(0)

    while camera.isOpened():
        ret, frame = camera.read()
        cv2.imshow(camera_name, frame)
        
        key = cv2.waitKey(1)
        if key == ord('q'):
            break
        
    camera.release()
    cv2.destroyAllWindows()



def add_watermark():
    mush = cv2.imread("lesson/mushroom.jpg")
    logo = cv2.imread("lesson/cvlogo.png")

    logo = cv2.resize(logo, (logo.shape[0]//2, logo.shape[1]//2))
    roi = mush[0:logo.shape[0], 0:logo.shape[1]]

    logo_gray = cv2.cvtColor(logo, cv2.COLOR_RGB2GRAY)
    ret, mask = cv2.threshold(logo_gray, 10, 255, cv2.THRESH_BINARY)
    mask_inv = cv2.bitwise_not(mask)
    bg = cv2.bitwise_and(roi, roi, mask=mask_inv)
    fg = cv2.bitwise_and(logo, logo, mask=mask)

    combined = cv2.add(bg, fg)
    mush[:logo.shape[0], :logo.shape[1]] = combined

    camera_name = "image"
    cv2.namedWindow(camera_name, cv2.WINDOW_GUI_NORMAL)
    cv2.imshow(camera_name, mush)
    cv2.waitKey()
    cv2.destroyAllWindows()


def cut_rose():
    image = cv2.imread("lesson/rose.jpg")
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    lower = np.array([0, 100, 100])
    upper = np.array([1, 255, 255])
    mask = cv2.inRange(hsv, lower, upper)
    mask = cv2.dilate(mask, np.ones((10, 10)))

    result = cv2.bitwise_and(image, image, mask=mask)

    camera_name = "image"
    cv2.namedWindow(camera_name, cv2.WINDOW_GUI_NORMAL)
    cv2.imshow(camera_name, result)
    cv2.waitKey()
    cv2.destroyAllWindows()


news = cv2.imread("lesson/news.jpg")
chebu = cv2.imread("lesson/wotiwan.png")

dest_pts = np.float32([[17, 25], [432, 55], [433, 269], [40, 294]])
src_pts = np.float32([[0, 0],
                      [chebu.shape[1], 0],
                      [chebu.shape[1], chebu.shape[0]],
                      [0, chebu.shape[0]]
])

M = cv2.getPerspectiveTransform(src_pts, dest_pts)
persp_img = cv2.warpPerspective(chebu, M, news.shape[:2][::-1])

gray = cv2.cvtColor(persp_img, cv2.COLOR_BGR2GRAY)
ret, mask = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)
bg = cv2.bitwise_and(news, news, mask=cv2.bitwise_not(mask))
fg = cv2.bitwise_and(persp_img, persp_img, mask=mask)

result = cv2.add(bg, fg)

camera_name = "image"
cv2.namedWindow(camera_name, cv2.WINDOW_GUI_NORMAL)
cv2.imshow(camera_name, result)
cv2.waitKey()
cv2.destroyAllWindows()
