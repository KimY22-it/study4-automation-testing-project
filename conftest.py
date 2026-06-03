import pytest

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from screenshot_utility import take_screenshot

@pytest.fixture(scope="module")
def driver():
    options = webdriver.ChromeOptions()
    options.set_capability("unhandledPromptBehavior", "ignore")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument(r"--user-data-dir=D:\selenium_profile_new")
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )
    driver.maximize_window()
    yield driver
    driver.quit()


MODULE_STATS = {}

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call":
        module_name = item.path.stem if hasattr(item, "path") else item.fspath.purebasename
        if module_name not in MODULE_STATS:
            MODULE_STATS[module_name] = {'passed': 0, 'failed': 0, 'skipped': 0, 'total': 0}
            
        MODULE_STATS[module_name]['total'] += 1
        if report.passed:
            MODULE_STATS[module_name]['passed'] += 1
        elif report.failed:
            MODULE_STATS[module_name]['failed'] += 1
        elif report.skipped:
            MODULE_STATS[module_name]['skipped'] += 1

    if report.when == "call" and report.failed:
        driver = item.funcargs.get("driver")
        if not driver:
            for arg in item.funcargs.values():
                if hasattr(arg, "driver"):
                    driver = arg.driver
                    break
        if driver: 
            take_screenshot(driver, f"FAILED_{item.name}")

# --- PYTEST-HTML REPORT CUSTOMIZATION ---

def pytest_html_report_title(report):
    report.title = "Báo cáo kiểm thử – Study4.com"

def pytest_html_results_summary(prefix, summary, postfix):
    # Thêm mô tả tính năng bằng chuỗi HTML (tương thích pytest-html v4)
    prefix.extend([
        '<div class="feature-chips">',
        '  <span class="chip">🔍 Tìm kiếm & lọc đề thi online</span>',
        '  <span class="chip">📝 Luyện tập đề thi online</span>',
        '  <span class="chip">📚 Sửa từ & luyện tập flashcard</span>',
        '</div>'
    ])

    # Bảng thống kê theo Module
    if MODULE_STATS:
        stats_html = [
            '<div class="module-stats-container">',
            '  <h2 style="margin-top:20px; margin-bottom: 10px;">Thống kê theo Module</h2>',
            '  <table class="module-stats-table">',
            '    <thead>',
            '      <tr><th>Module</th><th>Tổng Test</th><th>Passed ✅</th><th>Failed ❌</th><th>Skipped ⏭</th></tr>',
            '    </thead>',
            '    <tbody>'
        ]
        
        for mod, stats in MODULE_STATS.items():
            stats_html.append('<tr>')
            stats_html.append(f'  <td><strong>{mod}</strong></td>')
            stats_html.append(f'  <td>{stats["total"]}</td>')
            stats_html.append(f'  <td style="color:var(--passed-color); font-weight:bold;">{stats["passed"]}</td>')
            stats_html.append(f'  <td style="color:var(--failed-color); font-weight:bold;">{stats["failed"]}</td>')
            stats_html.append(f'  <td style="color:var(--warning-color);">{stats["skipped"]}</td>')
            stats_html.append('</tr>')
            
        stats_html.append('    </tbody>')
        stats_html.append('  </table>')
        stats_html.append('</div>')

        prefix.extend(stats_html)

