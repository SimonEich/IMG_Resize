import cv2

# Load the image
img = cv2.imread('img_resize/src/img_resize/test.JPG')

# Define scale factor
scale = 8
new_dim = (img.shape[1] * scale, img.shape[0] * scale)

# Resize with Lanczos (better quality than bicubic)
upscaled = cv2.resize(img, new_dim, interpolation=cv2.INTER_LANCZOS4)

# Save the result
cv2.imwrite('upscaled.jpg', upscaled)
