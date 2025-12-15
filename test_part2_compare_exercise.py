"""
Selenium automation script - Part 2: Compare Exercise with Video
Website: localhost:3000

This script covers:
- Click OK after saving template
- Go to home
- Click on knee extension and compare
- Record with webcam
- Test with video file (Seated knee extension.mp4)
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
import time
import os

class ExerciseComparisonPart2:
    def __init__(self, base_url="http://localhost:3000"):
        self.base_url = base_url
        self.driver = None
        self.wait = None
        
    def setup_driver(self):
        """Initialize the Chrome WebDriver"""
        options = webdriver.ChromeOptions()
        options.add_argument('--use-fake-ui-for-media-stream')
        options.add_argument('--use-fake-device-for-media-stream')
        
        self.driver = webdriver.Chrome(options=options)
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 20)
        
    def navigate_to_home(self):
        """Navigate to the home page"""
        print("Navigating to home page...")
        self.driver.get(self.base_url)
        time.sleep(2)
        
    def handle_popup(self):
        """Handle popup if it appears and click OK - continues if no popup found"""
        print("Checking for popup...")
        try:
            ok_button = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, 
                    "//button[contains(text(), 'OK') or contains(text(), 'Ok') or contains(text(), 'ok')]"))
            )
            ok_button.click()
            print("Popup OK button clicked")
            time.sleep(2)
        except TimeoutException:
            print("No popup found, continuing...")
        except Exception as e:
            print(f"Error while checking for popup: {str(e)}, continuing anyway...")
            pass
            
    def click_ok_after_save(self):
        """Click OK after saving template"""
        print("Clicking OK after save...")
        self.handle_popup()
        
    def go_to_home(self):
        print("Navigating to home...")
        try:
            home_button = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, 
                    "//*[contains(text(), 'Home') or contains(text(), 'home')]"))
            )
            home_button.click()
            time.sleep(2)
            
        except TimeoutException:
            print("Home button not found, navigating to base URL...")
            self.driver.get(self.base_url)
            time.sleep(2)
            
    def click_knee_extension_compare(self):
        print("Looking for 'knee extension' and clicking compare...")
        try:
            knee_extension = self.wait.until(
                EC.presence_of_element_located((By.XPATH, 
                    "//*[contains(text(), 'knee extension') or contains(text(), 'Knee Extension')]"))
            )
            print("Found knee extension entry")
            
            compare_button = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, 
                    "//*[contains(text(), 'knee extension') or contains(text(), 'Knee Extension')]//*[contains(text(), 'Compare')] | "
                    "//*[contains(text(), 'knee extension') or contains(text(), 'Knee Extension')]//following::*[contains(text(), 'Compare')][1] | "
                    "//*[contains(text(), 'knee extension') or contains(text(), 'Knee Extension')]//ancestor::*//button[contains(text(), 'Compare')]"))
            )
            compare_button.click()
            time.sleep(2)
            
        except TimeoutException:
            print("Could not find knee extension or compare button")
            raise
            
    def record_with_webcam(self):
        """Click on record with webcam option"""
        print("Clicking 'Record with webcam'...")
        try:
            webcam_button = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, 
                    "//*[contains(text(), 'Record with webcam') or contains(text(), 'Webcam') or contains(text(), 'webcam')]"))
            )
            webcam_button.click()
            time.sleep(2)
            
        except TimeoutException:
            print("Could not find 'Record with webcam' button")
            raise
            
    def test_with_video_file(self, filename="Seated knee extension.mp4"):
        print(f"Testing with video file: {filename}...")
        try:
            test_video_button = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, 
                    "//*[contains(text(), 'test with video') or contains(text(), 'Test with video') or contains(text(), 'video file')]"))
            )
            test_video_button.click()
            time.sleep(2)
            
            file_input = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='file']"))
            )
            
            downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads")
            file_path = os.path.join(downloads_folder, filename)
            
            if not os.path.exists(file_path):
                print(f"Warning: File {file_path} does not exist in Downloads folder.")
                print(f"Please ensure {filename} is in your Downloads folder: {downloads_folder}")
            else:
                print(f"Found file at: {file_path}")
            
            file_input.send_keys(file_path)
            time.sleep(3)
            print(f"File {filename} uploaded successfully from Downloads folder")
            
        except TimeoutException:
            print("Could not find 'Test with video' option or file input")
            raise
            
    def run_part2_test(self):
        try:
            print("=" * 60)
            print("Starting Part 2: Compare Exercise with Video")
            print("=" * 60)
            
            self.setup_driver()
            self.navigate_to_home()
            self.click_ok_after_save()
            self.go_to_home()
            self.click_knee_extension_compare()
            self.record_with_webcam()
            self.test_with_video_file("Seated knee extension.mp4")
            
            print("=" * 60)
            print("Part 2 completed successfully!")
            print("=" * 60)
            
            input("Press Enter to close the browser...")
            
        except Exception as e:
            print(f"\n{'=' * 60}")
            print(f"Part 2 failed with error: {str(e)}")
            print(f"{'=' * 60}")
            import traceback
            traceback.print_exc()
            
            input("Press Enter to close the browser...")
            
        finally:
            if self.driver:
                self.driver.quit()
                print("Browser closed")


if __name__ == "__main__":
    test = ExerciseComparisonPart2(base_url="http://localhost:3000")
    test.run_part2_test()
