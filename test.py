import cv2 as cv

from computer_vision import get_iris, extract_features_for_ml

img = cv.imread("/var/tmp/lab/photo_2024-08-23_18-33-36.jpg", cv.IMREAD_GRAYSCALE)

iris = get_iris(img, 100)

if iris is None:
    print("No iris with pupil inside detected...")
else:
    cv.imwrite("/tmp/v.png", iris[0])
    print(iris[1:])
    print("saved")
