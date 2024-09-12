from file_handler import FileReadWrite
from display_options import APIChoice
from api_analyzer import ApiAnalyzer
import time

def run(selected, uri_path, base_path, api_type):
    
    uri_obj = FileReadWrite(uri_path)
    analyzer_obj = ApiAnalyzer(api_type, selected)
    
    print("Detection of AmorphousURI:")
    result_AP, result_P, p_count, ap_count = analyzer_obj.detect_amorphous_uri()
    pattern_type = "AmorphousURI"
    uri_obj.write_data(result_AP, result_P, p_count, ap_count, selected, pattern_type, base_path)
    print("\nFinished Detection of AmorphousURI.\n")


    # print("Detection of NonStandardURI:")
    # result_AP, result_P, p_count, ap_count = analyzer_obj.detect_non_standard_uri()
    # pattern_type = "NonStandardURI"
    # uri_obj.write_data(result_AP, result_P, p_count, ap_count, selected, pattern_type, base_path)
    # print("\nFinished Detection of NonStandardURI:\n")



    # print("Detection of CRUDyURI:")
    # result_AP, result_P, p_count, ap_count = analyzer_obj.detect_crudy_uri()
    # pattern_type = "CRUDyURI"
    # uri_obj.write_data(result_AP, result_P, p_count, ap_count, selected, pattern_type, base_path)
    # print("\nFinished Detection of CRUDyURI:\n")


    # print("Detection of UnversionedURIs:")
    # result_AP, result_P, p_count, ap_count = analyzer_obj.detect_unversioned_uris()
    # pattern_type = "UnversionedURIs"
    # uri_obj.write_data(result_AP, result_P, p_count, ap_count, selected, pattern_type, base_path)
    # print("\nFinished Detection of UnversionedURIs:\n")


    # print("Detection of PluralisedNodes:")
    # result_AP, result_P, p_count, ap_count = analyzer_obj.detect_pluralized_node()
    # pattern_type = "PluralisedNodes"
    # uri_obj.write_data(result_AP, result_P, p_count, ap_count, selected, pattern_type, base_path)
    # print("\nFinished Detection of PluralisedNodes:\n")


    # print("Detection of Non-descriptive:")
    # result_AP, result_P, p_count, ap_count= analyzer_obj.detect_non_descriptive_uri()
    # pattern_type = "NonDescriptiveURI"
    # uri_obj.write_data(result_AP, result_P, p_count, ap_count, selected, pattern_type, base_path)
    # print("\nFinished Detection of Non-descriptiveURI:\n")


    # print("Detection of NonHierarchicalNodes:")
    # result_AP, result_P, p_count, ap_count = analyzer_obj.detect_non_hierarchical_nodes()
    # pattern_type = "NonHierarchicalNodes"
    # uri_obj.write_data(result_AP, result_P, p_count, ap_count, selected, pattern_type, base_path)
    # print("\nFinished Detection of NonHierarchicalNodes:\n")

    # print("Detection of InconsistantDocumentation:")
    # result_AP, result_P, p_count, ap_count = analyzer_obj.detect_inconsistent_documentations()
    # pattern_type = "InconsistantDoc"
    # uri_obj.write_data(result_AP, result_P, p_count, ap_count, selected, pattern_type, base_path)
    # print("\nFinished Detection of InconsistantDocumentation:\n")


    # print("Detection of ContextlessResource:")
    # result_AP, result_P, p_count, ap_count= analyzer_obj.detect_contextless()
    # pattern_type = "ContextlessResource"
    # uri_obj.write_data(result_AP, result_P, p_count, ap_count, selected, pattern_type, base_path)
    # print("\nFinished Detection of ContextlessResource:\n")



    # print("Detection of LessCohisiveDocumentation:")
    # result_AP, result_P, p_count, ap_count= analyzer_obj.detect_less_cohesive_documentation()
    # pattern_type = "LessCohisiveDoc"
    # uri_obj.write_data(result_AP, result_P, p_count, ap_count, selected, pattern_type, base_path)
    # print("\nFinished Detection of LessCohisiveDocumentation:\n")

    print("Detection of Non_FilteringEndpoint:")
    result_AP, result_P, p_count, ap_count= analyzer_obj.detect_non_filtering_endpoint()
    pattern_type = "Non-Filtering-Endpoint"
    uri_obj.write_data(result_AP, result_P, p_count, ap_count, selected, pattern_type, base_path)
    print("\nFinished Detection of Non_FilteringEndpoint:\n")


    print("Detection of ParameterTunneling:")
    result_AP, result_P, p_count, ap_count= analyzer_obj.detect_parameters_tunneling()
    pattern_type = "ParameterTunneling"
    uri_obj.write_data(result_AP, result_P, p_count, ap_count, selected, pattern_type, base_path)
    print("\nFinished Detection of ParameterTunneling:\n")



    print("Detection of InconsistentResoruceArchetype:")
    result_AP, result_P, p_count, ap_count= analyzer_obj.detect_incosistent_resource_archetype()
    pattern_type = "Incosistent_Archetypes"
    uri_obj.write_data(result_AP, result_P, p_count, ap_count, selected, pattern_type, base_path)
    print("\nFinished Detection of InconsistentResoruceArchetype:\n")


    print("Detection of IndentifierAmbiguity:")
    result_AP, result_P, p_count, ap_count= analyzer_obj.detect_identifier_ambiguity()
    pattern_type = "IndentifierAmbiguity"
    uri_obj.write_data(result_AP, result_P, p_count, ap_count, selected, pattern_type, base_path)
    print("\nFinished Detection of IndentifierAmbiguity:\n")


    print("Detection of FlatEndpoint:")
    result_AP, result_P, p_count, ap_count= analyzer_obj.detect_flat_endpoint()
    pattern_type = "FlatEndpoint"
    uri_obj.write_data(result_AP, result_P, p_count, ap_count, selected, pattern_type, base_path)
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
        run(api_name, path, api, api_type)
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


