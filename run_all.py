from file_handler import FileReadWrite
from display_options import APIChoice
from api_analyzer import ApiAnalyzer
import time

def run(selected, uri_path, base_path):
    
    uri_obj = FileReadWrite(uri_path)
    data = uri_obj.read_data()

    uri = []
    des = []
    for line in data:
        line  = line.split(">>")
        uri.append(line[1])

    #print(uri)

    analyzer_obj = ApiAnalyzer(uri)
    #analyzer_obj.detect_amorphous_uri()

    print("Detection of AmorphousURI:")
    result_AP, result_P, p_count, ap_count = analyzer_obj.detect_amorphous_uri()
    # Create the data string to write in the file]
    pattern_type = "Amorphous"
    uri_obj.write_data(result_AP, result_P, p_count, ap_count, selected, pattern_type, base_path)
    print("Finished Detection of AmorphousURI.\n")


    print("Detection of NonStandardURI:")
    result_AP, result_P, p_count, ap_count = analyzer_obj.detect_non_standard_uri()
    pattern_type = "Non Standard URI"
    uri_obj.write_data(result_AP, result_P, p_count, ap_count, selected, pattern_type, base_path)
    print("Finished Detection of NonStandardURI:\n")


    '''print("Detection of CRUDyURI:")
    result_AP, result_P, p_count, ap_count = analyzer_obj.detect_crudy_uri()
    pattern_type = "CRUDyURI"
    uri_obj.write_data(result_AP, result_P, p_count, ap_count, selected, pattern_type, base_path)
    print("Finished Detection of CRUDyURI:\n")



    print("Detection of UnversionedURIs:")
    result_AP, result_P, p_count, ap_count = analyzer_obj.detect_unversioned_uris()
    pattern_type = "UnversionedURIs"
    uri_obj.write_data(result_AP, result_P, p_count, ap_count, selected, pattern_type, base_path)
    print("Finished Detection of UnversionedURIs:\n")



    print("Detection of PluralisedNodes:")
    result_AP, result_P, p_count, ap_count = analyzer_obj.detect_pluralized_node(data)
    pattern_type = "PluralisedNodes"
    uri_obj.write_data(result_AP, result_P, p_count, ap_count, selected, pattern_type, base_path)
    print("Finished Detection of PluralisedNodes:\n")


    print("Detection of Non-descriptiveURI:")
    result_AP, result_P, p_count, ap_count = analyzer_obj.detect_non_descriptive_uri()
    pattern_type = "Non-descriptiveURI"
    uri_obj.write_data(result_AP, result_P, p_count, ap_count, selected, pattern_type, base_path)
    print("Finished Detection of Non-descriptiveURI:\n")


    
    print("Detection of ContextlessURI:")
    result_AP, result_P, p_count, ap_count = analyzer_obj.detect_contextless(data)
    pattern_type = "ContextlessURI"
    uri_obj.write_data(result_AP, result_P, p_count, ap_count, selected, pattern_type,base_path)
    print("Finished Detection of ContextlessURI:\n")



    print("Detection of NonHierarchicalNodes:")
    result_AP, result_P, p_count, ap_count = analyzer_obj.detect_non_hierarchical_nodes()
    pattern_type = "NonHierarchicalNodes"
    uri_obj.write_data(result_AP, result_P, p_count, ap_count, selected, pattern_type, base_path)
    print("Finished Detection of NonHierarchicalNodes:\n")


    print("Detection of LessCohisiveDocumentation:")
    result_AP, result_P, p_count, ap_count = analyzer_obj.detect_less_cohesive_documentation(data)
    pattern_type = "LessCohisiveDoc"
    uri_obj.write_data(result_AP, result_P, p_count, ap_count, selected, pattern_type,base_path)
    print("Finished Detection of LessCohisiveDocumentation:\n")


    print("Detection of InconsistantDocumentation:")
    result_AP, result_P, p_count, ap_count = analyzer_obj.detect_inconsistent_documentations(data)
    pattern_type = "InconsistantDoc"
    uri_obj.write_data(result_AP, result_P, p_count, ap_count, selected, pattern_type,base_path)
    print("Finished Detection of InconsistantDocumentation:\n")'''



total_time = 0
base_path = ["REST-APIs", "GraphQL-APIs"]
#base_path = ["GraphQL-APIs"]
for api in base_path:
    print(f"Detecting (Anti)Pattern for {api}")
    api_path = f"{api.strip()}/APIList.txt"
    file_obj = FileReadWrite(api_path)
    content = file_obj.read_file()
    name_list = content.split('\n')
    for api_name in name_list:
        #if api_name in ["Adobe Audience Manager","Apple App Store Connect","BroadCom","Cisco Flare", "ClearBlade","Dropbox", "Google Nest", "GroupWise", "IBM Cloud Pak System", "IBM Watson IoT"]:
            #continue
        start_time = time.time()
        print(f"\nDetecting ----> {api_name}\n")
        path = api+"/"+api_name+"/"+api_name+".txt"
        run(api_name, path, api)
        elapsed_time = time.time() - start_time
        print(f"\nDetecting Done ----> {api_name}. Time taken: {elapsed_time:.2f} seconds\n")
        total_time += elapsed_time
        #break
    print("Total Detection Time------->",total_time/60,"Minutes")

