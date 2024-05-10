import os
import numpy as np
import cv2
import imutils
import pytesseract

# Function to process each image
def process_image(image_path):
    image = cv2.imread(image_path)
    image = imutils.resize(image, width=500)
    cv2.imshow("Original Image", image)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.bilateralFilter(gray, 11, 17, 17)
    edged = cv2.Canny(gray, 170, 200)

    cnts, hierarchy = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:30]
    NumberPlateCnt = None 

    for c in cnts:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
        if len(approx) == 4:  
            NumberPlateCnt = approx 
            break

    if NumberPlateCnt is None:
        print("Number plate contour not found in the image.")
        return

    # Masking the part other than the number plate
    mask = np.zeros(gray.shape, np.uint8)
    new_image = cv2.drawContours(mask, [NumberPlateCnt], 0, 255, -1)
    new_image = cv2.bitwise_and(image, image, mask=mask)
    cv2.namedWindow("Final_image", cv2.WINDOW_NORMAL)
    cv2.imshow("Final_image", new_image)

    # Configuration for tesseract
    config = ('-l eng --oem 1 --psm 3')

    # Run tesseract OCR on image
    text = pytesseract.image_to_string(new_image, config=config)

    # Print recognized text
    print("License Plate Number:", text)

# Folder containing images
folder_path = "NumberPlate"

# Get a list of all image files in the folder
image_files = sorted([os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith(('.jpg', '.jpeg', '.png'))])

current_index = 0
while True:
    process_image(image_files[current_index])
    key = cv2.waitKey(0)

    if key == 27:  # ESC key
        break
    elif key == ord('n') and current_index < len(image_files) - 1:  # Next image
        current_index += 1
    elif key == ord('p') and current_index > 0:  # Previous image
        current_index -= 1

cv2.destroyAllWindows()
