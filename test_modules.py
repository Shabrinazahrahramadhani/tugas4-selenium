import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from config import BASE_URL

MODULES = [
    ("dashboard/index", "Dashboard"),
    ("admin/viewSystemUsers", "System Users"),
    ("pim/viewEmployeeList", "Employee Information"),
    ("pim/viewMyDetails", "Personal Details"),
    ("leave/viewLeaveList", "Leave List"),
    ("leave/viewLeaveEntitlements", "Leave Entitlements"),
    ("time/viewMyTimesheet", "Timesheet"),
    ("attendance/viewAttendanceRecord", "Attendance"),
    ("time/viewCustomers", "Customers"),
    ("recruitment/viewCandidates", "Candidates"),
    ("recruitment/viewJobVacancy", "Vacancies"),
    ("performance/searchKpi", "Key Performance Indicators"),
    ("performance/searchPerformanceReview", "Manage Performance Reviews"),
    ("directory/viewDirectory", "Directory"),
    ("claim/viewEvents", "Event"),
]


@pytest.mark.parametrize("path,title", MODULES, ids=[p for p, _ in MODULES])
def test_open_page(logged_in, wait, path, title):
    logged_in.get(f"{BASE_URL}/{path}")
    locator = (By.XPATH, f"//*[self::h5 or self::h6][contains(normalize-space(.),'{title}')]")
    assert wait.until(EC.visibility_of_element_located(locator))