import cv2
import numpy as np

def detect_fake_picture(pathd):
    img = cv2.imread(pathd)

    
    average_color = np.average(img, axis=(0, 1))
    if np.any(average_color < 50) or np.any(average_color > 200):
        return "Fake - Strange colors detected"


    edges = cv2.Canny(img, 100, 200)
    if np.mean(edges) > 10:
        return "Fake - Jagged edges detected"

    
    if np.sum(np.abs(np.diff(img, axis=0))) < 1000:
        return "Fake - Strange patterns detected"

   
    return "Real - No signs of fakeness detected"


pathd = "images/Sirisha.jpg"
result = detect_fake_picture(pathd)
print(result)