import cv2 as cv

from computer_vision import get_iris, extract_features_for_ml

img = cv.imread("/home/farooqkz/Downloads/Diabetes/100/IMG_2016_06_01_9999_21.JPG", cv.IMREAD_GRAYSCALE)

img = cv.resize(img, (640, 333))

c = cv.Canny(img, 40, 80)

cv.imwrite("/tmp/v2.png", c)

iris = get_iris(img, param2=10, param1=80)

if iris is None:
    print("No iris with pupil inside detected...")
else:
    cv.imwrite("/tmp/v1.png", iris[0])
    print(iris[1:])
    print("saved")
