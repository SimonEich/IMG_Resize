import cv2
import numpy as np
from tkinter import filedialog
from PIL import Image
from rembg import remove
import io

class Logic:
    """
    Logic class to handle image processing operations such as resizing, 
    creating thumbnails, and saving images using OpenCV and PIL.
    """

    def __init__(self):
        """Initialize the Logic object."""
        pass

    def _load_img(self, path) -> np.ndarray | None:
        """
        Load an image from the specified path using OpenCV.

        Args:
            path (str): The path to the image file.

        Returns:
            np.ndarray | None: The loaded image as a NumPy array or None if loading fails.
        """
        return cv2.imread(path)
    
    def get_resolution(self, path):
        """
        Get the resolution (height, width) of the image at the given path.

        Args:
            path (str): The image file path.

        Returns:
            tuple[int, int] | None: Resolution as (height, width), or None if the image can't be loaded.
        """
        img = self._load_img(path)
        return img.shape[:2] if img is not None else None

    def increase_Resolution(self, path, scale) -> None:
        """
        Increase the resolution of the image by a given scale and prompt the user to save the result.

        Args:
            path (str): Path to the image file.
            scale (int): Scaling factor (e.g., 2 for doubling size).
        """
        img = self._load_img(path)
        if img is None:
            print("Failed to load image.")
            return
        new_dim = (img.shape[1] * scale, img.shape[0] * scale)
        self.upscaled = cv2.resize(img, new_dim, interpolation=cv2.INTER_LANCZOS4)
        self.save_cv2_image(self.upscaled)

    def decrease_Resolution(self, path) -> None:
        """
        Decrease the resolution of the image by 50% and prompt the user to save it.

        Args:
            path (str): Path to the image file.
        """
        img = self._load_img(path)
        if img is None:
            print("Failed to load image.")
            return
        downscaled = cv2.resize(img, (img.shape[1] // 2, img.shape[0] // 2), interpolation=cv2.INTER_AREA)
        self.save_cv2_image(downscaled)

    def thumbnail_Resolution(self, path) -> None:
        """
        Resize and crop an image to match YouTube thumbnail resolution and prompt user to save.

        Args:
            path (str): Path to the image file.
        """
        self.resize_to_custom_resolution(path, 1280, 720)


    def save_cv2_image(self, img: np.ndarray):
        """
        Open a file save dialog and save an OpenCV image (in BGR) as JPEG or PNG using PIL.

        Args:
            img (np.ndarray): The image in BGR format.
        """
        file_path = filedialog.asksaveasfilename(
            defaultextension=".jpeg",
            filetypes=[
                ("JPEG files", "*.jpeg"),
                ("PNG files", "*.png")
            ],
            title="Save image file"
        )

        if file_path:
            ext = file_path.lower().split('.')[-1]
            format = "JPEG" if ext == "jpeg" else "PNG"

            # Convert BGR to RGB for PIL
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img_pil = Image.fromarray(img_rgb)

            if format == "JPEG":
                img_pil = img_pil.convert("RGB")  # Ensure no alpha channel

            img_pil.save(file_path, format=format)
            print(f"Image saved to: {file_path}")
        else:
            print("Save cancelled.")

    def resize_to_custom_resolution(self, input_path: str, target_width, target_height):
        """
        Resize and crop an image to fit YouTube thumbnail dimensions (1280x720),
        preserving aspect ratio and cropping the excess without stretching or padding.
        Prompts user for save location.

        Args:
            input_path (str): Path to input image file.
        """

        target_ratio = target_width / target_height

        with Image.open(input_path) as img:
            original_width, original_height = img.size
            original_ratio = original_width / original_height

            # Determine crop box
            if original_ratio > target_ratio:
                # Crop horizontally
                new_width = int(original_height * target_ratio)
                offset = (original_width - new_width) // 2
                crop_box = (offset, 0, offset + new_width, original_height)
            else:
                # Crop vertically
                new_height = int(original_width / target_ratio)
                offset = (original_height - new_height) // 2
                crop_box = (0, offset, original_width, offset + new_height)

            img_cropped = img.crop(crop_box)
            img_resized = img_cropped.resize((target_width, target_height), Image.LANCZOS)

            # Use save dialog
            file_path = filedialog.asksaveasfilename(
                defaultextension=".jpeg",
                filetypes=[("Image Files", "*.png *.jpeg")],
                title="Save YouTube Thumbnail"
            )
            if file_path:
                img_resized.save(file_path)
                print(f"Thumbnail saved to {file_path}")
            else:
                print("Save cancelled.")


    def remove_background(self, path) -> None:
        """
        Removes the background from an image and saves the result using a file dialog.

        Args:
            path (str): The path to the image file.
        """
        with open(path, 'rb') as f:
            input_bytes = f.read()
            output_bytes = remove(input_bytes)

        # Convert output bytes to PIL Image with transparency
        img = Image.open(io.BytesIO(output_bytes)).convert("RGBA")

        # Save with dialog
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png")],
            title="Save Image without Background"
        )
        if file_path:
            img.save(file_path, format="PNG")
            print(f"Image saved to: {file_path}")
        else:
            print("Save cancelled.")
            
    def save_cv2_image(self, img: np.ndarray):
        """
        Open a file save dialog and save an OpenCV image as PNG if it has transparency (alpha),
        otherwise allow both JPEG and PNG using PIL.

        Args:
            img (np.ndarray): The image (BGR or BGRA format).
        """
        has_alpha = img.shape[2] == 4 if len(img.shape) == 3 else False

        # Only allow PNG if image has transparency
        filetypes = [("PNG files", "*.png")] if has_alpha else [
            ("JPEG files", "*.jpeg"),
            ("PNG files", "*.png")
        ]
        def_ext = ".png" if has_alpha else ".jpeg"

        file_path = filedialog.asksaveasfilename(
            defaultextension=def_ext,
            filetypes=filetypes,
            title="Save image file"
        )

        if file_path:
            ext = file_path.lower().split('.')[-1]
            format = "PNG" if has_alpha or ext == "png" else "JPEG"

            # Convert BGR(A) to RGB(A)
            if has_alpha:
                img_rgb = cv2.cvtColor(img, cv2.COLOR_BGRA2RGBA)
            else:
                img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            img_pil = Image.fromarray(img_rgb)

            if format == "JPEG":
                img_pil = img_pil.convert("RGB")  # Ensure no alpha

            img_pil.save(file_path, format=format)
            print(f"Image saved to: {file_path}")
        else:
            print("Save cancelled.")

    
    def remove_white_pixels(self, path) -> None:
        """
        Remove white (or near-white) pixels from an image and save the result using a file dialog.
    
        Args:
            path (str): The path to the image file.
        """
        tolerance = 10
        img = Image.open(path).convert("RGBA")
        datas = img.getdata()
    
        new_data = []
        for r, g, b, a in datas:
            if (
                abs(r - 255) <= tolerance and
                abs(g - 255) <= tolerance and
                abs(b - 255) <= tolerance
            ):
                new_data.append((255, 255, 255, 0))  # Make transparent
            else:
                new_data.append((r, g, b, a))
    
        img.putdata(new_data)
    
        # Convert to NumPy array with BGRA format for OpenCV compatibility
        img_np = np.array(img)
        img_cv2 = cv2.cvtColor(img_np, cv2.COLOR_RGBA2BGRA)
    
        self.save_cv2_image(img_cv2)
    