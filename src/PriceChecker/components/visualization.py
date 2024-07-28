# import pandas as pd
# from nltk.corpus import stopwords
# from nltk.tokenize import word_tokenize
# from collections import Counter
# import nltk
# import matplotlib.pyplot as plt
# import numpy as np

# # Download the NLTK stopwords if not already downloaded
# nltk.download('stopwords')
# nltk.download('punkt')

# # Function to preprocess model names
# def preprocess(text):
#     stop_words = set(stopwords.words('english'))
#     words = word_tokenize(text)
#     filtered_words = [word.lower() for word in words if word.isalpha() and word.lower() not in stop_words]
#     return filtered_words

# # Function to check if at least four words match
# def at_least_four_words_match(words1, words2):
#     count1 = Counter(words1)
#     count2 = Counter(words2)
#     common_words = count1 & count2
#     return sum(common_words.values()) >= 4

# # Function to compare and find matching names and their prices
# def find_matching_names_and_compare_prices(file1, file2, output_file):
#     # Read CSV files into DataFrames
#     df1 = pd.read_csv(file1)
#     df2 = pd.read_csv(file2)
    
#     matched_data = []

#     # Iterate through rows of both DataFrames
#     for idx1, row1 in df1.iterrows():
#         model_name1 = str(row1['Model Name'])  # Assuming 'Model Name' is the column name
#         price1 = row1['Price']  # Assuming 'Price' is the column name
#         preprocessed_model1 = preprocess(model_name1)
        
#         for idx2, row2 in df2.iterrows():
#             model_name2 = str(row2['Model Name'])  # Assuming 'Model Name' is the column name
#             price2 = row2['Price']  # Assuming 'Price' is the column name
#             preprocessed_model2 = preprocess(model_name2)
            
#             if at_least_four_words_match(preprocessed_model1, preprocessed_model2):
#                 matched_data.append((model_name1, price1, model_name2, price2))

#     # Create DataFrame from matched_data list
#     df_output = pd.DataFrame(matched_data, columns=['Model Name from File 1', 'Price from File 1', 'Model Name from File 2', 'Price from File 2'])

#     # Save to output file
#     df_output.to_csv(output_file, index=False)

#     return df_output

# # Function to visualize price differences
# def visualize_price_differences(df):
#     # Create a bar plot to visualize price differences
#     df['Price Difference'] = df['Price from File 1'] - df['Price from File 2']
    
#     fig, ax = plt.subplots(figsize=(10, 8))
#     index = np.arange(len(df))
#     bar_width = 0.35

#     bar1 = ax.bar(index, df['Price from File 1'], bar_width, label='Price from File 1')
#     bar2 = ax.bar(index + bar_width, df['Price from File 2'], bar_width, label='Price from File 2')

#     ax.set_xlabel('Model Names')
#     ax.set_ylabel('Prices')
#     ax.set_title('Price Comparison of Matching Models')

#     # Use full model names from File 1 for x-axis labels
#     ax.set_xticks(index + bar_width / 2)
#     ax.set_xticklabels(df['Model Name from File 2'], rotation=90)
    
#     ax.legend()

#     plt.tight_layout()
#     plt.show()

# # Example usage
# file1 = 'output11.csv'
# file2 = 'output21.csv'
# output_file = 'matched_models_with_prices.csv'
# df_matched = find_matching_names_and_compare_prices(file1, file2, output_file)
# visualize_price_differences(df_matched)

import pandas as pd
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter
import nltk
import matplotlib
matplotlib.use('Agg')  # Use the 'Agg' backend for non-interactive plotting
import matplotlib.pyplot as plt
import numpy as np
import os
from flask import Flask, request, jsonify, render_template
from src.PriceChecker.components.data_ingestion import DataScraper
import logging

# Download the NLTK stopwords if not already downloaded
nltk.download('stopwords')
nltk.download('punkt')

class ModelPriceComparer:
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))

    def preprocess(self, text):
        logging.info("doing word tokenizer on data")
        words = word_tokenize(text)
        filtered_words = [word.lower() for word in words if word.isalpha() and word.lower() not in self.stop_words]
        return filtered_words

    def at_least_four_words_match(self, words1, words2):
        count1 = Counter(words1)
        count2 = Counter(words2)
        common_words = count1 & count2
        return sum(common_words.values()) >= 4

    def find_matching_names_and_compare_prices(self, file1, file2, output_file):
        # Read CSV files into DataFrames
        df1 = pd.read_csv(file1)
        df2 = pd.read_csv(file2)
        
        matched_data = []

        
        for idx1, row1 in df1.iterrows():
            model_name1 = str(row1['Model Name'])  
            price1 = row1['Price']  
            preprocessed_model1 = self.preprocess(model_name1)
            
            for idx2, row2 in df2.iterrows():
                model_name2 = str(row2['Model Name'])  
                price2 = row2['Price']  
                preprocessed_model2 = self.preprocess(model_name2)
                
                if self.at_least_four_words_match(preprocessed_model1, preprocessed_model2):
                    matched_data.append((model_name1, price1, model_name2, price2))

        # Create DataFrame from matched_data list
        df_output = pd.DataFrame(matched_data, columns=['Reliance model', 'Reliance Price', 'Flipkart Model', 'Flipkart Price'])

        # Save to output file
        df_output.to_csv(output_file, index=False)

        return df_output

    def visualize_price_differences(self, df, image_path):
        logging.info("visulizaing the data")
        # Create a bar plot to visualize price differences
        df['Price Difference'] = df['Reliance Price'] - df['Flipkart Price']
        
        fig, ax = plt.subplots(figsize=(10, 8))
        index = np.arange(len(df))
        bar_width = 0.35

        bar1 = ax.bar(index, df['Reliance Price'], bar_width, label='Reliance Price')
        bar2 = ax.bar(index + bar_width, df['Flipkart Price'], bar_width, label='Flipkart Price')

        ax.set_xlabel('Model Names')
        ax.set_ylabel('Prices')
        ax.set_title('Price Comparison of similar Models')

        # Use full model names from File 1 for x-axis labels
        ax.set_xticks(index + bar_width / 2)
        ax.set_xticklabels(df['Flipkart Model'], rotation=90)
        
        ax.legend()

        plt.tight_layout()
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(image_path), exist_ok=True)
        plt.savefig(image_path)
        plt.close()
