from PIL import Image

img = Image.open('img_resize/src/img_resize/test.JPG')
upscaled = img.resize((img.width * 8, img.height * 8), Image.LANCZOS)
upscaled.save("pil.jpg")

from PIL import Image, ImageEnhance

# Load the image
img = Image.open('img_resize/src/img_resize/test.JPG')

# Upscale the image by 8x
scale_factor = 8
new_size = (img.width * scale_factor, img.height * scale_factor)
upscaled_img = img.resize(new_size, Image.LANCZOS)

# Increase contrast slightly
enhancer = ImageEnhance.Contrast(upscaled_img)
contrast_img = enhancer.enhance(1.2)  # 1.0 = original, >1 = more contrast

# Save the result
output_path = "test_upscaled_contrast.jpg"
contrast_img.save(output_path, quality=95)

print(f"Saved: {output_path}")
