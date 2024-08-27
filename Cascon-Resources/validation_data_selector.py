# import pandas as pd
# import random

# # Set your random seed for reproducibility
# random_seed = 42
# random.seed(random_seed)

# # Load the CSV file into a pandas DataFrame
# file_path = './Result-Database/result_database.csv'
# df = pd.read_csv(file_path, header=0, encoding='ISO-8859-1')

# # Select 100 random rows from the DataFrame
# selected_rows = df.sample(n=91)


# output_file_path = './Result-Database/validation_data.csv'
# selected_rows.to_csv(output_file_path, index=False)

# print(f"Selected 91 rows saved to {output_file_path} with random seed {random_seed}.")


# import pandas as pd
# import random
# import json

# # Set your random seed for reproducibility
# random_seed = 42
# random.seed(random_seed)

# # Load the JSONL file into a pandas DataFrame
# file_path = 'All-Data/outout_data.jsonl'
# df = pd.read_json(file_path, lines=True, encoding='utf-8')

# # Select 91 random rows from the DataFrame
# selected_rows = df.sample(n=91, random_state=random_seed)

# # Save the selected rows to a new JSONL file
# output_file_path = './Journal_Resources/Validation-Survey/validation_data.jsonl'
# print(output_file_path)
# selected_rows.to_json(output_file_path, orient='records', lines=True, force_ascii=False)

# print(f"Selected 91 rows saved to {output_file_path} with random seed {random_seed}.")
