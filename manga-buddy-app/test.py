import tkinter as tk
from PIL import ImageGrab, Image, ImageTk, ImageDraw
import pytesseract
import os
import datetime
import shutil
import re

# Set Tesseract command path (update with your own path)
pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

# Set up the folder to save screenshots
screenshot_folder = "saved_screenshots"
if not os.path.exists(screenshot_folder):
    os.makedirs(screenshot_folder)

def take_screenshot():
    # Capture the screenshot of the primary screen
    screenshot = ImageGrab.grab()
    
    # Save the screenshot with a timestamp in the designated folder
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    screenshot_path = os.path.join(screenshot_folder, f"screenshot_{timestamp}.png")
    screenshot.save(screenshot_path)
    print(f"Screenshot saved as {screenshot_path}")

    # Draw rectangles around Japanese text in the screenshot
    screenshot_with_rectangles = highlight_japanese_text(screenshot)

    # Resize the modified screenshot to fit the window and display it
    screenshot_resized = screenshot_with_rectangles.resize((root.winfo_width(), root.winfo_height()))
    screenshot_tk = ImageTk.PhotoImage(screenshot_resized)
    screenshot_label.config(image=screenshot_tk)
    screenshot_label.image = screenshot_tk  # Keep a reference to avoid garbage collection

def highlight_japanese_text(image):
    # Convert the image to grayscale for better OCR accuracy
    gray_image = image.convert("L")
    
    # Use pytesseract to perform OCR on the image
    ocr_data = pytesseract.image_to_data(gray_image, lang="jpn", output_type=pytesseract.Output.DICT)
    
    # Create a drawable object to draw rectangles on the original image
    draw = ImageDraw.Draw(image)
    
    # Regular expression to identify Japanese characters
    japanese_chars = re.compile(r'[\u3040-\u30FF\u4E00-\u9FFF\uFF66-\uFF9F]')  # Hiragana, Katakana, Kanji

    # Iterate through each detected word
    for i, text in enumerate(ocr_data['text']):
        if japanese_chars.search(text):  # Check if text contains Japanese characters
            x, y, w, h = (ocr_data['left'][i], ocr_data['top'][i], ocr_data['width'][i], ocr_data['height'][i])
            draw.rectangle([(x, y), (x + w, y + h)], outline="red", width=2)

    return image

def delete_all_screenshots():
    # Delete all files in the screenshot folder
    for filename in os.listdir(screenshot_folder):
        file_path = os.path.join(screenshot_folder, filename)
        try:
            os.remove(file_path)
            print(f"Deleted {file_path}")
        except Exception as e:
            print(f"Failed to delete {file_path}: {e}")

# Set up the main application window
root = tk.Tk()
root.title("Screenshot Tool")
root.geometry("800x600")

# Create a label to display the screenshot
screenshot_label = tk.Label(root)
screenshot_label.pack(fill="both", expand=True)

# Create the "Capture Screenshot" button
screenshot_button = tk.Button(root, text="Capture Screenshot", command=take_screenshot)
screenshot_button.place(x=10, y=10)

# Create the "Delete All Screenshots" button and place it next to the "Capture Screenshot" button
delete_button = tk.Button(root, text="Delete All Screenshots", command=delete_all_screenshots)
delete_button.place(x=150, y=10)

# Run the application
root.mainloop()
