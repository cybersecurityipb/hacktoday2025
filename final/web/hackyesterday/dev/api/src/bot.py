import logging
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from sqlalchemy.orm import Session

from src.models import get_db, User

BASE_URL = "http://localhost"

def setup_driver():
    """Setup a headless Chrome driver"""
    chrome_executable = Service(executable_path="/usr/bin/chromedriver", log_path="NUL")
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    return webdriver.Chrome(service=chrome_executable, options=options)

def get_admin_credentials():
    """Returns the admin credentials"""
    db = next(get_db())
    admin = db.query(User).filter(User.is_admin == True).first()
    username, password = admin.username, admin.password
    db.close()
    return username, password

def login_and_view_challenges():
    """Simulates an admin user that logs in and views the challenges page"""
    logging.info("Starting bot...")
    driver = setup_driver()
    driver.get(BASE_URL + "/login")

    username, password = get_admin_credentials()
    username_input = driver.find_element(By.ID, "username")
    username_input.send_keys(username)

    password_input = driver.find_element(By.ID, "password")
    password_input.send_keys(password)

    login_button = driver.find_element(By.ID, "submit")
    login_button.click()
    logging.info("Logged in as '%s' with password '%s'.", username, password)

    time.sleep(3)
    driver.quit()
