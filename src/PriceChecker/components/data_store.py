# import pymysql
# from src.PriceChecker.constant.database import *

# # Database configuration
# db_config = {
#     'host': HOST,
#     'user': USER,
#     'password': PASSWORD,
#     'database': DATABASE_NAME,
#     'port': PORT  # Default MySQL port
# }

# # Dictionary of CSV files and their corresponding table names
# csv_to_table = {
#     'output11.csv': 'reliance_data',
#     'output21.csv': 'flipkart_data'
# }

# # Connect to the database
# try:
#     connection = pymysql.connect(
#         host=db_config['host'],
#         user=db_config['user'],
#         password=db_config['password'],
#         database=db_config['database'],
#         port=db_config['port'],
#         local_infile=True  # Enable local infile option
#     )
#     cursor = connection.cursor()
#     print("Connection to the database was successful.")

#     for csv_file_path, table_name in csv_to_table.items():
#         # Create table if it doesn't exist
#         create_table_sql = f"""
#         CREATE TABLE IF NOT EXISTS {table_name} (
#             model_name VARCHAR(255),
#             price VARCHAR(255)
#         );
#         """
#         cursor.execute(create_table_sql)
#         connection.commit()
#         print(f"Table {table_name} created or already exists.")

#         # Load data from CSV file into the table
#         load_data_sql = f"""
#         LOAD DATA LOCAL INFILE '{csv_file_path}'
#         INTO TABLE {table_name}
#         FIELDS TERMINATED BY ','
#         LINES TERMINATED BY '\\n'
#         IGNORE 1 LINES
#         (model_name, price);
#         """
#         try:
#             cursor.execute(load_data_sql)
#             connection.commit()
#             print(f"Data from {csv_file_path} has been successfully inserted into {table_name}.")
#         except Exception as e:
#             print(f"Error loading data from {csv_file_path} into {table_name}: {e}")

# except Exception as e:
#     print(f"Error: {e}")

# finally:
#     cursor.close()
#     connection.close()
#     print("Database connection closed.")
import logging
import pymysql
from src.PriceChecker.constant.database import db_config

class CSVToDatabaseLoader:
    def __init__(self, db_config, csv_to_table):
        self.db_config = db_config
        self.csv_to_table = csv_to_table

    def connect_to_database(self):
        try:
            logging.info("connected to database")
            self.connection = pymysql.connect(
                host=self.db_config['HOST'],
                user=self.db_config['USER'],
                password=self.db_config['PASSWORD'],
                database=self.db_config['DATABASE_NAME'],
                port=self.db_config['PORT'],
                local_infile=True  # Enable local infile option
            )
            self.cursor = self.connection.cursor()
            print("Connection to the database was successful.")
        except Exception as e:
            print(f"Error: {e}")
            raise

    # def create_table(self, table_name):
    #     create_table_sql = f"""
    #     CREATE TABLE IF NOT EXISTS {table_name} (
    #         Model_name VARCHAR(255),
    #         Price VARCHAR(255)
    #     );
    #     """
    #     try:
    #         self.cursor.execute(create_table_sql)
    #         self.connection.commit()
    #         print(f"Table {table_name} created or already exists.")
    #     except Exception as e:
    #         print(f"Error creating table {table_name}: {e}")
    #         raise

    def load_data_from_csv(self, csv_file_path, table_name):
        logging.info("Loading the data to the database")
        load_data_sql = f"""
        LOAD DATA LOCAL INFILE '{csv_file_path}'
        INTO TABLE {table_name}
        FIELDS TERMINATED BY ','
        LINES TERMINATED BY '\\n'
        IGNORE 1 LINES
        (model_name, price);
        """
        try:
            self.cursor.execute(load_data_sql)
            self.connection.commit()
            print(f"Data from {csv_file_path} has been successfully inserted into {table_name}.")
        except Exception as e:
            print(f"Error loading data from {csv_file_path} into {table_name}: {e}")
            raise

    def close_connection(self):
        self.cursor.close()
        self.connection.close()
        print("Database connection closed.")

    def run(self):
        self.connect_to_database()
        try:
            for csv_file_path, table_name in self.csv_to_table.items():
                # self.create_table(table_name)
                self.load_data_from_csv(csv_file_path, table_name)
        finally:
            self.close_connection()
