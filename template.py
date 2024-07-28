import os
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format="[%(asctime)s]: %(message)s ")

package_name = "PriceChecker"

list_of_files =[
    ".github/workflows/.gitkeep",
    f"src/{package_name}/__init__.py",
    f"src/{package_name}/components/__init__.py",
    f"src/{package_name}/utils/__init__.py",
    f"src/{package_name}/constant/__init__.py",
    "requirements.txt",
    "api.py"
    "setup.py",
    "main.py",
    "research/trials.ipynb"
]

for filepath in list_of_files:
    filepath =Path(filepath)
    filedir, filename = os.path.split(filepath)
    if filedir != "":
        os.makedirs(filedir,exist_ok=True)
        logging.info(f"Crete directory: {filedir} for file: {filename}")

    if (not os.path.exists(filepath) or (os.path.getsize(filepath) ==0)):
        with open(filepath,"w") as f:
            pass  # empty file
            logging.info(f"Creating empty file : {filepath}")

    else:
        logging.info(f"{filename} already exist")
