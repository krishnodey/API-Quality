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

analyzer_obj = ApiAnalyzer(api_type, selected)


print("Detection of AmorphousURI:")
analyzer_obj.detect_amorphous_uri()
print("\nFinished Detection of AmorphousURI.\n")


print("Detection of NonStandardURI:")
analyzer_obj.detect_non_standard_uri()
print("\nFinished Detection of NonStandardURI:\n")



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

# # print("Detection of Non_FilteringEndpoint:")
# # analyzer_obj.detect_non_filtering_endpoint()
# # print("\nFinished Detection of Non_FilteringEndpoint:\n")


# print("Detection of ParameterTunneling:")
# analyzer_obj.detect_parameters_tunneling()
# print("\nFinished Detection of ParameterTunneling:\n")



# print("Detection of InconsistentResoruceArchetype:")
# analyzer_obj.detect_incosistent_resource_archetype()
# print("\nFinished Detection of InconsistentResoruceArchetype:\n")


# print("Detection of IndentifierAmbiguity:")
# analyzer_obj.detect_identifier_ambiguity()
# print("\nFinished Detection of IndentifierAmbiguity:\n")


print("Detection of FlatEndpoint:")
analyzer_obj.detect_flat_endpoint()
print("\nFinished Detection of FlatEndpoint:\n")