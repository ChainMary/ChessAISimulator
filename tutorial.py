import cv2
import numpy as np
import platform
import time
from PIL import ImageGrab
import pyautogui
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def click_play(url):
    driver = helper_getSystem()
    driver.get(url)
    time.sleep(5)

    # Maximize the window to ensure the layout is predictable
    driver.maximize_window()
    time.sleep(2)

    # Assuming you take a screenshot and save it as 'screen.png'
    im = pyautogui.screenshot('screen.png')

    # Take a screenshot of the current state of the browser
    screenshot_path = "browser_screenshot.png"
    driver.save_screenshot(screenshot_path)

    # Load the screenshot and the template
    main_image = cv2.imread(screenshot_path)
    template = cv2.imread("play_online_template.png", 0)

    # Convert the main image to grayscale
    gray_main = cv2.cvtColor(main_image, cv2.COLOR_BGR2GRAY)

    # Perform template matching
    result = cv2.matchTemplate(gray_main, template, cv2.TM_CCOEFF_NORMED)
        # # Define a threshold for detecting the match
    threshold = 0.8
    loc = np.where(result >= threshold)

    # Load the screenshot and template
    img_rgb = cv2.imread('screen.png')
    # main_image = cv2.cvtColor(img_rgb)
    main_image = cv2.imread('screen.png', cv2.IMREAD_GRAYSCALE)  # 大图
    template = cv2.imread('play_online_template.png',cv2.IMREAD_GRAYSCALE)
    h, w = template.shape[::-1] #反转得到图像的高和宽（灰度图像）
    print(h)
    print(w)
        # Draw rectangles around the detected areas and get the center of the first match
    # for pt in zip(*loc[::-1]):
        # Calculate the center of the detected template
        # center_of_match = (pt[0] + template.shape[1] // 2, pt[1] + template.shape[0] // 2)
        # break  # Remove this if you expect multiple matches and want to process them all

    # Save and show the result
    detected_image_path = "detected_template.png"
    cv2.imwrite(detected_image_path, main_image)
    print("Template matching completed. Results saved to:", detected_image_path)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    top_left = max_loc

    # print(min_val)
    # print(max_val)
    bottom_right = (top_left[0] + w, top_left[1] + h)
    cv2.rectangle(main_image, top_left, bottom_right, 255, 2)

    match_img = img_rgb.copy()



    # Calculate the center of the matched region
    center_x = top_left[0] 
    center_y = top_left[1]  
    # print(center_x)
    # print(center_y)

    # Move to the center of the matched region and click
    pyautogui.moveTo(top_left[0], top_left[1]  , duration=1)
    pyautogui.click()
    time.sleep(5)

    print('end')
    driver.quit()

def helper_getSystem():
    os_name = platform.system()
    service = None

    if os_name in ['Windows', 'Darwin', 'Linux']:
        service = Service(ChromeDriverManager().install())
    else:
        raise Exception(f"Unsupported operating system: {os_name}")

    driver = webdriver.Chrome(service=service)
    return driver

# main methods
if __name__ == "__main__":
    url = "https://www.chess.com/"
    click_play(url)
    time.sleep(5)
