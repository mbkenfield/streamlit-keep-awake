from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException
import os
import sys

# Streamlit app URLs from environment variable (comma-separated) or defaults
STREAMLIT_URL = os.environ.get(
    "STREAMLIT_URL",
    "https://estimatework.streamlit.app/,https://rsicalculator.streamlit.app/"
)

STREAMLIT_URLS = [url.strip() for url in STREAMLIT_URL.split(",") if url.strip()]


def main():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    try:
        for url in STREAMLIT_URLS:
            print(f"\nOpening {url}")
            driver.get(url)

            wait = WebDriverWait(driver, 15)

            try:
                button = wait.until(
                    EC.element_to_be_clickable(
                        (By.XPATH, "//button[contains(text(),'Yes, get this app back up')]")
                    )
                )
                print("Wake-up button found. Clicking...")
                button.click()

                try:
                    wait.until(
                        EC.invisibility_of_element_located(
                            (By.XPATH, "//button[contains(text(),'Yes, get this app back up')]")
                        )
                    )
                    print("Button clicked and disappeared ✅ (app waking up)")
                except TimeoutException:
                    print("Button clicked but did not disappear ❌")
                    sys.exit(1)

            except TimeoutException:
                print("No wake-up button found. App already awake ✅")

    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)
    finally:
        driver.quit()
        print("\nScript finished.")


if __name__ == "__main__":
    main()
