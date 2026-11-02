import cv2

from vision.image_loader import load_image

image = load_image("assets/screenshot-01.png")

print("Height :", image.shape[0])
print("Width  :", image.shape[1])
print("Channels :", image.shape[2])

cv2.imshow("Screenshot", image)
cv2.waitKey(0)
cv2.destroyAllWindows()