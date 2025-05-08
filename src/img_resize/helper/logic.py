import cv2
import numpy as np

class Logic:
    def __init__(self):
        self.get_resolution
        
    def _load_img(self, path)->np.ndarray | None:
        img = cv2.imread(path)
        return img
    
    def get_resolution(self, path):
        img = self._load_img(path)
    
    def increase_Resolution(self, path, scale)->None:
        img = self._load_img(path)
        new_dim = (img.shape[1] * scale, img.shape[0] * scale)

        # Resize with Lanczos (better quality than bicubic)
        upscaled = cv2.resize(img, new_dim, interpolation=cv2.INTER_LANCZOS4)

    
    def decrease_Resolution(self, path)->None:
        img = self._load_img(path)
        
    def thumbnail_Resolution(self, path)->None:
        print('thumbnail')
    
    def click(self, a):
        print('click')