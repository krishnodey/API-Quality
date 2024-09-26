from file_handler import FileReadWrite
from display_options import APIChoice
from api_analyzer import ApiAnalyzer
import time

def run(selected, api_type):
    
    analyzer_obj = ApiAnalyzer(api_type, selected)
    
    print("Detection of AmorphousURI:")
    analyzer_obj.detect_amorphous_uri()
    print("\nFinished Detection of AmorphousURI.\n")


    # print("Detection of NonStandardURI:")
    # analyzer_obj.detect_non_standard_uri()
    # print("\nFinished Detection of NonStandardURI:\n")



    # print("Detection of CRUDyURI:")
    # analyzer_obj.detect_crudy_uri()
    # print("\nFinished Detection of CRUDyURI:\n")


    # print("Detection of UnversionedURIs:")
    # analyzer_obj.detect_unversioned_uris()
    # print("\nFinished Detection of UnversionedURIs:\n")


    # print("Detection of PluralisedNodes:")
    # analyzer_obj.detect_pluralized_node()
    # print("\nFinished Detection of PluralisedNodes:\n")


    # print("Detection of Non-descriptive:")
    # analyzer_obj.detect_non_descriptive_uri()
    # print("\nFinished Detection of Non-descriptiveURI:\n")


    # print("Detection of NonHierarchicalNodes:")
    # analyzer_obj.detect_non_hierarchical_nodes()
    # print("\nFinished Detection of NonHierarchicalNodes:\n")

    # print("Detection of InconsistantDocumentation:")
    # analyzer_obj.detect_inconsistent_documentations()
    # print("\nFinished Detection of InconsistantDocumentation:\n")


    # print("Detection of ContextlessResource:")
    # analyzer_obj.detect_contextless()
    # print("\nFinished Detection of ContextlessResource:\n")



    # print("Detection of LessCohisiveDocumentation:")
    # analyzer_obj.detect_less_cohesive_documentation()
    # print("\nFinished Detection of LessCohisiveDocumentation:\n")

    # print("Detection of Non_FilteringEndpoint:")
    # analyzer_obj.detect_non_filtering_endpoint()
    # print("\nFinished Detection of Non_FilteringEndpoint:\n")


    print("Detection of ParameterTunneling:")
    analyzer_obj.detect_parameters_tunneling()
    print("\nFinished Detection of ParameterTunneling:\n")



    print("Detection of InconsistentResoruceArchetype:")
    analyzer_obj.detect_incosistent_resource_archetype()
    print("\nFinished Detection of InconsistentResoruceArchetype:\n")


    print("Detection of IndentifierAmbiguity:")
    analyzer_obj.detect_identifier_ambiguity()
    print("\nFinished Detection of IndentifierAmbiguity:\n")


    print("Detection of FlatEndpoint:")
    analyzer_obj.detect_flat_endpoint()
    print("\nFinished Detection of FlatEndpoint:\n")




total_time = 0
base_path = ["REST-APIs", "GraphQL-APIs"]
#base_path = ["GraphQL-APIs"]
for api in base_path:
    print(f"Detecting (Anti)Pattern for {api}")
    api_path = f"{api.strip()}/APIList.txt"
    file_obj = FileReadWrite(api_path)
    content = file_obj.read_file()
    name_list = content.split('\n')
    api_type = 'REST' if 'REST-APIs' in api else 'GraphQL'
    for api_name in name_list:
        #if api_name in ["Adobe Audience Manager","Apple App Store Connect","BroadCom","Cisco Flare"]:#, "ClearBlade","Dropbox", "Google Nest"]:#, "GroupWise", "IBM Cloud Pak System", "IBM Watson IoT"]:
        #   continue
        start_time = time.time()
        print(f"\nDetecting ----> {api_name}\n")
        path = api+"/"+api_name+"/"+api_name+".txt"
        run(api_name, api_type)
        elapsed_time = time.time() - start_time
        print(f"\nDetecting Done ----> {api_name}. Time taken: {elapsed_time:.2f} seconds\n")
        total_time += elapsed_time
        #break
    print("Total Detection Time------->",total_time/60," Minutes")


from file_handler import FileReadWrite
import json


output_file = 'All-Data\\output_data.jsonl'

base_path = ["REST-APIs", "GraphQL-APIs"]
i = 1
with open(output_file, 'w', encoding='utf-8') as outfile:
    for api in base_path:
        api_path = f"{api.strip()}/APIList.txt"
        file_obj = FileReadWrite(api_path)
        content = file_obj.read_file()
        name_list = content.split('\n')
        api_type = 'REST' if 'REST-APIs' in api else 'GraphQL'
        for api_name in name_list:
            file = f"All-Data\\temp\\{api_type}\\{api_name}.jsonl"
            #print(f"Merging ---------{file}")
            with open(file, 'r') as infile:
                for line in infile:
                    # Load the JSON object
                    line_dict = json.loads(line)
                    line_dict['id'] = i
                    json_string=json.dumps(line_dict,ensure_ascii=False)
                    outfile.write(json_string + '\n')
                    i = i + 1
            
    #print(f'Merged all files into {output_file}')



# Function to convert JSONL to CSV
def jsonl_to_csv(jsonl_file, csv_file):
    with open(jsonl_file, 'r', encoding='utf-8') as f_jsonl, open(csv_file, 'w', newline='', encoding='utf-8') as f_csv:
        csv_writer = None
        for line in f_jsonl:
            # Load each line as a JSON object
            json_obj = json.loads(line.strip())
            
            # If this is the first line, create CSV headers
            if csv_writer is None:
                headers = json_obj.keys()
                csv_writer = csv.DictWriter(f_csv, fieldnames=headers)
                csv_writer.writeheader()
            
            # Write each JSON object as a row in the CSV
            csv_writer.writerow(json_obj)
import json
import csv
jsonl_file = 'All-Data\output_data.jsonl'  # Your input JSONL file
csv_file = 'All-Data\output_data.csv'     # Your output CSV file
jsonl_to_csv(jsonl_file, csv_file)


