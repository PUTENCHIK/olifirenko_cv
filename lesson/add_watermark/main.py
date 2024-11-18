import cv2
from pathlib import Path


path = Path(__file__).parent
mush = cv2.imread(path/ "mushroom.jpg")
logo = cv2.imread(path/ "cvlogo.png")

logo = cv2.resize(logo, (logo.shape[0]//2, logo.shape[1]//2))
roi = mush[0:logo.shape[0], 0:logo.shape[1]]

logo_gray = cv2.cvtColor(logo, cv2.COLOR_RGB2GRAY)
ret, mask = cv2.threshold(logo_gray, 10, 255, cv2.THRESH_BINARY)
mask_inv = cv2.bitwise_not(mask)
bg = cv2.bitwise_and(roi, roi, mask=mask_inv)
fg = cv2.bitwise_and(logo, logo, mask=mask)

combined = cv2.add(bg, fg)
mush[:logo.shape[0], :logo.shape[1]] = combined

window_name = "image"
cv2.namedWindow(window_name, cv2.WINDOW_GUI_NORMAL)
cv2.imshow(window_name, mush)
cv2.waitKey()
cv2.destroyAllWindows()
