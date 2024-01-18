import cv2
import numpy as np
from sklearn.cluster import KMeans

def find_histogram(clt):
    numLabels = np.arange(0, len(np.unique(clt.labels_)) + 1)
    (hist, _) = np.histogram(clt.labels_, bins=numLabels)
    hist = hist.astype("float")
    hist /= hist.sum()
    return hist

def plot_colors2(hist, centroids):
    bar = np.zeros((50, 300, 3), dtype="uint8")
    startX = 0
    for (percent, color) in zip(hist, centroids):
        endX = startX + (percent * 300)
        cv2.rectangle(bar, (int(startX), 0), (int(endX), 50),
                      color.astype("uint8").tolist(), -1)
        startX = endX
    return bar

# Capture video from webcam (0 is usually the default webcam)
cap = cv2.VideoCapture(0)

# Create a window to display the video feed
cv2.namedWindow('Video Feed', cv2.WINDOW_NORMAL)

while True:
    # Read a frame from the video feed
    ret, frame = cap.read()

    # Convert the frame to RGB
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Reshape the frame
    img = frame_rgb.reshape((frame_rgb.shape[0] * frame_rgb.shape[1], 3))

    # Apply KMeans clustering
    clt = KMeans(n_clusters=3)
    clt.fit(img)

    # Find histogram and dominant color
    hist = find_histogram(clt)
    dominant_color = clt.cluster_centers_[np.argmax(hist)]

    # Create a small image of the dominant color
    dominant_img = np.zeros((50, 50, 3), dtype="uint8")
    dominant_img[:, :] = dominant_color.astype("uint8")

    frame[0:50, 0:50] = dominant_img

    # Display the video feed
    cv2.imshow('dominant', frame)

    # Break the loop if 'q' key is pressed
    k = cv.waitKey(5) & 0xFF
    if k == 27:
        break

# Release the video capture object and close the window
cap.release()
cv2.destroyAllWindows()
