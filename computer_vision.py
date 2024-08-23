import cv2 as cv
import math
from numpy import ndarray
from typing import Optional

Circle = tuple[float, float, float]
Iris = tuple[ndarray, Circle, Circle]

def get_iris(image: ndarray) -> Optional[Iris]:
    min_radius = 480 * 0.8 * 0.9
    max_radius = 480 * 0.8 * 1.1
    irides = cv.HoughCircles(
        image,
        cv.HOUGH_GRADIENT,
        1,
        100,
        param1 = 40,
        param2 = 20,
        minRadius = min_radius,
        maxRadius = max_radius
    )

    if irides is None:
        return None

    min_radius_p = min_radius * 0.6 * 0.9
    max_radius_p = min_radius * 0.6 * 1.1

    pupils = cv.HoughCircles(
        image,
        cv.HOUGH_GRADIENT,
        1,
        100,
        param1 = 40,
        param2 = 20,
        minRadius = min_radius_p,
        maxRadius = max_radius_p
    )
 
    selected_iris: Optional[Circle] = None
    selected_pupil: Optional[Circle] = None
    for iris_x, iris_y, iris_r in irides[0]:
        for pupil_x, pupil_y, pupil_r in pupils[0]:
            if math.sqrt((pupil_x - iris_x)**2 + (pupil_y - iris_y)**2) <= 10:
                selected_pupil = (pupil_x, pupil_y, pupil_r)
                selected_iris = (iris_x, iris_y, iris_r)
                break

    if selected_iris is None or selected_pupil is None:
        return None
    
    center_x = selected_iris[0]
    center_y = selected_iris[1]
    length = selected_iris[2]
    x_upper = max(image.shape[0], center_x + length)
    y_upper = max(image.shape[1], center_y + length)
    x_lower = min(0, center_x - length)
    y_lower = min(0, center_y - length)
    image = image[
        y_lower : y_upper,
        x_lower : x_upper
    ]

    return (image, selected_iris, selected_pupil)
