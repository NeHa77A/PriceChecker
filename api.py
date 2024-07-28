from flask import Flask, request, jsonify, render_template
import pandas as pd
import os
from src.PriceChecker.components.data_ingestion import DataScraper
from src.PriceChecker.components.data_validation import CSVProcessor
from src.PriceChecker.components.data_store import CSVToDatabaseLoader
from src.PriceChecker.constant.database import db_config
from src.PriceChecker.components.visualization import ModelPriceComparer
from src.PriceChecker.constant.path_contant import *

app = Flask(__name__, template_folder=TEMPLATE_FOLDER, static_folder=STATIC_FOLDER)

def create_directories():
    ingestion_dir = INGESTION_DIR
    validation_dir = VALIDATION_DIR
    static_dir = STATIC_FOLDER
    os.makedirs(ingestion_dir, exist_ok=True)
    os.makedirs(validation_dir, exist_ok=True)
    os.makedirs(static_dir, exist_ok=True)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/scrape', methods=['POST'])
def scrape():
    query = request.form.get('query')
    
    if not query:
        return jsonify({'error': 'Query parameter missing'}), 400
    
    datainge = DataScraper()

    # Scrape data from both Reliance Digital and Flipkart
    reliance_data = datainge.scrape_reliance(query) or []
    flipkart_data = datainge.scrape_flipkart(query) or []

    if not reliance_data and not flipkart_data:
        return jsonify({'error': 'No data extracted from both sources.'}), 500

    # Ensure the data is in the correct format
    if not isinstance(reliance_data, list) or not all(isinstance(i, (list, dict)) for i in reliance_data):
        return jsonify({'error': 'Invalid format for Reliance data'}), 500
    if not isinstance(flipkart_data, list) or not all(isinstance(i, (list, dict)) for i in flipkart_data):
        return jsonify({'error': 'Invalid format for Flipkart data'}), 500

    # Create necessary directories
    create_directories()

    # Save the raw scraped data to CSV files
    reliance_df = pd.DataFrame(reliance_data, columns=['Model Name', 'Price'])
    flipkart_df = pd.DataFrame(flipkart_data, columns=['Model Name', 'Price'])
    
    reliance_raw_path = RELIANCE_RAW_PATH
    flipkart_raw_path = FLIPKART_ROW_PATH
    
    reliance_df.to_csv(reliance_raw_path, index=False)
    flipkart_df.to_csv(flipkart_raw_path, index=False)

    # Clean the data
    reliance_processor = CSVProcessor(reliance_raw_path, VAL_RELIANCE_DATA)
    reliance_processor.clean_csv()

    flipkart_processor = CSVProcessor(flipkart_raw_path, VAL_FLIPKART_DATA)
    flipkart_processor.clean_csv()

    # Load cleaned data to the database
    csv_to_table = {
        VAL_RELIANCE_DATA: 'reliance_data',
        VAL_FLIPKART_DATA: 'flipkart_data'
    }

    loader = CSVToDatabaseLoader(db_config, csv_to_table)
    loader.run()

    # Perform model price comparison
    comparer = ModelPriceComparer()
    output_file = MATCH_DATA
    df_matched = comparer.find_matching_names_and_compare_prices(
        VAL_RELIANCE_DATA,
        VAL_FLIPKART_DATA,
        output_file
    )

    # Visualize the price differences and save the plot as an image
    img_path = IMAGE_PATH
    comparer.visualize_price_differences(df_matched, img_path)

    return render_template("results.html", data=df_matched.to_dict(orient='records'), img_path=IMAGE)
