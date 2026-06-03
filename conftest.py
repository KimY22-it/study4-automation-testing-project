import pytest
import os
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from screenshot_utility import take_screenshot

BASE_DIR = Path(__file__).resolve().parent
REPORTS_DIR = BASE_DIR / "reports"
CSS_FILE = REPORTS_DIR / "custom_style.css"

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
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    extras = getattr(report, "extras", [])

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
            # Vẫn lưu file screenshot ra thư mục
            take_screenshot(driver, f"FAILED_{item.name}")
            # Thêm ảnh vào report HTML trực tiếp (base64) để giao diện báo cáo rõ ràng
            try:
                screenshot_b64 = driver.get_screenshot_as_base64()
                pytest_html = item.config.pluginmanager.getplugin("html")
                if pytest_html:
                    extras.append(pytest_html.extras.image(screenshot_b64, name="📸 Ảnh lỗi (Click để phóng to)"))
            except Exception as e:
                print(f"Lỗi chụp ảnh: {e}")

    report.extras = extras


# --- PYTEST-HTML REPORT CUSTOMIZATION ---

def pytest_html_report_title(report):
    report.title = "Báo cáo kiểm thử – Study4.com"

def pytest_html_results_summary(prefix, summary, postfix):
    # Inject file CSS giao diện Glassmorphism
    if CSS_FILE.exists():
        css_content = CSS_FILE.read_text(encoding="utf-8")
        prefix.append(f'<style>\n{css_content}\n</style>')

    # 1. Mô tả Website và Chức năng kiểm thử (Tối giản, Padding rõ ràng)
    description_html = """
    <div style="background: rgba(255, 255, 255, 0.7); backdrop-filter: blur(16px); padding: 32px; border-radius: 16px; margin-bottom: 32px; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05); border: 1px solid rgba(0, 0, 0, 0.06);">
        <h2 style="margin-top: 0; color: #1e293b; font-size: 22px; font-weight: 700; border-bottom: 1px solid rgba(0,0,0,0.06); padding-bottom: 12px; margin-bottom: 16px;">
            🌐 Giới thiệu Hệ thống & Mục tiêu Kiểm thử
        </h2>
        <p style="color: #475569; font-size: 15px; line-height: 1.7; margin-bottom: 20px;">
            <strong>Study4.com</strong> là nền tảng giáo dục trực tuyến chuyên cung cấp các khóa học và đề thi thử cho các chứng chỉ tiếng Anh như TOEIC, IELTS. 
            Báo cáo này trình bày chi tiết kết quả chạy tự động <strong>(Automation Testing)</strong> trên giao diện người dùng (UI) nhằm đảm bảo hệ thống hoạt động ổn định và mang lại trải nghiệm tốt nhất.
        </p>
        <h3 style="margin-top: 0; color: #334155; font-size: 16px; font-weight: 600; margin-bottom: 12px;">Các luồng tính năng chính được bao phủ:</h3>
        <div class="feature-chips" style="margin-bottom: 0;">
            <span class="chip">🔍 Tìm kiếm & Lọc đề thi online</span>
            <span class="chip">📝 Luyện tập & Làm bài thi thử</span>
            <span class="chip">📚 Quản lý & Học từ vựng Flashcard</span>
            <span class="chip">⚡ Hiệu năng UI & Xử lý lỗi</span>
        </div>
    </div>
    """
    prefix.append(description_html)

    # 2. Bảng tổng số test Pass/Fail của các Module (Tối giản, Rõ ràng)
    if MODULE_STATS:
        total_tests = 0
        total_passed = 0
        total_failed = 0
        total_skipped = 0
        
        for mod, stats in MODULE_STATS.items():
            total_tests += stats["total"]
            total_passed += stats["passed"]
            total_failed += stats["failed"]
            total_skipped += stats["skipped"]

        stats_html = [
            '<div class="module-stats-container" style="background: rgba(255, 255, 255, 0.7); backdrop-filter: blur(16px); padding: 32px; border-radius: 16px; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05); border: 1px solid rgba(0, 0, 0, 0.06); margin-bottom: 32px;">',
            '  <h2 style="margin-top: 0; color: #1e293b; font-size: 22px; font-weight: 700; border-bottom: 1px solid rgba(0,0,0,0.06); padding-bottom: 12px; margin-bottom: 20px;">',
            '    📊 Tổng kết Pass/Fail theo Module',
            '  </h2>',
            '  <table class="module-stats-table" style="width: 100%; border-collapse: separate; border-spacing: 0;">',
            '    <thead>',
            '      <tr>',
            '        <th style="background: rgba(255,255,255,0.5); padding: 16px; text-align: left; color: #64748b; font-weight: 700; text-transform: uppercase; font-size: 13px; border-bottom: 2px solid rgba(0,0,0,0.06); border-top-left-radius: 8px;">Module (File Test)</th>',
            '        <th style="background: rgba(255,255,255,0.5); padding: 16px; text-align: center; color: #64748b; font-weight: 700; text-transform: uppercase; font-size: 13px; border-bottom: 2px solid rgba(0,0,0,0.06);">Tổng số Test</th>',
            '        <th style="background: rgba(255,255,255,0.5); padding: 16px; text-align: center; color: var(--passed); font-weight: 700; text-transform: uppercase; font-size: 13px; border-bottom: 2px solid rgba(0,0,0,0.06);">Passed ✅</th>',
            '        <th style="background: rgba(255,255,255,0.5); padding: 16px; text-align: center; color: var(--failed); font-weight: 700; text-transform: uppercase; font-size: 13px; border-bottom: 2px solid rgba(0,0,0,0.06);">Failed ❌</th>',
            '        <th style="background: rgba(255,255,255,0.5); padding: 16px; text-align: center; color: var(--warning); font-weight: 700; text-transform: uppercase; font-size: 13px; border-bottom: 2px solid rgba(0,0,0,0.06); border-top-right-radius: 8px;">Skipped ⏭</th>',
            '      </tr>',
            '    </thead>',
            '    <tbody>'
        ]
        
        for mod, stats in MODULE_STATS.items():
            stats_html.append('<tr style="transition: background-color 0.2s;">')
            stats_html.append(f'  <td style="padding: 16px; border-bottom: 1px solid rgba(0,0,0,0.04); font-weight: 600; color: #334155;">{mod}</td>')
            stats_html.append(f'  <td style="padding: 16px; text-align: center; border-bottom: 1px solid rgba(0,0,0,0.04); color: #64748b; font-family: monospace; font-size: 15px;">{stats["total"]}</td>')
            stats_html.append(f'  <td style="padding: 16px; text-align: center; border-bottom: 1px solid rgba(0,0,0,0.04); color: var(--passed); font-weight: 700; font-family: monospace; font-size: 15px;">{stats["passed"]}</td>')
            stats_html.append(f'  <td style="padding: 16px; text-align: center; border-bottom: 1px solid rgba(0,0,0,0.04); color: var(--failed); font-weight: 700; font-family: monospace; font-size: 15px;">{stats["failed"]}</td>')
            stats_html.append(f'  <td style="padding: 16px; text-align: center; border-bottom: 1px solid rgba(0,0,0,0.04); color: var(--warning); font-family: monospace; font-size: 15px;">{stats["skipped"]}</td>')
            stats_html.append('</tr>')
            
        # Hàng TỔNG CỘNG
        stats_html.append('<tr style="background: rgba(241, 245, 249, 0.6);">')
        stats_html.append(f'  <td style="padding: 16px; border-bottom: none; font-weight: 700; color: #0f172a; border-bottom-left-radius: 8px;">TỔNG CỘNG</td>')
        stats_html.append(f'  <td style="padding: 16px; text-align: center; border-bottom: none; font-weight: 700; color: #0f172a; font-family: monospace; font-size: 16px;">{total_tests}</td>')
        stats_html.append(f'  <td style="padding: 16px; text-align: center; border-bottom: none; font-weight: 700; color: var(--passed); font-family: monospace; font-size: 16px;">{total_passed}</td>')
        stats_html.append(f'  <td style="padding: 16px; text-align: center; border-bottom: none; font-weight: 700; color: var(--failed); font-family: monospace; font-size: 16px;">{total_failed}</td>')
        stats_html.append(f'  <td style="padding: 16px; text-align: center; border-bottom: none; font-weight: 700; color: var(--warning); border-bottom-right-radius: 8px; font-family: monospace; font-size: 16px;">{total_skipped}</td>')
        stats_html.append('</tr>')

        stats_html.append('    </tbody>')
        stats_html.append('  </table>')
        stats_html.append('</div>')

        prefix.extend(stats_html)
