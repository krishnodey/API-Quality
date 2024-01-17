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

#patterns and anti-patterns
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
        

print(des)