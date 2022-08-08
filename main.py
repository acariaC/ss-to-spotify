import cv2
import numpy as np
from pytesseract import pytesseract, Output

# Getting the image from specified folder
img = cv2.imread("/Users/oliverkuhn/Desktop/iCloud Photos/IMG_3785.PNG")
# ALTERNATIVE TEST: img = cv2.imread("/Users/oliverkuhn/Desktop/iCloud Photos/IMG_4057.PNG")


# General information about the image (to be deleted!)
rows, cols, _ = img.shape
print("ROWS: ", rows)
print("COLUMNS: ", cols, "\n")

# Cropping the image down to the relevant parts
cropped_image = img[700: 1955, 0: 1170]

# Getting the text in the cropped image
config = 'textord_min_xheight 255'

artistAndTitle = pytesseract.image_to_string(cropped_image, config = config)
print(artistAndTitle)

h, w, c = img.shape
boxes = pytesseract.image_to_boxes(img)
for b in boxes.splitlines():
    b = b.split(' ')
    img = cv2.rectangle(img, (int(b[1]), h - int(b[2])), (int(b[3]), h - int(b[4])), (0, 255, 0), 2)


# Displaying the image

cv2.imshow("Boxed", cropped_image)
cv2.waitKey(0)



