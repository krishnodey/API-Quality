from file_handler import FileReadWrite
from display_options import APIChoice
from api_analyzer import ApiAnalyzer


base_path = "APIs/"


apilist_path = base_path + 'APIList.txt'  # Replace with your CSV file path
api_obj = APIChoice(apilist_path)
#api_choice.display_choices()
api_obj.select_choice()
selected = api_obj.get_selected_choice()
print(f"Your selected choice is: {selected}")


uri_path = base_path+selected+"/APITest.txt"
uri_obj = FileReadWrite(uri_path)
uri_content = uri_obj.read_file()
uri_content = uri_content.split("\n")
print(uri_content)

analyzer_obj = ApiAnalyzer(uri_content)
#analyzer_obj.detect_amorphous_uri()

'''''''''''''''''''''''''Amorphous URIs'''''''''''''''''''''''''''''''''
print("Detection of AmorphousURI:")
result_AP, result_P, p_count, ap_count = analyzer_obj.detect_amorphous_uri()
# Create the data string to write in the file]
pattern_type = "Amorphous"
uri_obj.write_data(result_AP, result_P, p_count, ap_count, selected, pattern_type)
print("Finished Detection of AmorphousURI.\n")


'''''''''''''''''''''''''Non Standard URIs'''''''''''''''''''''''''''''''
print("Detection of NonStandardURI:")
result_AP, result_P, p_count, ap_count = analyzer_obj.detect_non_standard_uri()
pattern_type = "Non Standard URI"
uri_obj.write_data(result_AP, result_P, p_count, ap_count, selected, pattern_type)
print("Finished Detection of NonStandardURI:\n")


'''''''''''''''''''''''''''CRUDyURI'''''''''''''''''''''''''''''''''''''''
print("Detection of CRUDyURI:")
result_AP, result_P, p_count, ap_count = analyzer_obj.detect_crudy_uri()
pattern_type = "CRUDyURI"
uri_obj.write_data(result_AP, result_P, p_count, ap_count, selected, pattern_type)
print("Finished Detection of CRUDyURI:")



'''''''''''''''''''''''''''UnversionedURIs'''''''''''''''''''''''''''''''''''''''
print("Detection of UnversionedURIs:")
result_AP, result_P, p_count, ap_count = analyzer_obj.detect_unversioned_uris()
pattern_type = "UnversionedURIs"
uri_obj.write_data(result_AP, result_P, p_count, ap_count, selected, pattern_type)
print("Finished Detection of UnversionedURIs:")

'''
#semaintic Analysis
uri_path = base_path+selected+"/"+selected+".txt"
print(uri_path)
uri_obj = FileReadWrite(uri_path)
uri_content = uri_obj.read_file()
uri_content = uri_content.split("\n")
print(uri_content)'''

api_endpoints = []
with open(f'APIs\\{selected}\\{selected}.txt', 'r') as file:
    for line in file:
        #parts = line.strip().split(' >> ')
        api_endpoints.append((line))


# Displaying the parsed data
#print(api_endpoints)
'''''''''''''''''''''''''''PluralisedNodes'''''''''''''''''''''''''''''''''''''''
print("Detection of PluralisedNodes:")
result_AP, result_P, p_count, ap_count = analyzer_obj.detect_pluralized_node(api_endpoints)
pattern_type = "PluralisedNodes"
uri_obj.write_data(result_AP, result_P, p_count, ap_count, selected, pattern_type)
#print(result_AP)
#print(result_P)
print("Finished Detection of PluralisedNodes:")


'''''''''''''''''''''''''Non-descriptiveURI'''''''''''''''''''''''''''''''''''''''
print("Detection of Non-descriptiveURI:")
result_AP, result_P, p_count, ap_count = analyzer_obj.detect_non_descriptive_uri()
pattern_type = "Non-descriptive"
uri_obj.write_data(result_AP, result_P, p_count, ap_count, selected, pattern_type)
print("Finished Detection of Non-descriptiveURI:")


#print(api_endpoints)
'''''''''''''''''''''''''ContextlessURI'''''''''''''''''''''''''''''''''''''''
#print("Detection of ContextlessURI:")
#result_AP, result_P, p_count, ap_count = analyzer_obj.detect_contextless(api_endpoints)
#pattern_type = "Contextless"
#uri_obj.write_data(result_AP, result_P, p_count, ap_count, selected, pattern_type)
#print("Finished Detection of ContextlessURI:")



'''''''''''''''''''''''''NonHierarchicalNodes'''''''''''''''''''''''''''''''''''''''
print("Detection of NonHierarchicalNodes:")
result_AP, result_P, p_count, ap_count = analyzer_obj.detect_non_hierarchical_nodes()
pattern_type = "NonHierarchicalNodes"
uri_obj.write_data(result_AP, result_P, p_count, ap_count, selected, pattern_type)
print("Finished Detection of NonHierarchicalNodes:")


