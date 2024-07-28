import os
import time
import pandas as pd
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

class DataScraper:
    def __init__(self):
        self.artifact_folder = os.path.join('artifact', 'data_ingestion')
        os.makedirs(self.artifact_folder, exist_ok=True)
    
    def scrape_reliance(self, query):
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')

        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        if query== 'iphone':
            url = 'https://www.reliancedigital.in/page/apple-'+query
            return url
        else:
            url = 'https://www.reliancedigital.in/search?q=' + query
            driver.get(url)

        time.sleep(10)

        model_names = []
        prices = []

        for i in range(1, 25):
            try:
                container_xpath = f'//*[@id="pl"]/div[2]/ul/li[{i}]'
                container = driver.find_element(By.XPATH, container_xpath)
                model_name_xpath = f'//*[@id="pl"]/div[2]/ul/li[{i}]/div/a/div/div[2]/p'
                model_name_tag = container.find_element(By.XPATH, model_name_xpath)
                price_xpath = f'//*[@id="pl"]/div[2]/ul/li[{i}]/div/a/div/div[2]/div[1]/div/div/span/span[2]'
                price_tag = container.find_element(By.XPATH, price_xpath)

                if model_name_tag and price_tag:
                    model_names.append(model_name_tag.text.strip())
                    prices.append(price_tag.text.strip())
            except Exception as e:
                print(f"Exception occurred while parsing container {i}: {e}")
                continue

        driver.quit()

        if not model_names or not prices:
            return None

        data = pd.DataFrame({'Model Name': model_names, 'Price': prices})
        file_path = os.path.join(self.artifact_folder, 'reliance_data.csv')
        data.to_csv(file_path, index=False)
        return data.to_dict(orient='records')

    def scrape_flipkart(self, query):
        searchString = query.replace(' ', '%20')
        url = 'https://www.flipkart.com/search?q=' + searchString

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9'
        }

        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            return None

        soup = BeautifulSoup(response.content, 'html.parser')

        model_names = []
        prices = []

        containers = soup.find_all('div', class_='cPHDOP col-12-12')

        for container in containers:
            try:
                model_name = container.find('div', class_='KzDlHZ')
                price = container.find('div', class_='Nx9bqj _4b5DiR')

                if model_name and price:
                    model_names.append(model_name.text)
                    prices.append(price.text)
            except AttributeError:
                continue

        if not model_names or not prices:
            return None

        data = pd.DataFrame({'Model Name': model_names, 'Price': prices})
        file_path = os.path.join(self.artifact_folder, 'flipkart_data.csv')
        data.to_csv(file_path, index=False)
        return data.to_dict(orient='records')
