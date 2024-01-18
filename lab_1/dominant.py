import cv2 as cv
import numpy as np

cap = cv.VideoCapture(0)

while True:
    # Take each frame
    _, frame = cap.read()

    # Define the coordinates of the central rectangle
    x, y, w, h = 200, 150, 100, 100

    # Extract the region of interest (ROI) from the frame
    roi = frame[y:y+h, x:x+w]

    # Convert the ROI from BGR to HSV
    hsv_roi = cv.cvtColor(roi, cv.COLOR_BGR2HSV)

    # Reshape the ROI to a list of pixels
    pixels = hsv_roi.reshape((-1, 3))

    # Convert pixels to float32
    pixels = np.float32(pixels)

    # Perform k-means clustering to find dominant color
    criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 100, 0.2)
    k = 1  # Number of clusters (dominant color)
    _, labels, centers = cv.kmeans(pixels, k, None, criteria, 10, cv.KMEANS_RANDOM_CENTERS)

    # Convert the center back to uint8
    dominant_color = np.uint8(centers[0])

    # Create an image of the dominant color
    color_image = np.zeros((50, 50, 3), dtype=np.uint8)
    color_image[:, :] = dominant_color

    # Display the color image in the top-left corner
    frame[0:50, 0:50] = color_image

    # Draw a rectangle around the central region
    cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Display the frames
    cv.imshow('frame', frame)

    # Break the loop if 'Esc' key is pressed
    k = cv.waitKey(5) & 0xFF
    if k == 27:
        break

# Release the capture and close all windows
cap.release()
cv.destroyAllWindows()
