import json
import logging
import os
from typing import Any

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager


def crack_data(data: str, driver_path: str = "") -> Any:
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    if driver_path:
        driver = webdriver.Chrome(service=ChromeService(executable_path=driver_path), options=chrome_options)
    else:
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)

    try:
        fileabsdir = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
        url = f"file://{os.path.join(fileabsdir,'index.html')}"
        driver.get(url)
        res = driver.execute_script(f"return calc('${data}')")
        driver.quit()
        ret = json.loads(res)
        return ret
    except Exception as e:
        logging.error("==================================== ERRORS ====================================")
        logging.error("Download ChromeDriver: ")
        logging.error(
            "https://www.selenium.dev/documentation/webdriver/getting_started/install_drivers/#1-driver-management-software"
        )
        logging.error("https://chromedriver.chromium.org/downloads/version-selection")
        logging.error("==================================== ERRORS ====================================")
        logging.exception(e)
        raise e
