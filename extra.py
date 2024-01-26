from file_handler import FileReadWrite

'''api_endpoints = []

with open('APIs\\Node-RED\\Node-RED.txt', 'r') as file:
    for line in file:
        #parts = line.strip().split(' >> ')
        api_endpoints.append((line))

# Displaying the parsed data
print(api_endpoints)
'''

'''path = "acronyms.txt"

read_data = FileReadWrite(path)
data = read_data.read_data()
print(data)

for line in data:
    line  = line.split(">>")
    line[1].strip("\n")
    print(line[0] +"  -------  "+line[1])'''

'''#patterns and anti-patterns
base_path = "GraphQL-APIs"
selected = "Instagram"
uri_path = base_path+"/"+selected+"/"+selected+".txt"
uri_obj = FileReadWrite(uri_path)
data = uri_obj.read_data()

#print(data)

uri = []
des= []
for line in data:
    line  = line.split(">>")
    uri.append(line[1])
    if(len(line) == 4):
        text = f"{line[2]} {line[3]}"
        des.append(text)
        

print(des)'''

'''from api_analyzer import ApiAnalyzer

data = ['/bulk/devices/remove']
obj = ApiAnalyzer(data)
#data = ['POST >> /bulk/devices/remove >> Delete multiple devices. Deletemultiple devices, each request can contain a maximum of 512 kB']

data = ['POST >> /bulk/devices/remove >> Remove multiple devices. Remove multiple devices, each request can contain a maximum of 512 kB']

ap, p, pc, apc = obj.detect_inconsistent_documentations(data)
print(f"anti-pattern: {ap}")
print(f"Pattern: {p}")'''


from uri_cleaning import UriCleaning

text = "Creates a new StorefrontAccessToken.json new_palyer et v ge"
obj = UriCleaning()
#print(obj.preprocess_documentation(text))
node = "device/{ID}/name_pq"
print(obj.get_uri_nodes(node))