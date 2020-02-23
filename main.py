import cv2
import numpy as np
from file_utils import get_bid_files

FOLDER_PATH = "raw-day-light/"


def resize_image(image, scaling_factor=30):
    scaling_factor = 30
    width = int(image.shape[1] * scaling_factor / 100)
    height = int(image.shape[0] * scaling_factor / 100)
    dsize = (width, height)

    return cv2.resize(image, dsize=dsize)


def prepare_image(image):
    result = resize_image(image)
    result = result[100:800, 100:800, :]

    return result


def cropped_image(image):
    blured = cv2.GaussianBlur(image, (5, 5), cv2.BORDER_DEFAULT)

    gray = cv2.cvtColor(blured, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY)

    contours, _ = cv2.findContours(
        thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    mask = cv2.drawContours(thresh.copy(), contours,
                            0, 255, cv2.FILLED)

    result = cv2.bitwise_or(image.copy(), image.copy(), mask=mask)

    thresh_contours, _ = cv2.findContours(
        thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    x, y, _, _ = cv2.boundingRect(thresh_contours[0])
    w, h = 410, 245

    return result[y:y+h, x:x+w, :]


def bid_section(image):
    return image[20:210, 250:380, :]


def draw(image):
    cv2.imshow('result', image)
    cv2.waitKey()


def solidity(contour):
    contour_area = cv2.contourArea(contour)
    hull = cv2.convexHull(contour)
    hull_area = cv2.contourArea(hull)

    if hull_area == 0:
        return 0

    ratio = contour_area / hull_area

    return ratio


files = get_bid_files(FOLDER_PATH)


def get_convex_hull(image):
    bid_image = bid_section(image)
    blured = cv2.GaussianBlur(bid_image, (3, 3), cv2.BORDER_DEFAULT)
    gray = cv2.cvtColor(blured, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 170, 255, cv2.THRESH_BINARY_INV)

    contours, _ = cv2.findContours(
        thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    contours = filter(lambda c: solidity(c) > 0, contours)
    contours = sorted(contours, key=lambda c: cv2.minAreaRect(c), reverse=True)
    contours = list(contours)

    single_contour = np.concatenate(contours)
    single_hull = cv2.convexHull(single_contour)

    return single_hull + (250, 20)


for file in files:
    image = cv2.imread(file)
    image = prepare_image(image)
    image = cropped_image(image)

    hull = get_convex_hull(image)
    result = cv2.drawContours(image.copy(), [hull], 0, (0, 255, 0), 2)

    draw(result)
