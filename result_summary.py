# from file_handler import FileReadWrite
# import csv

# # Specify the file path
# base_path = ['./Outputs-REST-APIs/', './Outputs-GraphQL-APIs/']
# pattern_types = [
#     "AmorphousURI",
#     "NonStandardURI",
#     "CRUDyURI",
#     "UnversionedURIs",
#     "PluralisedNodes",
#     "NonDescriptiveURI",
#     "ContextlessResource",
#     "NonHierarchicalNodes",
#     "LessCohisiveDoc",
#     "InconsistantDoc"
# ]

# for base in base_path:
#     api_path = f"{base[10:].strip()}APIList.txt"
#     file_obj = FileReadWrite(api_path)
#     content = file_obj.read_file()
#     summary_file = "Result-Summary/"+base[10:-1].strip()+"-Summary.csv"

#     with open(summary_file, 'w', newline='') as summ_file:
#         csv_writer = csv.writer(summ_file)
#         header_line = ['api_name', 'AmorphousURI', 'TidyURI', 'NonStandardURI', 'StandarURI', 'CRUDyURI', 'VerblessURI',
#                        'UnversionedURI', 'VersionedURI', 'PluralisedNodes', 'SingularNodes', 'NonDescriptiveURI',
#                        'DescriptiveURI', 'ContextlessResource', 'ContextualResouce', 'NonHierarchicalNodes', 'HierarchicalNodes',
#                        'LessCohisiveDoc', 'CohisiveDoc', 'InconsistantDoc', 'ConsistantDoc']
#         csv_writer.writerow(header_line)

#         name_list = content.split('\n')

#         total_ap = 0
#         total_p = 0
#         for api_name in name_list:
#             data_line = [api_name]

#             for pattern in pattern_types:
#                 file_path = base + api_name + "-" + pattern + ".txt"
#                 print(f"Reading data from ----> {file_path}")

#                 # Initialize counters
#                 anti_pattern_count = 0
#                 pattern_count = 0

#                 # Read the file line by line
#                 with open(file_path, 'r', encoding='utf-8') as file:
#                     lines = file.readlines()

#                     # Iterate through each line
#                     for line in lines:
#                         # Check for Anti-Pattern line
#                         if '***Anti-Pattern***' in line:
#                             # Extract count from the next line
#                             anti_pattern_count = lines[lines.index(line) + 1].strip()
#                             anti_pattern_count = int(anti_pattern_count.split(':')[-1].strip())
#                         # Check for Patterns line
#                         elif '***Patterns***' in line:
#                             # Extract count from the next line
#                             pattern_count = lines[lines.index(line) + 1].strip()
#                             pattern_count = int(pattern_count.split(':')[-1].strip())

#                 # Print the results
#                 total_ap += anti_pattern_count
#                 total_p += pattern_count 
#                 data_line.extend([anti_pattern_count, pattern_count])
#                 print("Anti-Pattern Count:", anti_pattern_count)
#                 print("Pattern Count:", pattern_count)
#                 print(f"Done reading from ----> {file_path}\n")

#             csv_writer.writerow(data_line)
#         print(f"# of patterns {total_p}\t #of anti-patterns {total_ap}\ttotal = {total_ap+total_p}")



import json
import csv

# Input and output file names
input_file = "./All-Data/output_data.jsonl"
output_file = "./All-Data/result_summary.csv"

# Dictionary to store aggregated results
api_summary = {}


# Read the JSONL file and process each line
with open(input_file, "r", encoding="utf-8") as file:
    for line in file:
        data = json.loads(line.strip())
        # print(data)
        
        api_name = data["api_name"]
        # if data["api_type"] != "REST_APIs":
        #     continue
        api_key = f"{data['api_name']}-{data['api_type']}"
        # print(api_key)

        
        # Initialize the API entry if not already in the dictionary
        if api_key not in api_summary:
            api_summary[api_key] = {
                "amorphous": 0,
                "tidy": 0,

                "non_standard": 0,
                "standard": 0,
                
                "crudy": 0,
                "verbless": 0,
                
                "unversioned": 0,
                "versioned": 0,
                
                "pluralized": 0,
                "singularized": 0,

                "non_descriptive": 0,
                "descriptive": 0,

                "non_hierarchical": 0,
                "hierarchical": 0,

                "inconsistent": 0,
                "consistent": 0,

                "contextless": 0,
                "contextual": 0,

                "non_pertinent": 0,
                "pertinent": 0,

                "parameter_tunnel": 0,
                "parameter_ad": 0,

                "inconsistent_arc": 0,
                "consistent_arc": 0,

                "identifier_ambig": 0,
                "identifier_an": 0,

                "flat": 0,
                "structured": 0,
            
            }
        
        # Aggregate values (assuming binary values, summing works)
        api_summary[api_key]["amorphous"] += data["amorphous_uri"]
        api_summary[api_key]["tidy"] += data["tidy_uri"]

        api_summary[api_key]["non_standard"] += data["non_standard_uri"]
        api_summary[api_key]["standard"] += data["standard_uri"]

        api_summary[api_key]["crudy"] += data["crudy_uri"]
        api_summary[api_key]["verbless"] += data["verbless_uri"]   

        api_summary[api_key]["unversioned"] += data["unversioned_uri"]
        api_summary[api_key]["versioned"] += data["versioned_uri"]

        api_summary[api_key]["pluralized"] += data["pluralized_nodes"]
        api_summary[api_key]["singularized"] += data["singularized_nodes"]

        api_summary[api_key]["non_descriptive"] += data["non_descriptive_uri"]
        api_summary[api_key]["descriptive"] += data["descriptive_uri"]
        
        api_summary[api_key]["non_hierarchical"] += data["non_hierarchical_nodes"]
        api_summary[api_key]["hierarchical"] += data["hierarchical_nodes"]
        
        api_summary[api_key]["inconsistent"] += data["inconsistent_doc"]
        api_summary[api_key]["consistent"] += data["consistent_doc"]
        
        api_summary[api_key]["contextless"] += data["contextless_resource"]
        api_summary[api_key]["contextual"] += data["contextual_resouce"]
        
        api_summary[api_key]["non_pertinent"] += data["less_cohesive_doc"]
        api_summary[api_key]["pertinent"] += data["cohesive_doc"]
        
        api_summary[api_key]["parameter_tunnel"] += data["parameter_tunneling"]
        api_summary[api_key]["parameter_ad"] += data["parameter_adherence"]

        api_summary[api_key]["inconsistent_arc"] += data["inconsistent_archetype"]
        api_summary[api_key]["consistent_arc"] += data["consistent_archetype"]

        api_summary[api_key]["identifier_ambig"] += data["identifier_ambiguity"]
        api_summary[api_key]["identifier_an"] += data["identifier_annotation"]

        api_summary[api_key]["flat"] += data["flat_endpoint"]
        api_summary[api_key]["structured"] += data["structured_endpoint"]
#print(api_summary)


# Write results to CSV
with open(output_file, "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    header = ["API Name", "Amorphous Endpoint", "Tidy Endpoint", "Contextless Resource",  "Contextual Resource", "CRUDy Endpoint", "Verbless Endpoint",
    "Inconsistent Documentation", "Consistent Documentation", "NonDescriptive Endpoint", "Descriptive Endpoint", "NonHierarchical Nodes", "Hierarchical Nodes", 
    "NonPertinent Documentation", "Pertinent Documentation", "NonStandard Endpoint", "Standard Endpoint", "Pluralized Nodes", "Singularized Nodes",
    "Unversioned Endpoint", "Versioned Endpoint", "Parameter Tunneling", "Parameter Adherence", "Inconsistent Archetype", "Consistent Archetype", "Identifier Ambiguity", "Identifier Annotation", "Flat Endpoint", "Structured Endpoint"]
    # Write header
    writer.writerow(header)
    
    # Write API data
    for api_name, values in api_summary.items():
        # print(api_name.split("-")[0].strip())
        row = [api_name.split("-")[0].strip(), values["amorphous"], values["tidy"], values["contextless"], values["contextual"], values["crudy"], values["verbless"], 
               values["inconsistent"], values["consistent"], values["non_descriptive"], values["descriptive"], values["non_hierarchical"], values["hierarchical"] , 
               values["non_pertinent"], values["pertinent"], values["non_standard"], values["standard"], values["pluralized"], values["singularized"], 
               values["unversioned"], values["versioned"], values["parameter_tunnel"], values["parameter_ad"], values["inconsistent_arc"], values["consistent_arc"], 
               values["identifier_ambig"], values["identifier_an"], values["flat"], values["structured"]]
        writer.writerow(row)

print(f"CSV file '{output_file}' created successfully.")

