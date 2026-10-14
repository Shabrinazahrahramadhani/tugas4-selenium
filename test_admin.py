import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from config import BASE_URL


def test_admin_search_user(logged_in, wait):
    logged_in.get(f"{BASE_URL}/admin/viewSystemUsers")
    box = wait.until(EC.visibility_of_element_located(
        (By.XPATH, "//label[normalize-space()='Username']/../following-sibling::div//input")))
    box.send_keys("Admin")
    logged_in.find_element(By.XPATH, "//button[normalize-space()='Search']").click()
    assert wait.until(EC.visibility_of_element_located(
        (By.XPATH, "//div[@role='row']//div[normalize-space()='Admin']")))


def test_admin_add_job_title(logged_in, wait):
    logged_in.get(f"{BASE_URL}/admin/viewJobTitleList")
    wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Add']"))).click()
    field = wait.until(EC.visibility_of_element_located(
        (By.XPATH, "//label[normalize-space()='Job Title']/../following-sibling::div//input")))
    field.send_keys(f"QA Tester {int(time.time())}")
    logged_in.find_element(By.XPATH, "//button[normalize-space()='Save']").click()
    assert wait.until(EC.visibility_of_element_located(
        (By.XPATH, "//p[contains(normalize-space(.),'Successfully Saved')]")))