from file_handler import FileReadWrite
import csv

# Specify the file path
base_path = ['./Outputs-REST-APIs/', './Outputs-GraphQL-APIs/']
pattern_types = [
    "Amorphous",
    "Non Standard URI",
    "CRUDyURI",
    "UnversionedURIs",
    "PluralisedNodes",
    "Non-descriptiveURI",
    "ContextlessURI",
    "NonHierarchicalNodes",
    "LessCohisiveDoc",
    "InconsistantDoc"
]

for base in base_path:
    api_path = f"{base[10:].strip()}APIList.txt"
    file_obj = FileReadWrite(api_path)
    content = file_obj.read_file()
    summary_file = "Result-Summary/"+base[10:-1].strip()+"-Summary.csv"

    with open(summary_file, 'w', newline='') as summ_file:
        csv_writer = csv.writer(summ_file)
        header_line = ['api_name', 'AmorphousURI', 'TidyURI', 'NonStandardURI', 'StandarURI', 'CRUDyURI', 'Verbless',
                       'UnversionedURI', 'VersionedURI', 'PluralisedNodes', 'SingularNodes', 'Non-descriptiveURI',
                       'DescriptiveURI', 'ContextlessURI', 'Contextual', 'NonHierarchicalNodes', 'HierarchicalNodes',
                       'LessCohisiveDoc', 'CohisiveDoc', 'InconsistantDoc', 'Consistant']
        csv_writer.writerow(header_line)

        name_list = content.split('\n')
        for api_name in name_list:
            data_line = [api_name]

            for pattern in pattern_types:
                file_path = base + api_name + "-" + pattern + ".txt"
                print(f"Reading data from ----> {file_path}")

                # Initialize counters
                anti_pattern_count = 0
                pattern_count = 0

                # Read the file line by line
                with open(file_path, 'r') as file:
                    lines = file.readlines()

                    # Iterate through each line
                    for line in lines:
                        # Check for Anti-Pattern line
                        if '***Anti-Pattern***' in line:
                            # Extract count from the next line
                            anti_pattern_count = lines[lines.index(line) + 1].strip()
                            anti_pattern_count = int(anti_pattern_count.split(':')[-1].strip())
                        # Check for Patterns line
                        elif '***Patterns***' in line:
                            # Extract count from the next line
                            pattern_count = lines[lines.index(line) + 1].strip()
                            pattern_count = int(pattern_count.split(':')[-1].strip())

                # Print the results
                data_line.extend([anti_pattern_count, pattern_count])
                print("Anti-Pattern Count:", anti_pattern_count)
                print("Pattern Count:", pattern_count)
                print(f"Done reading from ----> {file_path}\n")

            csv_writer.writerow(data_line)
