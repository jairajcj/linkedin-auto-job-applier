import json
import time
import random
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

class LinkedInBot:
    def __init__(self, config_path='config.json'):
        with open(config_path, 'r') as f:
            self.config = json.load(f)
        
        self.email = self.config.get('email')
        self.password = self.config.get('password')
        self.keywords = self.config.get('keywords')
        self.location = self.config.get('location')
        self.avoid_unpaid = self.config.get('avoid_unpaid', True)
        
        # Setup Chrome options
        options = webdriver.ChromeOptions()
        # options.add_argument('--headless') # Run in headless mode if needed
        options.add_argument('--start-maximized')
        options.add_argument('--disable-notifications')
        
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        self.wait = WebDriverWait(self.driver, 10)

    def login(self):
        print("Logging in...")
        self.driver.get('https://www.linkedin.com/login')
        try:
            username_field = self.wait.until(EC.presence_of_element_located((By.ID, 'username')))
            username_field.send_keys(self.email)
            
            password_field = self.driver.find_element(By.ID, 'password')
            password_field.send_keys(self.password)
            password_field.send_keys(Keys.RETURN)
            
            # Wait for login to complete (check for search bar or feed)
            self.wait.until(EC.presence_of_element_located((By.ID, 'global-nav-search')))
            print("Login successful.")
        except TimeoutException:
            print("Login failed or CAPTCHA detected. Please solve it manually.")
            time.sleep(30) # time to solve captcha

    def generate_url(self, keyword):
        base_url = "https://www.linkedin.com/jobs/search/?"
        params = [
            f"keywords={keyword}",
            f"location={self.location}"
        ]
        if self.config['filters'].get('easy_apply_only'):
            params.append("f_AL=true") # Easy Apply filter
            
        # Add other filters mapping if necessary (simplified for now)
        
        return base_url + "&".join(params)

    def is_paid_job(self, description_text):
        if not self.avoid_unpaid:
            return True
            
        text = description_text.lower()
        unpaid_keywords = ['unpaid', 'volunteer', 'no salary', 'for credit']
        for word in unpaid_keywords:
            if word in text:
                return False
        return True

    def apply_to_jobs(self):
        for keyword in self.keywords:
            url = self.generate_url(keyword)
            print(f"Searching for: {keyword}")
            self.driver.get(url)
            time.sleep(random.uniform(2, 4))
            
            # Find job cards
            try:
                job_list = self.wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.job-card-container--clickable')))
            except TimeoutException:
                print(f"No jobs found for {keyword}")
                continue

            limit = self.config.get('apply_limit', 5)
            count = 0
            
            for job in job_list:
                if count >= limit:
                    break
                    
                try:
                    # Scroll into view to ensure clickability
                    self.driver.execute_script("arguments[0].scrollIntoView();", job)
                    job.click()
                    time.sleep(random.uniform(1, 3))
                    
                    # Get Description to check for filters
                    description_element = self.driver.find_element(By.CLASS_NAME, 'jobs-description-content__text')
                    if not self.is_paid_job(description_element.text):
                        print("Skipping potential unpaid job.")
                        continue
                        
                    # Find Apply Button (More robust using text)
                    try:
                        apply_btn = self.driver.find_element(By.XPATH, "//button[contains(., 'Easy Apply')]")
                    except NoSuchElementException:
                        print("Easy Apply button not found (might be already applied or different type).")
                        continue
                        
                    apply_btn.click()
                    print("Clicked Easy Apply. Waiting 10 seconds for the form to load/for you to check...")
                    time.sleep(10)
                    
                    # Handle Easy Apply logic
                    # NOTE: This is highly variable. We will try to click "Next" or "Submit".
                    # Real implementation requires complex state management for form steps.
                    self.handle_application_form()
                    
                    count += 1
                except Exception as e:
                    print(f"Error processing job: {e}")
                    continue

    def handle_application_form(self):
        # A simple recursive or loop-based approach to clicking "Next" / "Review" / "Submit"
        # This is a basic skeleton.
        try:
            submit_button = None
            while True:
                time.sleep(1)
                buttons = self.driver.find_elements(By.TAG_NAME, 'button')
                
                # Look for typical buttons
                next_btn = None
                review_btn = None
                submit_btn = None
                
                for btn in buttons:
                    text = btn.text.lower()
                    if 'next' in text:
                        next_btn = btn
                    elif 'review' in text:
                        review_btn = btn
                    elif 'submit application' in text:
                        submit_btn = btn
                
                if submit_btn:
                    print("Found 'Submit Application' button. Waiting 10 seconds for you to review...")
                    time.sleep(10)
                    submit_btn.click()
                    print("Application Submitted!")
                    time.sleep(2)
                    # Close success modal
                    try:
                        close_btn = self.driver.find_element(By.CSS_SELECTOR, '[aria-label="Dismiss"]')
                        close_btn.click()
                    except:
                        pass
                    break
                elif review_btn:
                    print("Found 'Review' button. Waiting 10 seconds for you to review/answer...")
                    time.sleep(10)
                    review_btn.click()
                elif next_btn:
                    print("Found 'Next' button. Waiting 10 seconds for you to answer questions...")
                    time.sleep(10)
                    next_btn.click()
                else:
                    # If no obvious navigation button, we might be stuck or done.
                    # Or it might be asking for input we haven't provided.
                    # print("Waiting for standard buttons...")
                    pass
        except Exception as e:
            print(f"Form handling error: {e}")

    def run(self):
        self.login()
        self.apply_to_jobs()
        print("Done.")
        self.driver.quit()

if __name__ == "__main__":
    bot = LinkedInBot()
    bot.run()
