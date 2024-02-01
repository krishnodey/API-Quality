import pandas as pd
import random

# Set your random seed for reproducibility
random_seed = 42
random.seed(random_seed)

# Load the CSV file into a pandas DataFrame
file_path = './Result-Database/result_database.csv'
df = pd.read_csv(file_path, header=0, encoding='ISO-8859-1')

# Select 100 random rows from the DataFrame
selected_rows = df.sample(n=91)


output_file_path = './Result-Database/validation_data.csv'
selected_rows.to_csv(output_file_path, index=False)

print(f"Selected 91 rows saved to {output_file_path} with random seed {random_seed}.")
