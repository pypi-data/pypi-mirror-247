import pyautogui
import numpy as np
import pygetwindow as gw
import easyocr

def capture_window(window: gw.Window):
    window.activate()  # Bring the window to the front
    # Adjust if the window has a border or title bar
    left, top, width, height = window.left, window.top, window.width, window.height
    img =  pyautogui.screenshot(region=(left, top, width, height))
    return np.array(img)


def find_word_coordinates(image, search_word):
    # Create a reader object
    reader = easyocr.Reader(['en'])  # 'en' denotes English language

    # Perform OCR on the image
    results = reader.readtext(image)

    # List to store coordinates of found words
    found_word_coordinates = []

    # Iterate over OCR results
    for result in results:
        # Each result has this format: (bbox, text, confidence)
        bbox, text, _ = result

        # Check if the detected text matches the search word
        if text.lower() == search_word.lower():
            # bbox is in the format [(top_left), (top_right), (bottom_right), (bottom_left)]
            # You can format it as you like, here's a simple conversion to (x, y, width, height)
            top_left = bbox[0]
            bottom_right = bbox[2]
            x, y = top_left
            width = bottom_right[0] - top_left[0]
            height = bottom_right[1] - top_left[1]

            found_word_coordinates.append((x, y, width, height))

    return found_word_coordinates