import json
import random

# Set your random seed for reproducibility
random_seed = 42
random.seed(random_seed)

# Load the JSONL file and read all lines
file_path = './All-Data/output_data.jsonl'
with open(file_path, 'r', encoding='utf-8') as infile:
    lines = infile.readlines()

# Select 91 random lines
selected_lines = random.sample(lines, 91)

# Save the selected lines to a new JSONL file
output_file_path = './Journal-Resources/Validation-Survey/validation_data.jsonl'
with open(output_file_path, 'w', encoding='utf-8') as outfile:
    outfile.writelines(selected_lines)

print(f"Selected 91 lines saved to {output_file_path} with random seed {random_seed}.")

