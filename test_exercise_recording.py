"""
Selenium automation script for testing exercise recording functionality
Website: localhost:3000
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import os

class ExerciseRecordingTest:
    def __init__(self, base_url="http://localhost:3000"):
        self.base_url = base_url
        self.driver = None
        self.wait = None
        
    def setup_driver(self):
        """Initialize the Chrome WebDriver"""
        options = webdriver.ChromeOptions()
        # Add options to allow file uploads and camera access
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
        
    def click_record_new_exercise(self):
        """Click on 'Record New Exercise' button"""
        print("Clicking 'Record New Exercise'...")
        try:
            record_button = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, 
                    "//*[contains(text(), 'Record New Exercise') or contains(text(), 'record new exercise') or contains(text(), 'New Exercise')]"))
            )
            record_button.click()
            time.sleep(2)
        except TimeoutException:
            try:
                record_button = self.driver.find_element(By.CSS_SELECTOR, "button[data-testid*='record'], button[class*='record']")
                record_button.click()
                time.sleep(2)
            except NoSuchElementException:
                print("Could not find 'Record New Exercise' button")
                raise
                
    def start_recording(self):
        """Click on 'Start recording' button"""
        print("Clicking 'Start recording'...")
        try:
            start_button = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, 
                    "//*[contains(text(), 'Start recording') or contains(text(), 'Start Recording') or contains(text(), 'Start')]"))
            )
            start_button.click()
            time.sleep(2)
        except TimeoutException:
            try:
                start_button = self.driver.find_element(By.CSS_SELECTOR, "button[data-testid*='start'], button[class*='start']")
                start_button.click()
                time.sleep(2)
            except NoSuchElementException:
                print("Could not find 'Start recording' button")
                raise
                
    def upload_video_file(self, filename="Untitled.mp4"):
        """Upload video file from Downloads folder and analyze exercise"""
        print(f"Uploading video file: {filename}...")
        try:
            upload_button = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, 
                    "//*[contains(text(), 'Upload Video') or contains(text(), 'Upload File') or contains(text(), 'upload')]"))
            )
            upload_button.click()
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
            print("Could not find upload button or file input")
            raise
            
    def analyze_and_save_exercise(self):
        """Click on 'Analyze and save exercise' button and wait for pose detection"""
        print("Clicking 'Analyze and save exercise'...")
        try:
            analyze_button = None
            
            try:
                analyze_button = self.wait.until(
                    EC.element_to_be_clickable((By.XPATH, 
                        "//button[contains(text(), 'Analyze and save exercise') or "
                        "contains(text(), 'Analyze and Save Exercise') or "
                        "contains(text(), 'Analyze') or "
                        "contains(text(), 'analyze')]"))
                )
            except TimeoutException:
                analyze_button = self.driver.find_element(By.XPATH, 
                    "//*[contains(@class, 'analyze') or contains(@id, 'analyze') or "
                    "contains(text(), 'Save exercise')]")
            
            if analyze_button:
                analyze_button.click()
                print("'Analyze and save exercise' button clicked")
            else:
                raise Exception("Could not find 'Analyze and save exercise' button")
            
            print("Waiting for 'Detecting pose' text...")
            self.wait.until(
                EC.presence_of_element_located((By.XPATH, 
                    "//*[contains(text(), 'Detecting pose') or contains(text(), 'detecting pose') or "
                    "contains(text(), 'Detecting') or contains(text(), 'Processing')]"))
            )
            print("'Detecting pose' text found - processing started")
            

            try:
                print("Checking for popup error...")
                ok_button = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, 
                        "//button[contains(text(), 'OK') or contains(text(), 'Ok') or contains(text(), 'ok')]"))
                )
                ok_button.click()
                print("Popup error OK button clicked")
                time.sleep(2)
            except TimeoutException:
                print("No popup error found, continuing...")
            
        except Exception as e:
            print(f"Error in analyze_and_save_exercise: {str(e)}")
            try:
                self.driver.save_screenshot("analyze_error.png")
                print("Screenshot saved as analyze_error.png")
            except:
                pass
            raise
            
    def wait_for_processing(self, timeout=180):
        """Wait for processing to complete - waits until 'Detecting pose' text disappears"""
        print("Waiting for processing to finish...")
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            try:
        
                processing_elements = self.driver.find_elements(By.XPATH, 
                    "//*[contains(text(), 'Detecting pose') or "
                    "contains(text(), 'detecting pose') or "
                    "contains(text(), 'Detecting') or "
                    "contains(text(), 'Processing') or "
                    "contains(text(), 'processing') or "
                    "contains(text(), 'landmarks')]")
                
                if not processing_elements:
                    print("Processing completed - 'Detecting pose' text has disappeared")
                    break
                else:
                    print(f"Still processing... ({int(time.time() - start_time)}s elapsed)")
                    
            except Exception as e:
                print(f"Error checking processing status: {e}")
                pass
            
            time.sleep(3)  
            
        if time.time() - start_time >= timeout:
            print(f"Warning: Processing timeout reached ({timeout}s)")
        
        time.sleep(2)  
        
    def handle_popup(self):
        """Handle popup if it appears and click OK"""
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
            
    def click_play(self):
        """Click on play button"""
        print("Clicking play button...")
        try:
            play_button = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, 
                    "//*[contains(text(), 'Play') or contains(text(), 'play')] | //button[@aria-label='Play'] | //*[@class*='play']"))
            )
            play_button.click()
            print("Play button clicked")
            time.sleep(3)  # Wait 3 seconds as specified
            
        except TimeoutException:
            # Try to find play icon/button by CSS
            try:
                play_button = self.driver.find_element(By.CSS_SELECTOR, 
                    "button[class*='play'], [data-testid*='play'], .play-button")
                play_button.click()
                print("Play button clicked (alternative selector)")
                time.sleep(3)
            except NoSuchElementException:
                print("Could not find play button")
                raise
                
    def save_template_for_comparison(self):
        """Save template for comparison"""
        print("Saving template for comparison...")
        try:
            save_template_button = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, 
                    "//*[contains(text(), 'Save template') or contains(text(), 'Save Template') or contains(text(), 'template')]"))
            )
            save_template_button.click()
            time.sleep(2)
            
        except TimeoutException:
            print("Could not find 'Save template' button")
            raise
            
    def click_ok_after_save(self):
        """Click OK after saving template"""
        print("Clicking OK after save...")
        self.handle_popup()
        
    def go_to_home(self):
        """Navigate back to home"""
        print("Navigating to home...")
        try:
            # Try to find home button/link
            home_button = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, 
                    "//*[contains(text(), 'Home') or contains(text(), 'home')]"))
            )
            home_button.click()
            time.sleep(2)
            
        except TimeoutException:
            # Alternative: navigate directly to home URL
            print("Home button not found, navigating to base URL...")
            self.driver.get(self.base_url)
            time.sleep(2)
            
    def click_knee_extension_compare(self):
        """Click on knee extension compare option"""
        print("Looking for 'knee extension' and clicking compare...")
        try:
            # First find knee extension element
            knee_extension = self.wait.until(
                EC.presence_of_element_located((By.XPATH, 
                    "//*[contains(text(), 'knee extension') or contains(text(), 'Knee Extension')]"))
            )
            print("Found knee extension entry")
            
            # Find and click compare button (might be nearby or within the same container)
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
        """Upload video file for testing from Downloads folder"""
        print(f"Testing with video file: {filename}...")
        try:
            # Look for test with video file option
            test_video_button = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, 
                    "//*[contains(text(), 'test with video') or contains(text(), 'Test with video') or contains(text(), 'video file')]"))
            )
            test_video_button.click()
            time.sleep(2)
            
            # Find the file input element
            file_input = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='file']"))``
            )
            
            # Get the absolute path of the file from Downloads folder
            downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads")
            file_path = os.path.join(downloads_folder, filename)
            
            # Check if file exists
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
            
    def run_complete_test(self):
        """Execute the complete test flow"""
        try:
            print("=" * 60)
            print("Starting Exercise Recording Test")
            print("=" * 60)
            
            # Setup
            self.setup_driver()
            
            # Navigate to home
            self.navigate_to_home()
            
            # Step 1: Record New Exercise
            self.click_record_new_exercise()
            
            # Step 2: Start recording
            self.start_recording()
            
            # Step 3: Upload Video File (Untitled.mp4)
            self.upload_video_file("Untitled.mp4")
            
            # Step 4: Analyze and save exercise
            self.analyze_and_save_exercise()
            
            # Step 5: Wait for processing to finish
            self.wait_for_processing()
            
            # Step 6: Handle popup if present
            self.handle_popup()
            
            # Step 7: Click on play
            self.click_play()
            
            # Step 8: Save template for comparison
            self.save_template_for_comparison()
            
            # Step 9: Click OK
            self.click_ok_after_save()
            
            # Step 10: Go to home
            self.go_to_home()
            
            # Step 11: Click on knee extension compare
            self.click_knee_extension_compare()
            
            # Step 12: Record with webcam
            self.record_with_webcam()
            
            # Step 13: Test with video file (Seated knee extension.mp4)
            self.test_with_video_file("Seated knee extension.mp4")
            
            print("=" * 60)
            print("Test completed successfully!")
            print("=" * 60)
            
            # Keep browser open for inspection
            input("Press Enter to close the browser...")
            
        except Exception as e:
            print(f"\n{'=' * 60}")
            print(f"Test failed with error: {str(e)}")
            print(f"{'=' * 60}")
            import traceback
            traceback.print_exc()
            
            # Keep browser open for debugging
            input("Press Enter to close the browser...")
            
        finally:
            if self.driver:
                self.driver.quit()
                print("Browser closed")


if __name__ == "__main__":
    # Create test instance and run
    test = ExerciseRecordingTest(base_url="http://localhost:3000")
    test.run_complete_test()
