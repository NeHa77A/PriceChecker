# from flask import Flask, request, jsonify, render_template
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.options import Options
# import pandas as pd
# from webdriver_manager.chrome import ChromeDriverManager
# import time
# import requests
# from bs4 import BeautifulSoup

# app = Flask(__name__, template_folder='E:\\assignment\\templates')

# @app.route('/')
# def index():
#     return render_template("index.html")

# @app.route('/scrape', methods=['POST'])
# def scrape():
#     query = request.form.get('query')
    
#     if not query:
#         return jsonify({'error': 'Query parameter missing'}), 400

#     # Scrape data from both Reliance Digital and Flipkart
#     reliance_data = scrape_reliance(query) or []
#     flipkart_data = scrape_flipkart(query) or []

#     if not reliance_data and not flipkart_data:
#         return jsonify({'error': 'No data extracted from both sources.'}), 500

#     # Combine results from both sources
#     combined_data = {
#         'Reliance Digital': reliance_data,
#         'Flipkart': flipkart_data
#     }

#     return render_template("results.html", data=combined_data)


# def scrape_reliance(query):
#     options = Options()
#     options.add_argument('--headless')
#     options.add_argument('--no-sandbox')
#     options.add_argument('--disable-dev-shm-usage')

#     driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
#     url = 'https://www.reliancedigital.in/search?q=' + query
#     driver.get(url)

#     time.sleep(10)

#     model_names = []
#     prices = []

#     for i in range(1, 25):
#         try:
#             container_xpath = f'//*[@id="pl"]/div[2]/ul/li[{i}]'
#             container = driver.find_element(By.XPATH, container_xpath)
#             model_name_xpath = f'//*[@id="pl"]/div[2]/ul/li[{i}]/div/a/div/div[2]/p'
#             model_name_tag = container.find_element(By.XPATH, model_name_xpath)
#             price_xpath = f'//*[@id="pl"]/div[2]/ul/li[{i}]/div/a/div/div[2]/div[1]/div/div/span/span[2]'
#             price_tag = container.find_element(By.XPATH, price_xpath)

#             if model_name_tag and price_tag:
#                 model_names.append(model_name_tag.text.strip())
#                 prices.append(price_tag.text.strip())
#         except Exception as e:
#             print(f"Exception occurred while parsing container {i}: {e}")
#             continue

#     driver.quit()

#     if not model_names or not prices:
#         return None

#     data = pd.DataFrame({'Model Name': model_names, 'Price': prices})
#     data.to_csv('reliance_data.csv', index=False)
#     return data.to_dict(orient='records')

# def scrape_flipkart(query):
#     searchString = query.replace(' ', '%20')
#     url = 'https://www.flipkart.com/search?q=' + searchString

#     headers = {
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
#         'Accept-Language': 'en-US,en;q=0.9'
#     }

#     response = requests.get(url, headers=headers)

#     if response.status_code != 200:
#         return None

#     soup = BeautifulSoup(response.content, 'html.parser')

#     model_names = []
#     prices = []

#     containers = soup.find_all('div', class_='cPHDOP col-12-12')

#     for container in containers:
#         try:
#             model_name = container.find('div', class_='KzDlHZ')
#             price = container.find('div', class_='Nx9bqj _4b5DiR')

#             if model_name and price:
#                 model_names.append(model_name.text)
#                 prices.append(price.text)
#         except AttributeError:
#             continue

#     if not model_names or not prices:
#         return None

#     data = pd.DataFrame({'Model Name': model_names, 'Price': prices})
#     data.to_csv('flipkart_data.csv', index=False)
#     return data.to_dict(orient='records')

# if __name__ == '__main__':
#     app.run(debug=True)

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
import logging

class DataScraper:
    def __init__(self):
        self.artifact_folder = os.path.join('artifact', 'data_ingestion')
        os.makedirs(self.artifact_folder, exist_ok=True)
    
    def scrape_reliance(self, query):
        logging.info("Performing scraping from reliance website")
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')

        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        if query== 'iphones':
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
                logging.info("completed scraping from reliance website")
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
        logging.info("Performing scraping from flipkart website")
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
        logging.info("completed scraping from flipkart website")
        file_path = os.path.join(self.artifact_folder, 'flipkart_data.csv')
        data.to_csv(file_path, index=False)
        return data.to_dict(orient='records')
