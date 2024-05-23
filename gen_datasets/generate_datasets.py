import pandas as pd
import numpy as np
from faker import Faker
import os

# Initialize Faker to generate lorem ipsum data
fake = Faker()

# Function to generate a column of lorem ipsum sentences
def generate_lorem_ipsum_data(num_rows, num_sentences=1):
    return [fake.text(max_nb_chars=200) for _ in range(num_rows)]

# Define the number of datasets, rows, and columns
num_datasets = 10
num_rows = 100000  # Adjust the number of rows per dataset as needed
num_columns = 5    # Adjust the number of columns per dataset as needed

# Define the output folder
output_folder = "./All_Datasets"

# Create the output folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Create datasets
for i in range(1, num_datasets + 1):
    # Create a DataFrame with lorem ipsum data
    data = {f'col_{j+1}': generate_lorem_ipsum_data(num_rows) for j in range(num_columns)}
    df = pd.DataFrame(data)
    
    # Save to CSV in the output folder
    df.to_csv(os.path.join(output_folder, f'dataset_{i}.csv'), index=False)
    print(f"Dataset {i} created successfully.")

print("** Datasets with lorem ipsum created successfully. **")