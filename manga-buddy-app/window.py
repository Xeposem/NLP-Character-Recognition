import tkinter as tk
from PIL import ImageGrab, Image, ImageTk
import os
import datetime
import shutil

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
    
    # Display the screenshot in the label
    screenshot_resized = screenshot.resize((root.winfo_width(), root.winfo_height()))
    screenshot_tk = ImageTk.PhotoImage(screenshot_resized)
    screenshot_label.config(image=screenshot_tk)
    screenshot_label.image = screenshot_tk  # Keep a reference to avoid garbage collection

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
delete_button.place(x=150, y=10)  # Adjust the x position as needed to place it next to the first button

# Run the application
root.mainloop()
