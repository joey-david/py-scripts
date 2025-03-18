import sys
import os
import argparse
import time
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import JavascriptException
import cv2
import numpy as np
import base64

########################################################################
# 1) GUI for user to select images
########################################################################

class ImageSelectionGUI(tk.Toplevel):
    """
    A simple GUI that allows the user to select images (via file dialog).
    The user can add multiple images, see them in a list, and press 'Done' to proceed.
    """
    def __init__(self, master):
        super().__init__(master)
        self.title("Select Images")
        self.geometry("500x300")
        self.image_paths = []

        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Listbox to display chosen images
        self.listbox = tk.Listbox(main_frame, selectmode=tk.SINGLE)
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Scrollbar
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=self.listbox.yview)
        scrollbar.pack(side=tk.LEFT, fill=tk.Y)
        self.listbox.config(yscrollcommand=scrollbar.set)

        # Button frame
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5)

        self.add_btn = ttk.Button(btn_frame, text="Add Image", command=self.add_image)
        self.add_btn.pack(fill=tk.X, pady=5)

        self.remove_btn = ttk.Button(btn_frame, text="Remove Selected", command=self.remove_selected)
        self.remove_btn.pack(fill=tk.X, pady=5)

        self.preview_btn = ttk.Button(btn_frame, text="Preview", command=self.preview_selected)
        self.preview_btn.pack(fill=tk.X, pady=5)

        self.done_btn = ttk.Button(btn_frame, text="Done", command=self.on_done)
        self.done_btn.pack(fill=tk.X, pady=20)

        self.preview_window = None

    def add_image(self):
        """Open a file dialog to select images and add them to the list."""
        filetypes = [
            ("Image Files", "*.png *.jpg *.jpeg *.gif *.bmp *.tiff"),
            ("All Files", "*.*")
        ]
        paths = filedialog.askopenfilenames(title="Select images", filetypes=filetypes)
        for p in paths:
            if os.path.isfile(p):
                self.image_paths.append(os.path.abspath(p))
                self.listbox.insert(tk.END, os.path.basename(p))

    def remove_selected(self):
        """Remove the currently selected image from the list."""
        idx = self.listbox.curselection()
        if not idx:
            return
        i = idx[0]
        self.listbox.delete(i)
        del self.image_paths[i]

    def preview_selected(self):
        """Preview the currently selected image in a separate window."""
        idx = self.listbox.curselection()
        if not idx:
            return
        i = idx[0]
        img_path = self.image_paths[i]

        if self.preview_window is not None:
            self.preview_window.destroy()

        self.preview_window = tk.Toplevel(self)
        self.preview_window.title("Preview - " + os.path.basename(img_path))

        try:
            img = Image.open(img_path)
            img.thumbnail((300, 300))
            tk_img = ImageTk.PhotoImage(img)
            label = tk.Label(self.preview_window, image=tk_img)
            label.image = tk_img
            label.pack()
        except Exception as e:
            messagebox.showerror("Error", f"Could not open image:\n{e}")

    def on_done(self):
        self.destroy()

    def get_selected_images(self):
        """Returns the list of selected images after user closes the dialog."""
        return self.image_paths

########################################################################
# 2) Functions to drive Selenium
########################################################################

def open_chrome_no_automation_flags():
    """
    Opens Chrome with some common automation flags disabled to reduce detection.
    Preserves user profile data to maintain existing login sessions.
    Requires chromedriver on PATH.
    """
    options = Options()
    # Disabling webdriver and automation extension
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    
    # Additional arguments to reduce automation fingerprinting
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--no-first-run")
    options.add_argument("--no-default-browser-check")
    
    driver = webdriver.Chrome(options=options)
    return driver

def click_zones_in_order(driver, image_paths, coordinates_map, pause=1.0, threshold=0.95):
    """
    For each image, finds it on screen using computer vision and clicks it.
    If coordinates_map is provided, it will be used as fallback.
    threshold: minimum matching confidence (0.0 to 1.0, higher is more strict)
    """
    
    def get_screenshot_as_cv2(driver):
        """Captures screenshot and converts to CV2 format"""
        screenshot = driver.get_screenshot_as_base64()
        image_data = base64.b64decode(screenshot)
        nparr = np.frombuffer(image_data, np.uint8)
        return cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    def find_image_on_screen(template_path, screenshot):
        """Finds template image in screenshot using template matching"""
        template = cv2.imread(template_path)
        if template is None:
            print(f"[ERROR] Could not load template image: {template_path}")
            return None
            
        # Get dimensions
        h, w = template.shape[:2]
        
        # Apply template matching
        result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
        
        # Find best match location
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        
        if max_val >= threshold:
            # Calculate center point
            top_left = max_loc
            center_x = top_left[0] + w // 2
            center_y = top_left[1] + h // 2
            return (center_x, center_y, max_val)
        else:
            return None
    
    failCount = 0
    while True:
        for path in image_paths:
            # Take screenshot
            screenshot = get_screenshot_as_cv2(driver)
            
            # Try to find image on screen
            match = find_image_on_screen(path, screenshot)
            
            if match:
                failCount = 0
                x, y, confidence = match
                print(f"Found '{os.path.basename(path)}' with confidence: {confidence:.2f}")
                
                # Click at the match location
                action = ActionChains(driver)
                    
                # Move to the location and click
                action.move_by_offset(x, y)
                action.click()
                action.perform()
                action.reset_actions()  # Reset for next action
            else:
                failCount += 1
                if failCount > 2*len(image_paths):
                    print("Failed to find images twice. Exiting.")
                    return
            
            time.sleep(pause)

########################################################################
# 3) Main
########################################################################

def main():
    parser = argparse.ArgumentParser(description="Image selection, then browser automation.")
    parser.add_argument("--url", "-url", type=str, default="https://www.example.com",
                        help="URL to navigate to in chrome.")
    args = parser.parse_args()

    # Step 1: Create a single root instance for all GUIs
    root = tk.Tk()
    root.withdraw()

    # Open selection GUI
    select_gui = ImageSelectionGUI(root)
    root.wait_window(select_gui)
    selected_images = select_gui.get_selected_images()

    if not selected_images:
        print("No images selected. Exiting.")
        root.destroy()
        sys.exit(0)

    # Step 2: Open Chrome to the provided URL
    driver = open_chrome_no_automation_flags()
    driver.get(args.url)
    
    for i in range (0, 30):
        print(29-i)
        time.sleep(1)
    print("go")

    # Step 3: Build a dummy coordinates_map
    # For demonstration, let's place each subsequent image click ~50px below the previous.
    coordinates_map = {}
    x_offset = 50
    base_y_offset = 100
    for i, img in enumerate(selected_images):
        # example: each image is 50px further down
        coordinates_map[img] = (x_offset, base_y_offset + i*50)

    # Step 4: Click in order
    click_zones_in_order(driver, selected_images, coordinates_map, pause=2.5)

    # Keep browser open a bit
    time.sleep(2)
    driver.quit()

    # Cleanup
    root.destroy()

if __name__ == "__main__":
    main()
