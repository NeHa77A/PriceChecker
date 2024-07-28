## Problem Statement
By using python, you need to scrap the data from two e-
commerce website &amp; compare the price of product, which
seems similar.
The compared result should be visualized in any visualization
tool.
Tabulate same data in two different tables, use any database.

### Solution
In this project, we are involved in scraping mobile phone prices from Reliance Digital and Flipkart, cleaning the data, storing it in a MySQL database, and comparing prices between the two sources. The results are visualized and displayed on a web interface using Flask.

```
project/
├── src/
│   ├── PriceChecker/
│   │   ├── components/
│   │   │   ├── __init__.py
│   │   │   ├── data_ingestion.py
│   │   │   ├── data_validation.py
│   │   │   ├── data_store.py
│   │   │   └── visualization.py
│   │   └── constant/
│   │       ├── __init__.py
│   │       └── database.py
├── artifact/
│   ├── data_ingestion/
│   │   ├── reliance_data.csv
│   │   └── flipkart_data.csv
│   └── data_validation/
│       ├── reliance_data.csv
│       ├── flipkart_data.csv
│       └── matched_models_with_prices.csv
├── api.py
└── main.py
|── templates/
│       ├── index.html
│       └── results.html
└── static/
        └── price_comparison.png
```
## Architecture
![](https://raw.githubusercontent.com/NeHa77A/PriceChecker/main/architecture.png)

## Run the Project
### Step 1-: Clone the Repository
```bash
git clone https://github.com/NeHa77A/PriceChecker.git
```

### Step 2-: Create conda environment
```bash
conda create -p ./venv python=3.10 -y
```

### Step 3-: Activate Conda environment
```bash
conda activate venv/
```

### Step 4-: Install requirements
```bash
pip install -r requirements.txt
```

### Step 5-: Install requirements
```bash
python main.py
```
Access the Web Interface:

Open your browser and go to http://127.0.0.1:5000/.

Submit Query:

Enter a query for the mobile phone model and submit the form to scrape, compare, and visualize the data.

![](https://raw.githubusercontent.com/NeHa77A/PriceChecker/main/output.png)

![](https://raw.githubusercontent.com/NeHa77A/PriceChecker/main/output/visulization.png)
