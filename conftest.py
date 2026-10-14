import os
from selenium.webdriver.firefox.options import Options

import base64
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pytest_html import extras

from config import BASE_URL, USERNAME, PASSWORD


GRID_URL = os.environ.get("GRID_URL")
HEADLESS = os.environ.get("HEADLESS") == "1"


@pytest.fixture
def driver(request):
    options = Options()
    if HEADLESS:
        options.add_argument("-headless")
    if GRID_URL:
        d = webdriver.Remote(command_executor=GRID_URL, options=options)
    else:
        d = webdriver.Firefox(options=options)
    d.set_window_size(1366, 900)
    request.node.driver = d
    yield d
    d.quit()

@pytest.fixture
def wait(driver):
    return WebDriverWait(driver, 30)


@pytest.fixture
def logged_in(driver, wait):
    driver.get(f"{BASE_URL}/auth/login")
    wait.until(EC.visibility_of_element_located((By.NAME, "username"))).send_keys(USERNAME)
    driver.find_element(By.NAME, "password").send_keys(PASSWORD)
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    wait.until(EC.visibility_of_element_located((By.XPATH, "//h6[normalize-space()='Dashboard']")))
    return driver


def pytest_html_report_title(report):
    report.title = "Laporan Pengujian OrangeHRM - Selenium WebDriver"


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when == "call":
        driver = getattr(item, "driver", None)
        if driver is not None:
            try:
                png = driver.get_screenshot_as_base64()
                report.extras = getattr(report, "extras", [])
                report.extras.append(extras.png(png))
            except Exception:
                pass