import cv2
import random
import numpy as np

# rotate the image by a random angle
def rotate_image(image):
    
    # Get image dimensions
    height, width = image.shape[:2]
    
    # Generate a random angle between -30 and 30 degrees
    random_angle = random.uniform(-180, 180)
    
    # Calculate the rotation matrix
    rotation_matrix = cv2.getRotationMatrix2D((width/2, height/2), random_angle, 1)
    
    # Perform the actual rotation
    rotated_image = cv2.warpAffine(image, rotation_matrix, (width, height))
    
    return rotated_image

def paste_on_top(paste_to: np.ndarray, paste_from: np.ndarray, x: int ,y: int ):

    w = paste_from.shape[1]
    h = paste_from.shape[0]

    y2 = y+h
    x2 = x+w

    paste_to[y:y2,x:x2] = paste_from

    return paste_to