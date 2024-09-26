from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service as ChromeService
from time import sleep
import os

class StockExchangeTest():
    def __init__(self, driver: str, application_url: str = "http://51.21.3.43", download_dir: str = '/Users/zoharmurciano') -> None:
        self.driver = driver
        self.application_url = application_url
        se = ChromeService(executable_path=self.driver)
        self.executable_driver = webdriver.Chrome(service=se, options=Options())
    
    def init_webapp(self):
        self.executable_driver.get(self.application_url)

    def test_stock_change_button(self):
        """Test that stocks are changing."""

        button_element = '/html/body/div[1]/div/div/h2/select'
        WebDriverWait(self.executable_driver, 20).until(EC.element_to_be_clickable((By.XPATH, button_element)))
        select = Select(self.executable_driver.find_element(By.XPATH, button_element))
        sleep(5)

        # Check every stock that it's clickable
        for item in ['FB', 'IBM', 'TSLA', 'GOOGL', 'AMZN']:
            try:
                select.select_by_value(item)
                print(f'[SUCCESS] found value {item}')
                sleep(2)
            except:
                print(f'[ERROR] Cant find value {item}')

    def test_chart_exists(self):
        """Test that chart exists"""
        try:
            self.executable_driver.find_element(By.CLASS_NAME, 'js-plotly-plot')
            print("[SUCCESS] Chart exists")
        except NoSuchElementException:
            print("[ERROR] Chart not found")
    
    def test_plot_navigation_bar(self):
        """Test that you can download chart"""

        WebDriverWait(self.executable_driver, 20).until(EC.element_to_be_clickable((By.CLASS_NAME, 'js-plotly-plot')))
        elements = {
            'zoom_in': '/html/body/div[1]/div/div/div/div/div/div[2]/div/div[3]/a[1]',
            'zoom_out': '/html/body/div[1]/div/div/div/div/div/div[2]/div/div[3]/a[2]'

        }
        for element in elements:
            try:
                data_point = self.executable_driver.find_element(By.XPATH, elements[element]).click()
                print(f'[SUCCESS] success clicking on {element}')
                sleep(2)
            except:
                print(f'[ERROR] error clicking on {element}')
    
    def test_download_chart_png(self):
        """Test download chart and that it was downloaded to correct folder."""
        
        default_download_dir = os.path.join(os.path.expanduser("~"), "Downloads")
        WebDriverWait(self.executable_driver, 20).until(EC.element_to_be_clickable((By.CLASS_NAME, 'js-plotly-plot')))
        data_point = self.executable_driver.find_element(By.XPATH, '/html/body/div/div/div/div/div/div/div[2]/div/div[1]').click()
        downloaded_file = os.path.join(default_download_dir, "newplot.png")
        
        # Check if the file was downloaded.
        if os.path.exists(downloaded_file):
            print(f"[SUCCESS] File downloaded successfully to {downloaded_file}!")
        else:
            print("[ERROR]File download failed or file not found.")
        sleep(2)
    
    def stop_webapp(self):
        self.executable_driver.quit()
    

if __name__ == "__main__":
    stock_test = StockExchangeTest('/Users/zoharmurciano/desktop/chromedriver', 'http://51.21.3.43')
    stock_test.init_webapp()
    stock_test.test_stock_change_button()
    stock_test.test_chart_exists()
    stock_test.test_download_chart_png()
    stock_test.test_plot_navigation_bar()
    stock_test.stop_webapp()