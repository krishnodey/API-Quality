import csv
import json



#ceate a jsonl file of all data

base_path = ['REST-APIs/', 'GraphQL-APIs/']
i = 1

write_path = 'All-Data/Alldata.jsonl'
out_file = open(write_path, 'w')

#with open(write_path, 'w', newline='') as w_file:
    #csv_writer = csv.writer(w_file)
    #header = ["ID", 'API-Type',"API-Name", "HTTP Method", "URI", "Description+Parameters"]
    #csv_writer.writerow(header)

for base in base_path:
        api_path = f"{base}APIList.txt"
        with open(api_path, 'r', encoding='utf-8') as file:
            apis = file.read().strip().split("\n")
            api_type = 'REST' if 'REST-API' in base else 'GraphQL'
            for api in apis:
                file_path = base + api + "/" + api + ".txt"
                print(f"\n-----Reading for {file_path}----\n")

                with open(file_path, 'r') as f:
                    data = f.read().strip().split("\n")

                    for line in data:
                        #print(f"{i} {line}")
                        line = line.strip().split(">>")
                        if len(line) == 4:
                            c1, c2, c3, c4 = line[0].strip(), line[1].strip(), line[2].strip(), line[3].strip()
                        else:
                            c1,c2,c3, c4 = line[0].strip(), line[1].strip(), line[2].strip(), ''

                        line_dict = {"id": i,"api_type": api_type, "api_name": api,"method": c1, "uri": c2, "description": c3, 'parameters': c4}
                        line_dict.update({"amorphous_uri": 0, "tidy_uri": 0, 'amorphous_comment': ""})
                        line_dict.update({"crudy_uri": 0 , "verbless_uri": 0, "crudy_comment": ""})
                        line_dict.update({"contextless_resource": 0, "contextual_resouce": 0, 'contextless_comment': ""})
                        line_dict.update({"inconsistent_doc": 0, "consistent_doc": 0, 'inconsistent_comment': ""})
                        line_dict.update({"less_cohesive_doc": 0, "cohesive_doc": 0, 'less_cohesive_comment': ""})
                        line_dict.update({"non_descriptive_uri": 0, "descriptive_uri": 0, 'non_descriptive_comment': ""})
                        line_dict.update({"non_hierarchical_nodes": 0, "hierarchical_nodes": 0, 'non_hierarchical_comment': ""})
                        line_dict.update({"non_standard_uri": 0, "standard_uri": 0, 'non_standard_comment': ""})
                        line_dict.update({"pluralized_nodes": 0, "singularized_nodes": 0, 'pluralized_comment': ""})
                        line_dict.update({"unversioned_uri": 0, "versioned_uri": 0, 'unversioned_comment': ""})
                        line_dict.update({"api_category": ""})
                                    

                        '''header_line = ['ID','API-Type', 'API-Name','HTTP Method','URI', 'Decription+Parameters', 
                                       'AmorphousURI', 'TidyURI','Comment',
                                        'NonStandardURI', 'StandarURI','Comment' ,
                                        'CRUDyURI', 'VerblessURI', 'Comment',
                                        'UnversionedURI', 'VersionedURI','Comment' , 
                                        'PluralisedNodes', 'SingularNodes','Comment' , 
                                        'NonDescriptiveURI','DescriptiveURI','Comment' , 
                                        'ContextlessResource', 'ContextualResouce','Comment', 
                                        'NonHierarchicalNodes', 'HierarchicalNodes', 'Comment',
                                        'LessCohisiveDoc', 'CohisiveDoc','Comment', 
                                        'InconsistantDoc', 'ConsistantDoc','Comment', 
                                        "Type(Public/Private/Partner)"]'''
    
                        json_string=json.dumps(line_dict,ensure_ascii=False)
                        out_file.write(json_string+"\n")
                        i += 1     
out_file.close()

print("Data has been written to Alldata.jsonl")


'''import csv
pattern_types = ["AmorphousURI", "NonStandardURI", "CRUDyURI", "UnversionedURIs", "PluralisedNodes", "NonDescriptiveURI", "ContextlessResource", "NonHierarchicalNodes", "LessCohisiveDoc", "InconsistantDoc"]
base_path = ['REST-APIs/', 'GraphQL-APIs/']
out_path = 'Out_All/'
i = 1

#write_path = 'All-Data/Alldata.csv'
for base in base_path:
    api_path = f"{base}APIList.txt"
    with open(api_path, 'r') as file:
        apis = file.read().strip().split("\n")
        api_type = 'REST-' if 'REST-API' in base else 'GraphQL-'
        for api in apis:
            for pattern in pattern_types:
                j = 0
                file_path = out_path + api_type+ api + "-" + pattern+".txt"
                print(f"\n-----Reading for {file_path}----\n")
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = f.read().strip().split("\n")
                    for line in data:
                        #print(f"{i} {line}")
                        j +=1
                        i += 1
                print(f"{j}\n")

print("Data has been written to Alldata.csv")'''



