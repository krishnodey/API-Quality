from file_handler import FileReadWrite
from display_options import APIChoice
from api_analyzer import ApiAnalyzer


print("Select an API Type")
print("1. REST APIs\n2. GraphQL APIs")
api= int(input())
if api == 1:
    base_path = "REST-APIs/"
    api_type = 'REST'
elif api == 2:
    base_path = "GraphQL-APIs/"
    api_type = 'GraphQL'
else:
    print("Enter a Valid Number")

#diplay choices
apilist_path = base_path + 'APIList.txt'
print(apilist_path)
api_obj = APIChoice(apilist_path)
#api_choice.display_choices()
api_obj.select_choice()
selected = api_obj.get_selected_choice()
print(f"Your selected choice is: {selected}")


#patterns and anti-patterns
uri_path = base_path+selected+"/"+selected+".txt"
uri_obj = FileReadWrite(uri_path)
#data = uri_obj.read_data()
#print(data)
#uri = []
#des = []
#for line in data:
#    line  = line.split(">>")
#    uri.append(line[1])

#print(uri)

analyzer_obj = ApiAnalyzer(api_type, selected)
#analyzer_obj.detect_amorphous_uri()

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


# print("Detection of Non_FilteringEndpoint:")
# result_AP, result_P, p_count, ap_count= analyzer_obj.detect_non_filtering_endpoint()
# pattern_type = "Non-Filtering-Endpoint"
# uri_obj.write_data(result_AP, result_P, p_count, ap_count, selected, pattern_type, base_path)
# print("\nFinished Detection of Non_FilteringEndpoint:\n")


# print("Detection of ParameterTunneling:")
# result_AP, result_P, p_count, ap_count= analyzer_obj.detect_parameters_tunneling()
# pattern_type = "ParameterTunneling"
# uri_obj.write_data(result_AP, result_P, p_count, ap_count, selected, pattern_type, base_path)
# print("\nFinished Detection of ParameterTunneling:\n")



# print("Detection of InconsistentResoruceArchetype:")
# result_AP, result_P, p_count, ap_count= analyzer_obj.detect_incosistent_resource_archetype()
# pattern_type = "Incosistent_Archetypes"
# uri_obj.write_data(result_AP, result_P, p_count, ap_count, selected, pattern_type, base_path)
# print("\nFinished Detection of InconsistentResoruceArchetype:\n")


print("Detection of IndentifierAmbiguity:")
result_AP, result_P, p_count, ap_count= analyzer_obj.detect_identifier_ambiguity()
pattern_type = "IndentifierAmbiguity"
uri_obj.write_data(result_AP, result_P, p_count, ap_count, selected, pattern_type, base_path)
print("\nFinished Detection of IndentifierAmbiguity:\n")


# print("Detection of FlatEndpoint:")
# result_AP, result_P, p_count, ap_count= analyzer_obj.detect_flat_endpoint()
# pattern_type = "FlatEndpoint"
# uri_obj.write_data(result_AP, result_P, p_count, ap_count, selected, pattern_type, base_path)
# print("\nFinished Detection of FlatEndpoint:\n")