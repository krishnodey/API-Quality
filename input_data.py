import json

#ceate a jsonl file of all data
base_path = ['REST-APIs/', 'GraphQL-APIs/']
i = 1

write_path = 'All-Data/input_data.jsonl'
out_file = open(write_path, 'w')

for base in base_path:
        api_path = f"{base}APIList.txt"
        with open(api_path, 'r', encoding="iso-8859-1") as file:
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
                        line_dict.update({"api_category": ""})
                                    
                        json_string=json.dumps(line_dict,ensure_ascii=False)
                        out_file.write(json_string+"\n")
                        i += 1     
out_file.close()

print("Data has been written to input_data.jsonl")