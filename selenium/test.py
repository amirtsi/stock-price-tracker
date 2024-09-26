import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service as ChromeService
from time import sleep
import os

class TestStockExchange:
    @pytest.fixture(scope="class")
    def init_driver(self):
        """Fixture to set up and tear down the driver."""
        self.driver_path = '/usr/local/bin/chromedriver'
        self.application_url = "http://127.0.0.1"
        service = ChromeService(executable_path=self.driver_path)
        self.driver = webdriver.Chrome(service=service, options=Options())
        self.driver.get(self.application_url)
        yield
        self.driver.quit()

    def test_stock_change_button(self, init_driver):
        """Test that stocks are changing."""
        button_element = '/html/body/div[1]/div/div/h2/select'
        WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH, button_element)))
        select = Select(self.driver.find_element(By.XPATH, button_element))
        sleep(5)
        for item in ['FB', 'IBM', 'TSLA', 'GOOGL', 'AMZN']:
            try:
                select.select_by_value(item)
                print(f'[SUCCESS] Found value {item}')
                sleep(2)
            except:
                print(f'[ERROR] Cannot find value {item}')

    def test_chart_exists(self, init_driver):
        """Test that chart exists."""
        try:
            self.driver.find_element(By.CLASS_NAME, 'js-plotly-plot')
            print("[SUCCESS] Chart exists")
        except NoSuchElementException:
            print("[ERROR] Chart not found")

    def test_plot_navigation_bar(self, init_driver):
        """Test interaction with plotly chart navigation bar."""
        WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.CLASS_NAME, 'js-plotly-plot')))
        elements = {
            'zoom_in': '/html/body/div[1]/div/div/div/div/div/div[2]/div/div[3]/a[1]',
            'zoom_out': '/html/body/div[1]/div/div/div/div/div/div[2]/div/div[3]/a[2]'
        }
        for element, xpath in elements.items():
            try:
                self.driver.find_element(By.XPATH, xpath).click()
                print(f'[SUCCESS] Successfully clicked on {element}')
                sleep(2)
            except:
                print(f'[ERROR] Error clicking on {element}')

    def test_download_chart_png(self, init_driver):
        """Test downloading the chart as a PNG."""
        default_download_dir = os.path.join(os.path.expanduser("~"), "Downloads")
        WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.CLASS_NAME, 'js-plotly-plot')))
        data_point = self.driver.find_element(By.XPATH, '/html/body/div/div/div/div/div/div/div[2]/div/div[1]').click()
        downloaded_file = os.path.join(default_download_dir, "newplot.png")

        if os.path.exists(downloaded_file):
            print(f"[SUCCESS] File downloaded successfully to {downloaded_file}!")
        else:
            print("[ERROR] File download failed or file not found.")
        sleep(2)
