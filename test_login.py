from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from config import BASE_URL, USERNAME, PASSWORD


def _login(driver, wait, username, password):
    driver.get(f"{BASE_URL}/auth/login")
    wait.until(EC.visibility_of_element_located((By.NAME, "username"))).send_keys(username)
    driver.find_element(By.NAME, "password").send_keys(password)
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()


def test_login_valid_credentials(driver, wait):
    _login(driver, wait, USERNAME, PASSWORD)
    header = wait.until(EC.visibility_of_element_located(
        (By.XPATH, "//h6[normalize-space()='Dashboard']")))
    assert header.text == "Dashboard"


def test_login_invalid_credentials(driver, wait):
    _login(driver, wait, USERNAME, "salah123")
    alert = wait.until(EC.visibility_of_element_located(
        (By.CSS_SELECTOR, ".oxd-alert-content-text")))
    assert alert.text == "Invalid credentials"


def test_logout(logged_in, wait):
    logged_in.find_element(By.CSS_SELECTOR, ".oxd-userdropdown-tab").click()
    wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Logout"))).click()
    wait.until(EC.visibility_of_element_located((By.NAME, "username")))
    assert "/auth/login" in logged_in.current_url