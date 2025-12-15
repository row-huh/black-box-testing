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
        options = webdriver.ChromeOptions()
        options.add_argument('--use-fake-ui-for-media-stream')
        options.add_argument('--use-fake-device-for-media-stream')
        self.driver = webdriver.Chrome(options=options)
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 20)

    def navigate_to_home(self):
        self.driver.get(self.base_url)
        time.sleep(2)

    def click_record_new_exercise(self):
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
                raise

    def start_recording(self):
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
                raise

    def upload_video_file(self, filename="Untitled.mp4"):
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
            current_dir = os.path.dirname(os.path.abspath(__file__))
            test_videos_folder = os.path.join(current_dir, "test-videos")
            file_path = os.path.join(test_videos_folder, filename)
            if not os.path.exists(file_path):
                pass
            file_input.send_keys(file_path)
            time.sleep(3)
        except TimeoutException:
            raise

    def analyze_and_save_exercise(self):
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
            self.wait.until(
                EC.presence_of_element_located((By.XPATH, 
                    "//*[contains(text(), 'Detecting pose') or contains(text(), 'detecting pose') or "
                    "contains(text(), 'Detecting') or contains(text(), 'Processing')]"))
            )
            try:
                ok_button = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, 
                        "//button[contains(text(), 'OK') or contains(text(), 'Ok') or contains(text(), 'ok')]"))
                )
                ok_button.click()
                time.sleep(2)
            except TimeoutException:
                pass
        except Exception as e:
            try:
                self.driver.save_screenshot("analyze_error.png")
            except:
                pass
            raise

    def wait_for_processing(self, timeout=180):
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
                    break
            except Exception as e:
                pass
            time.sleep(3)  
        time.sleep(2)  

    def handle_popup(self):
        try:
            ok_button = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, 
                    "//button[contains(text(), 'OK') or contains(text(), 'Ok') or contains(text(), 'ok')]"))
            )
            ok_button.click()
            time.sleep(2)
        except TimeoutException:
            pass

    def click_play(self):
        try:
            play_button = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, 
                    "//*[contains(text(), 'Play') or contains(text(), 'play')] | //button[@aria-label='Play'] | //*[@class*='play']"))
            )
            play_button.click()
            time.sleep(3)  
        except TimeoutException:
            try:
                play_button = self.driver.find_element(By.CSS_SELECTOR, 
                    "button[class*='play'], [data-testid*='play'], .play-button")
                play_button.click()
                time.sleep(3)
            except NoSuchElementException:
                raise

    def save_template_for_comparison(self):
        try:
            save_template_button = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, 
                    "//*[contains(text(), 'Save template') or contains(text(), 'Save Template') or contains(text(), 'template')]"))
            )
            save_template_button.click()
            time.sleep(2)
        except TimeoutException:
            raise

    def click_ok_after_save(self):
        self.handle_popup()

    def go_to_home(self):
        try:
            home_button = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, 
                    "//*[contains(text(), 'Home') or contains(text(), 'home')]"))
            )
            home_button.click()
            time.sleep(2)
        except TimeoutException:
            self.driver.get(self.base_url)
            time.sleep(2)

    def click_knee_extension_compare(self):
        try:
            knee_extension = self.wait.until(
                EC.presence_of_element_located((By.XPATH, 
                    "//*[contains(text(), 'knee extension') or contains(text(), 'Knee Extension')]"))
            )
            compare_button = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, 
                    "//*[contains(text(), 'knee extension') or contains(text(), 'Knee Extension')]//*[contains(text(), 'Compare')] | "
                    "//*[contains(text(), 'knee extension') or contains(text(), 'Knee Extension')]//following::*[contains(text(), 'Compare')][1] | "
                    "//*[contains(text(), 'knee extension') or contains(text(), 'Knee Extension')]//ancestor::*//button[contains(text(), 'Compare')]"))
            )
            compare_button.click()
            time.sleep(2)
        except TimeoutException:
            raise

    def record_with_webcam(self):
        try:
            webcam_button = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, 
                    "//*[contains(text(), 'Record with webcam') or contains(text(), 'Webcam') or contains(text(), 'webcam')]"))
            )
            webcam_button.click()
            time.sleep(2)
        except TimeoutException:
            raise

    def test_with_video_file(self, filename="Seated knee extension.mp4"):
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
            current_dir = os.path.dirname(os.path.abspath(__file__))
            test_videos_folder = os.path.join(current_dir, "test-videos")
            file_path = os.path.join(test_videos_folder, filename)
            if not os.path.exists(file_path):
                pass
            file_input.send_keys(file_path)
            time.sleep(3)
        except TimeoutException:
            raise

    def run_complete_test(self):
        try:
            self.setup_driver()
            self.navigate_to_home()
            self.click_record_new_exercise()
            self.start_recording()
            self.upload_video_file("Untitled.mp4")
            self.analyze_and_save_exercise()
            self.wait_for_processing()
            self.handle_popup()
            self.click_play()
            self.save_template_for_comparison()
            self.click_ok_after_save()
            self.go_to_home()
            self.click_knee_extension_compare()
            self.record_with_webcam()
            self.test_with_video_file("Seated knee extension.mp4")
        except Exception as e:
            import traceback
            traceback.print_exc()
        finally:
            if self.driver:
                self.driver.quit()

if __name__ == "__main__":
    test = ExerciseRecordingTest(base_url="http://localhost:3000")
    test.run_complete_test()
