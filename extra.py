api_endpoints = []

with open('APIs\\Node-RED\\Node-RED.txt', 'r') as file:
    for line in file:
        #parts = line.strip().split(' >> ')
        api_endpoints.append((line))

# Displaying the parsed data
print(api_endpoints)
