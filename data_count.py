import csv

base_path = ['REST-APIs/', 'GraphQL-APIs/']
i = 1

write_path = 'All-Data/Alldata.csv'

with open(write_path, 'w', newline='') as w_file:
    csv_writer = csv.writer(w_file)
    header = ["ID", 'API-Type',"API-Name", "HTTP Method", "URI", "Description+Parameters"]
    csv_writer.writerow(header)

    for base in base_path:
        api_path = f"{base}APIList.txt"
        with open(api_path, 'r') as file:
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
                            c1 = line[0].strip()
                            c2 = line[1].strip()
                            line[3] = ' '.join(line[3].split())
                            c3 = f"{line[2].strip()} {line[3].strip()}"                     
                        else:
                            c1,c2,c3 = line[0].strip(), line[1].strip(), line[2].strip()
                        lst = ([i, api_type, api, c1, c2, c3])

                        csv_writer.writerow(lst)
                        i += 1

print("Data has been written to Alldata.csv")


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



