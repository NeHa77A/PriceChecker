# import csv
# import re

# def clean_csv(input_file, output_file):
#     with open(input_file, mode='r', newline='', encoding='utf-8') as infile, \
#          open(output_file, mode='w', newline='', encoding='utf-8') as outfile:
#         reader = csv.reader(infile)
#         writer = csv.writer(outfile)
        
#         # Read and write the header as is
#         header = next(reader)
#         writer.writerow(header)
        
#         for row in reader:
#             # Clean the product details column by removing commas and parentheses within quotes
#             product_details = row[0].replace(',', '').replace('(', '').replace(')', '')
            
#             # Clean the price column by removing commas and keeping only the integer part
#             price = re.sub(r'[^\d]', '', row[1].split('.')[0])
            
#             writer.writerow([product_details, price])

# # Input and output file paths
# input_file = 'reliance_selenium.csv'
# output_file = 'output11.csv'

# clean_csv(input_file, output_file)

# input_file = 'flipkart_mobiles1.csv'
# output_file = 'output21.csv'

# # Clean the CSV file
# clean_csv(input_file, output_file)

import logging
import csv
import re

class CSVProcessor:
    def __init__(self, input_file, output_file):
        self.input_file = input_file
        self.output_file = output_file

    def clean_csv(self):
        logging.info("Cleaning the data")
        with open(self.input_file, mode='r', newline='', encoding='utf-8') as infile, \
             open(self.output_file, mode='w', newline='', encoding='utf-8') as outfile:
            reader = csv.reader(infile)
            writer = csv.writer(outfile)
            
            # Read and write the header as is
            header = next(reader)
            writer.writerow(header)
            
            for row in reader:
                # Clean the product details column by removing commas and parentheses within quotes
                product_details = row[0].replace(',', '').replace('(', '').replace(')', '')
                
                # Clean the price column by removing commas and keeping only the integer part
                price = re.sub(r'[^\d]', '', row[1].split('.')[0])
                
                writer.writerow([product_details, price])

# # Example usage
# if __name__ == "__main__":
#     reliance_processor = CSVProcessor('artifact/data_ingestion/reliance_data.csv', 'artifact/data_validation/reliance_data.csv')
#     reliance_processor.clean_csv()

#     flipkart_processor = CSVProcessor('artifact/data_validation/flipkart_data.csv', 'artifact/data_validation/flipkart_data.csv')
#     flipkart_processor.clean_csv()

