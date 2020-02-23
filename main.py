import cv2
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


files = get_bid_files(FOLDER_PATH)

for file in files:
    image = cv2.imread(file)
    image = prepare_image(image)

    cropped = cropped_image(image)
    cv2.imshow('result', cropped)
    cv2.waitKey()
