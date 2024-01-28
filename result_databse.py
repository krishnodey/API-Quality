from file_handler import FileReadWrite
import csv
import json

# Specify the file path
base_path = ['./Outputs-REST-APIs/', './Outputs-GraphQL-APIs/']
out_base = './Out_All/'
pattern_types = ["AmorphousURI", "NonStandardURI", "CRUDyURI","UnversionedURIs","PluralisedNodes", "NonDescriptiveURI", "NonHierarchicalNodes", "InconsistantDoc"]


count = 0
for base in base_path:
    api_path = f"{base[10:].strip()}APIList.txt"
    file_obj = FileReadWrite(api_path)
    content = file_obj.read_file()
    apis = content.strip().split("\n")
    data = []
    api_type = 'REST' if 'REST-API' in base else 'GraphQL'
    for api in apis:
        #print(api)
        d2 = {}
        for pattern in pattern_types:
            out_dir = out_base+api_type+"-"+api+"-"+pattern+".txt"
            print("\n")
            print(out_dir, "-----------------------------\n\n")
            with open(out_dir, 'r', encoding="utf-8") as f:
                lines = f.read().strip().split("\n")
                for line in lines[1:]:
                    count += 1
                    #print(line)
                    line = line.split("\t")
                    if len(line) == 6:
                        c1, c2, c3,c4,c5, c6 = line[0].strip(), line[1].strip(), line[2].strip(), line[3].strip(), line[4].strip(), line[5].strip()
                        
                    else:
                        c1,c2,c3,c4,c5,c6 = line[0].strip(), line[1].strip(), line[2].strip(), line[3].strip(), line[4].strip(), " "

                    if f'{c1}+{c2}' not in d2:
                        d2[f'{c1}+{c2}'] = [f"{api}",c1, c2, c3, c4, c5, c6]
                    else:
                        d2[f'{c1}+{c2}'].extend([c4, c5, c6])
        data.append(d2)
        
with open("Out_All/result_database.csv", 'w') as file:
    header_line = ['ID','API-Type', 'API-Name','HTTP Method','URI', 'Decription', 'Parameters','AmorphousURI', 'TidyURI','Comment', 'NonStandardURI', 'StandarURI','Comment' ,'CRUDyURI', 'VerblessURI', 'Comment',
                       'UnversionedURI', 'VersionedURI','Comment' , 'PluralisedNodes', 'SingularNodes','Comment' , 'NonDescriptiveURI',
                       'DescriptiveURI','Comment' , 'ContextlessResource', 'ContextualResouce','Comment', 'NonHierarchicalNodes', 'HierarchicalNodes', 'Comment',
                       'LessCohisiveDoc', 'CohisiveDoc','Comment', 'InconsistantDoc', 'ConsistantDoc','Comment']
    csv_writer = csv.writer(file)
    csv_writer.writerow(header_line)
    i = 1
    for d in data:
        for key, value in d.items():
            lst = [i,api_type]
            lst.extend(value)
            #a = [i, api_type]
            #a.extend(value)
            #print(a)
            #if len(a) != 29:
            #    print(i)
            #    print(a)
            #i+=1
            print(lst)
            csv_writer.writerow(lst)
            i = i + 1
            lst = []
    print('--'*25)

print(count)

#POST >> /v1/me/library >> Add a catalog resource to a user’s iCloud Music Library.>>ids [string] (Required) The unique catalog identifiers for the resources. To indicate the type of resource to add, follow the ids with one of the allowed values. Add multiple types in the same request. l string The localization to use, specified by a language tag. The possible values are in the supportedLanguageTags array belonging to the Storefront object that storefront specifies. Otherwise, the default is defaultLanguageTag in Storefront.
#POST >> /v1/me/library >> Add a catalog resource to a user’s iCloud Music Library. >>n/a

#'Add a catalog resource to a userÃ¢â‚¬â„¢s iCloud Music Library.



'''for base in base_path:
    api_path = f"{base[10:].strip()}APIList.txt"
    file_obj = FileReadWrite(api_path)
    content = file_obj.read_file()
    summary_file = "Result-Database/"+base[10:-1].strip()+"-Result-Database.csv"

    with open(summary_file, 'w', newline='') as summ_file:
        csv_writer = csv.writer(summ_file)
        header_line = ['ID','API-Type', 'API-Name','HTTP Method','URI', 'Decription', 'Parameters','AmorphousURI', 'TidyURI','Comment', 'NonStandardURI', 'StandarURI','Comment' ,'CRUDyURI', 'VerblessURI', 'Comment',
                       'UnversionedURI', 'VersionedURI','Comment' , 'PluralisedNodes', 'SingularNodes','Comment' , 'NonDescriptiveURI',
                       'DescriptiveURI','Comment' , 'ContextlessResource', 'ContextualResouce','Comment', 'NonHierarchicalNodes', 'HierarchicalNodes', 'Comment',
                       'LessCohisiveDoc', 'CohisiveDoc','Comment', 'InconsistantDoc', 'ConsistantDoc','Comment', 'Type(Public/Partner/Private)']
        csv_writer.writerow(header_line)
        uri_id = 1
        
        #print(content)
        for api in content.split('\n'):
            
            print("\n\n"+api+"\n\n")
            in_dir = base[10:].strip()+api+"/"+api+".txt"
        
            in_data = {}
            with open(in_dir) as f:
                lines = f.read().strip().split("\n")
                for line in lines:
                    if base == './Outputs-GraphQL-APIs/':
                        method, uri, des, para = line.strip().split(">>") 
                        des = des+para   
                    else:
                        method, uri, des = line.strip().split(">>")
                    in_data[uri.strip()] = [method.strip(), des.strip()]

            data = []
            for pattern in pattern_types:
                out_dir = base.strip()+"/"+api+"-"+pattern+".txt"
            

                with open(out_dir) as f:
                    lines = f.read().strip().split("\n")
                    for line in lines:
                        if line.startswith('/'):
                            nd = line.strip().split("\t")
                            if len(nd) == 3:
                                uri = nd[0].strip()
                                pname = nd[1].strip()
                                comment = nd[2].strip()
                            else:
                                uri = nd[0].strip()
                                pname = nd[1].strip()
                                comment = ''
                            #uri = uri.strip()
                            if uri in in_data:
                                #if method == in_data[uri][0]:
                                d = {}
                                d['uri'] = uri
                                d['method'] = in_data[uri][0]
                                d['description'] = in_data[uri][1]
                                d['pattern_name'] = pname.strip()
                                d['comment'] = comment
                                data.append(d)
                            else:
                                print(f'URI not found: {uri}')
                for row in data:
                    print(row)

            print("\n\n\n")'''
                




























'''with open(data_path, 'r') as file:
                data = file.read()
                data = data.split('\n')

            for pattern in pattern_types:
                res_path = base.strip()+"/"+api+"-"+pattern+".txt"
                
                
                
                
                with open(res_path, 'r') as file:
                    results = file.read()
                    results = results.split('\n')
                    lst = []
                    for line in results:
                        if '***Patterns***' not in line and '***Anti-Pattern***' not in line and 'Count:' not in line and line.strip() != '':
                            lst.append(line) 

                #uri_column = [line.split('>>')[1].strip() for line in data]
                
                for line_file2, line in zip(lst,data):
                    data_line = []
                    line = line.split(">>")
                    data_line.extend([uri_id,base[10:-1].strip(), api, line[0],line[1],line[2]])
                    #print(f"{uri_id},{base[10:-1].strip()}, {api}, {line[0]},{line[1]},{line[2]}", end = " ")
                    uri_id += 1
                    if any(column_file1_value in line_file2 for column_file1_value in uri_column):
                        line_file2 = line_file2.split('\t')
                        p = 0
                        ap = 0
                        if pattern == "AmorphousURI" : # "","PluralisedNodes", , ""]
                            if line_file2[1].strip() == 'Tidy End-point':
                                p = 1
                            elif line_file2[1].strip() == 'Amorphous End-point':
                                ap = 1
                            print(f"{line_file2[0]} ---> {line_file2[1]} --> {p} -->{ap} -->{line_file2[2]}")
                            data_line.extend([line_file2[0], line_file2[1], p, ap, line_file2[2]])
                        if pattern == "ContextlessResource":
                            if line_file2[1].strip() == 'Contextual Resource Names':
                                p = 1
                            elif line_file2[1].strip() == 'Contextless Resource Names':
                                ap = 1
                            data_line.extend([line_file2[0], line_file2[1], p, ap, ' '])
                            print(f"{line_file2[0]}---> {line_file2[1]} --> {p} --> {ap}")
                        if pattern == "CRUDyURI":
                            if line_file2[1].strip() == 'Verbless End-point':
                                p = 1
                            elif line_file2[1].strip() == 'CRUDy End-point':
                                ap = 1
                            data_line.extend([line_file2[0], line_file2[1], p, ap, line_file2[2]])
                            print(f"{line_file2[0]} --->{line_file2[1]} -->{p} -->{ap}-->{line_file2[2]}")
                        if pattern == "InconsistantDoc":
                            if line_file2[2].strip() == 'Consistent Documentation':
                                p = 1
                            elif line_file2[2].strip() == 'Inconsistent Documentation':
                                ap = 1
                            data_line.extend([line_file2[0], line_file2[1], p, ap, line_file2[2]])
                            print(f"{line_file2[1]} ---> {line_file2[2]}-->{p} -->{ap}")
                        if pattern == "LessCohisiveDoc":
                            if line_file2[1].strip() == 'Pertinent Documentation':
                                p = 1
                            elif line_file2[1].strip() == 'Non-pertinent Documentation':
                                ap = 1
                            data_line.extend([line_file2[0], line_file2[1], p, ap, ' '])
                            print(f"{line_file2[0]} ---> {line_file2[1]}-->{p} -->{ap}")
                        if pattern == "NonDescriptiveURI":
                            if line_file2[1].strip() == 'Self-descriptive End-point':
                                p = 1
                            elif line_file2[1].strip() == 'Non-descriptive End-point':
                                ap = 1
                            data_line.extend([line_file2[0], line_file2[1], p, ap, ' '])
                            print(f"{line_file2[0]} ---> {line_file2[1]}-->{p} -->{ap}")
                        if pattern == "NonHierarchicalNodes":
                            if line_file2[1].strip() == 'Hierarchical Nodes':
                                p = 1
                            elif line_file2[1].strip() == 'Non-hierarchical Nodes':
                                ap = 1
                            data_line.extend([line_file2[0], line_file2[1], p, ap, ' '])
                            print(f"{line_file2[0]} ---> {line_file2[1]}-->{p} -->{ap}")
                        if pattern == "NonStandardURI":
                            if line_file2[1].strip() == 'Standard End-point':
                                p = 1
                            elif line_file2[1].strip() == 'Non-standard End-point':
                                ap = 1
                            data_line.extend([line_file2[0], line_file2[1], p, ap, line_file2[2]])
                            print(f"{line_file2[0]} ---> {line_file2[1]}-->{p} -->{ap}-->{line_file2[2]}")
                        if pattern == "PluralisedNodes":
                            if line_file2[2].strip() == 'Singularized Nodes' or line_file2[2].strip() == 'regular methods.':
                                p = 1
                            elif line_file2[2].strip() == 'Pluralized Nodes':
                                ap = 1
                            if len(line_file2) >= 4:
                                data_line.extend([line_file2[1], line_file2[2], p, ap, line_file2[3]])
                                print(f"{line_file2[1]} ---> {line_file2[2]} -->{p} -->{ap}--> {line_file2[3]}")
                            else:
                                data_line.extend([line_file2[1], line_file2[2], p, ap, ' '])
                                print(f"{line_file2[1]}---> {line_file2[2]}-->{p} -->{ap}")
                        if pattern == "UnversionedURIs":
                            if line_file2[1].strip() == '[Version found.]':
                                p = 1
                            elif line_file2[1].strip() == '[No version found.]':
                                ap = 1
                            data_line.extend([line_file2[0], line_file2[1], p, ap, ' '])
                            print(f"{line_file2[0]} ---> {line_file2[1]}-->{p} -->{ap}")
                    csv_writer.writerow(data_line)
                            #data_line.extend([line_file2[1], line_file2[2]])
                #print(data_line)'''

