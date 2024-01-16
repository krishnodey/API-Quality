from file_handler import FileReadWrite

'''api_endpoints = []

with open('APIs\\Node-RED\\Node-RED.txt', 'r') as file:
    for line in file:
        #parts = line.strip().split(' >> ')
        api_endpoints.append((line))

# Displaying the parsed data
print(api_endpoints)
'''

path = "acronyms.txt"

read_data = FileReadWrite(path)
data = read_data.read_data()
print(data)

for line in data:
    line  = line.split(">>")
    line[1].strip("\n")
    print(line[0] +"  -------  "+line[1])
