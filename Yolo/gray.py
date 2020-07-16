import cv2
import glob


img = glob.glob('./data_original/*/*.jpg')
for i in img:
    image = cv2.imread(i)
    image_g = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    cv2.imwrite(i, image_g)