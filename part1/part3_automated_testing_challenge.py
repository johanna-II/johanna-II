import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TestRegistration:
    @pytest.fixture(scope="class")
    def driver(self):
        driver = webdriver.Chrome()  # Make sure you have the appropriate WebDriver installed
        driver.implicitly_wait(10)  # Set an implicit wait for elements to be present
        yield driver
        driver.quit()

    @staticmethod
    def fill_registration_form(driver, username, password, email, subscribe_newsletter=True):
        driver.find_element(By.NAME, "username").send_keys(username)
        driver.find_element(By.NAME, "password").send_keys(password)
        driver.find_element(By.NAME, "email").send_keys(email)
        if subscribe_newsletter:
            driver.find_element(By.NAME, "subscribe_newsletter").click()

    @staticmethod
    def submit_registration_form(driver):
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    def test_successful_registration(self, driver):
        driver.get("http://13.209.85.69")
        self.fill_registration_form(driver, "johndoe", "password123", "johndoe@example.com")
        self.submit_registration_form(driver)
        success_message = driver.find_element(By.CSS_SELECTOR, ".success-message").text
        assert success_message == "Registration successful"

    @pytest.mark.parametrize("missing_field", ["username", "password", "email"])
    def test_missing_required_field(self, driver, missing_field):
        driver.get("http://13.209.85.69")
        if missing_field != "username":
            driver.find_element(By.NAME, "username").send_keys("johndoe")
        if missing_field != "password":
            driver.find_element(By.NAME, "password").send_keys("password123")
        if missing_field != "email":
            driver.find_element(By.NAME, "email").send_keys("johndoe@example.com")
        self.submit_registration_form(driver)
        error_message = driver.find_element(By.CSS_SELECTOR, ".error-message").text
        assert f"{missing_field.capitalize()} is required" in error_message

    def test_invalid_email_format(self, driver):
        driver.get("http://13.209.85.69")
        self.fill_registration_form(driver, "johndoe", "password123", "johndoe@example")
        self.submit_registration_form(driver)
        error_message = driver.find_element(By.CSS_SELECTOR, ".error-message").text
        assert "Invalid email format" in error_message

    def test_username_already_exists(self, driver):
        driver.get("http://13.209.85.69")
        self.fill_registration_form(driver, "existinguser", "password123", "existinguser@example.com")
        self.submit_registration_form(driver)
        error_message = driver.find_element(By.CSS_SELECTOR, ".error-message").text
        assert "Username already exists" in error_message

    def test_password_too_short(self, driver):
        driver.get("http://13.209.85.69")
        self.fill_registration_form(driver, "johndoe", "pass", "johndoe@example.com")
        self.submit_registration_form(driver)
        error_message = driver.find_element(By.CSS_SELECTOR, ".error-message").text
        assert "Password must be at least 8 characters long" in error_message

    def test_password_complexity(self, driver):
        driver.get("http://13.209.85.69")
        self.fill_registration_form(driver, "johndoe", "password", "johndoe@example.com")
        self.submit_registration_form(driver)
        error_message = driver.find_element(By.CSS_SELECTOR, ".error-message").text
        assert "Password must contain at least one uppercase letter, one lowercase letter, and one digit" in error_message

    def test_username_special_characters(self, driver):
        driver.get("http://13.209.85.69")
        self.fill_registration_form(driver, "john#doe", "password123", "johndoe@example.com")
        self.submit_registration_form(driver)
        error_message = driver.find_element(By.CSS_SELECTOR, ".error-message").text
        assert "Username can only contain alphanumeric characters and underscores" in error_message

    def test_email_already_registered(self, driver):
        driver.get("http://13.209.85.69")
        self.fill_registration_form(driver, "johndoe", "password123", "existingemail@example.com")
        self.submit_registration_form(driver)
        error_message = driver.find_element(By.CSS_SELECTOR, ".error-message").text
        assert "Email is already registered" in error_message

    def test_terms_and_conditions_not_accepted(self, driver):
        driver.get("http://13.209.85.69")
        self.fill_registration_form(driver, "johndoe", "password123", "johndoe@example.com", subscribe_newsletter=False)
        driver.find_element(By.NAME, "terms_and_conditions").click()
        self.submit_registration_form(driver)
        error_message = driver.find_element(By.CSS_SELECTOR, ".error-message").text
        assert "You must accept the terms and conditions" in error_message
