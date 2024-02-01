from file_handler import FileReadWrite
import csv
import json

#set public private and partner
private_api = ["Adobe Audience Manager", "Apple App Store Connect", "BroadCom", "GroupWise", "Survey"]
public_api = ["Amazon AWS Core IoT","Arduino IoT Cloud","Cisco Flare","ClearBlade","Dropbox","Droplit.io","Facebook Graph API""Google Nest", "IBM Watson IoT","Instagram", "Linkedin","Losant","Microsoft Azure IoT","Microsoft Power BI","Node-RED","Samsung ARTIK Cloud","Sonos", "Stack Overflow", "The Things Network", "Twitter", "YouTube"]
partner_api = ["IBM Cloud Pak System", "LiveAgent", "Microsoft Partner Center", "Oracle Cloud Marketplace Publisher", "Prolateral Core Infrastructure", "QuickBooks", "Shopify", "Uber", "WM3 Multishop"]
graph_public = ["AniList", "AppleMusic", "Artsy", "Braintree", "Facebook", "GitHub", "GitLab", "Instagram", "Pipefy", "Pokeapi", "Shopify", "Twitter"]
def set_public_private(text, api):
    text = text.strip()
    if api.strip() == "REST":
        if text in private_api:
            return "Private"
        elif text in public_api:
            return "Public"
        elif text in partner_api:
            return "Partner"
    else:
        if text in graph_public:
            return "Public"
        
# Specify the file path
base_path = ['./Outputs-REST-APIs/', './Outputs-GraphQL-APIs/']
out_base = './Out_All/'
pattern_types = ["AmorphousURI", "NonStandardURI", "CRUDyURI", "UnversionedURIs", "PluralisedNodes", "NonDescriptiveURI", "ContextlessResource", "NonHierarchicalNodes", "LessCohisiveDoc", "InconsistantDoc"]

count = 0
with open("Result-Database/result_database.csv", 'w', newline='') as file:
    header_line = ['ID','API-Type', 'API-Name','HTTP Method','URI', 'Decription+Parameters', 'AmorphousURI', 'TidyURI','Comment', 'NonStandardURI', 'StandarURI','Comment' ,'CRUDyURI', 'VerblessURI', 'Comment',
                            'UnversionedURI', 'VersionedURI','Comment' , 'PluralisedNodes', 'SingularNodes','Comment' , 'NonDescriptiveURI',
                            'DescriptiveURI','Comment' , 'ContextlessResource', 'ContextualResouce','Comment', 'NonHierarchicalNodes', 'HierarchicalNodes', 'Comment',
                            'LessCohisiveDoc', 'CohisiveDoc','Comment', 'InconsistantDoc', 'ConsistantDoc','Comment', "Type(Public/Private/Partner)"]
    csv_writer = csv.writer(file)
    csv_writer.writerow(header_line)
    i = 0
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

                        if f'{c1}+{c2}+{c3}' not in d2:
                            d2[f'{c1}+{c2}+{c3}'] = [f"{api}",c1, c2, c3, c4, c5, c6]
                        else:
                            d2[f'{c1}+{c2}+{c3}'].extend([c4, c5, c6])
            data.append(d2)
        for type in data:
            for key, value in type.items():
                i += 1
                lst =[i, api_type]
                lst.extend(value)
                public = set_public_private(value[0], api_type)
                lst.extend([public])
                csv_writer.writerow(lst)
                #print(lst)
                

