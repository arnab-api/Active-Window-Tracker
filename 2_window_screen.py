import numpy as np
import cv2
import pyautogui
import imutils
  
  
# take screenshot using pyautogui
image = pyautogui.screenshot()
image = np.array(image)
image = imutils.resize(image, width=1080)
cv2.namedWindow("preview")
print(type(image))
cv2.imshow("preview", image)
# since the pyautogui takes as a 
# PIL(pillow) and in RGB we need to 
# convert it to numpy array and BGR 
# so we can write it to the disk

while True:
    cv2.imshow("preview", image)
    image = pyautogui.screenshot()
    image = np.array(image)
    image = imutils.resize(image, width=1080)
    key = cv2.waitKey(20)
    if key == 27: # exit on ESC
        break
cv2.destroyWindow("preview")

# image = cv2.cvtColor(np.array(image),
#                      cv2.COLOR_RGB2BGR)
   
# # writing it to the disk using opencv
# cv2.imwrite("image1.png", image)