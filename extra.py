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


'''from uri_cleaning import UriCleaning

text = "Creates a new StorefrontAccessToken.json new_palyer et v ge"
obj = UriCleaning()
#print(obj.preprocess_documentation(text))
node = "device/{ID}/name_pq"
print(obj.get_uri_nodes(node))'''

'''res_path = '.\Outputs-REST-APIs/Adobe Audience Manager-AmorphousURI.txt'
with open(res_path, 'r') as file:
    results = file.read()
    results = results.split('\n')
    for result in results:
        result = result.split("\t")
        #print(result)
        if '/available-data-feeds/' in result:
            #print('Found')
            if result[1].strip() == 'Tidy End-point':
                print("pattern")
            elif len(result) > 2:
                print('anti', result[2])
        else:
            print('Not Found')
            '''
'''import csv

base_path = ['REST-APIs/', 'GraphQL-APIs/']
i = 1

write_path = 'All-Data/Alldata.csv'

with open(write_path, 'w', newline='') as w_file:
    csv_writer = csv.writer(w_file)

    for base in base_path:
        api_path = f"{base}APIList.txt"
        with open(api_path, 'r') as file:
            apis = file.read().strip().split("\n")

            for api in apis:
                file_path = base + api + "/" + api + ".txt"
                print(f"\n-----Reading for {file_path}----\n")

                with open(file_path, 'r') as f:
                    data = f.read().strip().split("\n")

                    for line in data:
                        print(f"{i} {line}")
                        csv_writer.writerow([f"{i} {line}"])
                        i += 1

print("Data has been written to Alldata.csv")

'''
''''from uri_cleaning import UriCleaning
obj = UriCleaning()
text = '/codeadmin/v/2/library/{systemKey}/{name}'
processed_nodes =  obj.get_uri_nodes(text)
print(obj.get_uri_nodes(text))

for new in processed_nodes:
            print(new)
            for i in range(len(new)):
                val = obj.set_Acronym(new[i])
                print(new[i])
                print(val)
                if val is not None:
                    for index in range(len(val)):
                        if i + index < len(new):
                            new[i + index] = val[index]
                        else:
                            new.append(val[index])

print(processed_nodes)

val = obj.set_Acronym('codeadmin')
print(val)

#new = obj.get_Acronym(["codeadmin","api", "claire"])

#print(new)
                    
clean = obj.get_uri_nodes('codeadmin/api/cliareAll/newIs/eem/bop/v2')   

print(clean)

clean = obj.preprocess_documentation('Calls/executes ClearCode service_newIs')
print(clean)'''



'''def check_duplicates(file_path):
    lines_seen = set()
    duplicate_lines = []

    with open(file_path, 'r') as file:
        for line_num, line in enumerate(file, start=1):
            columns = line.strip().split()[:3]  # Extract the first three columns
            key = tuple(columns)
            if key in lines_seen:
                duplicate_lines.append(line_num)
                print(key)
            else:
                lines_seen.add(key)

    return duplicate_lines


file_path = '.\GraphQL-APIs\AppleMusic\AppleMusic.txt'
duplicates = check_duplicates(file_path)

print(duplicates)
if duplicates:
    print("Duplicate rows found at line(s):", duplicates)
else:
    print("No duplicate rows found.")'''

'''def check_duplicates(file_path):
    lines_seen = {}
    duplicate_lines = []

    with open(file_path, 'r') as file:
        for line_num, line in enumerate(file, start=1):
            columns = line.strip().split(">>")
            key = tuple(columns[:3])
            line_str = str(columns[:3])  # Convert the first three columns to a string
            #print(line_str)

            if key in lines_seen:
                duplicate_lines.append((line_num, key, lines_seen[key]))
            else:
                lines_seen[key] = line_num

    return duplicate_lines


#file_path = '.\GraphQL-APIs\AniList\AniList.txt'



base_path = ["REST-APIs","GraphQL-APIs"]
for api in base_path:
    print(f"Checking duplicates for {api}")
    api_path = f"{api.strip()}/APIList.txt"
    file_obj = FileReadWrite(api_path)
    content = file_obj.read_file()
    name_list = content.split('\n')
    for api_name in name_list:
        print(f"\nchecking ----> {api_name}\n")
        path = api+"/"+api_name+"/"+api_name+".txt"
        duplicates = check_duplicates(path)
        if duplicates:
            print("\nDuplicate rows found:")
            for line_num, key, original_line_num in duplicates:
                print(f"Line {line_num} and Line {original_line_num} have duplicate columns: {key}")
        else:
            print("\nNo duplicate rows found.")'''



'''import csv

def read_csv(file_path):
    data = []
    with open(file_path, 'r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)
        for row in csv_reader:
            data.append(row)
    return data

def compare_csv(file1_path, file2_path):
    data1 = read_csv(file1_path)
    data2 = read_csv(file2_path)
    
    print(f"Length of database file = {len(data1)}")
    print(f"Length of alldata file = {len(data2)}")

    print(data1)
    # Find the index of columns to compare in both files
    indices_to_compare = [2, 3, 4]  # Indices of columns 3, 4, and 5

    # Create sets of rows for each file based on the specified columns
    rows_set1 = set(tuple(row[i] for i in indices_to_compare) for row in data1)
    rows_set2 = set(tuple(row[i] for i in indices_to_compare) for row in data2)

    # Find uncommon rows
    uncommon_rows = rows_set1.symmetric_difference(rows_set2)

    # Print uncommon rows
    if uncommon_rows:
        print("Uncommon rows:")
        for row_tuple in uncommon_rows:
            print(row_tuple)

# Example usage
file1_path = "./Result-Database/result_database.csv"
file2_path = "./All-Data/Alldata.csv"

compare_csv(file1_path, file2_path)'''

'''import csv

databse_path = "./Result-Database/result_database.csv"
alldata_path = "./All-Data/Alldata.csv"

with open(alldata_path, "r") as all_file, open(databse_path, 'r') as db_file:
    all = csv.reader(all_file)
    db = csv.reader(db_file)
    next(all)
    next(db)
    tw = 0
    anilist = 0
    apple = 0
    artsy = 0
    fb = 0
    github = 0
    gitlab = 0
    instagram = 0
    pipefy = 0
    poke = 0
    shopify = 0
    brain = 0
    api = ["AniList", "AppleMusic", "Artsy", "Braintree", "Facebook", "GitHub", "GitLab", "Instagram", "Pipefy", "Pokeapi", "Shopify", "Twitter"]
    for row1 in all:
        if row1[2] == api[0].strip():
            anilist += 1
        elif row1[2] == api[1].strip():
            apple += 1
        elif row1[2] == api[2].strip():
            artsy += 1
        elif row1[2] == api[3].strip():
            brain += 1
        elif row1[2] == api[4].strip():
            fb += 1
        elif row1[2] == api[5].strip():
            github += 1
        elif row1[2] == api[6].strip():
            gitlab += 1
        elif row1[2] == api[7].strip() and row1[1] == "GraphQL":
            instagram += 1
        elif row1[2] == api[8].strip():
            pipefy += 1
        elif row1[2] == api[9].strip():
            poke += 1
        elif row1[2] == api[10].strip() and row1[1] == "GraphQL":
            shopify += 1
        elif row1[2] == api[11].strip():
            tw += 1
    print(f"AniList = {anilist}, AppleMusic +{apple}, Artsy = {artsy}, Braintree{brain}, Facebook = {fb}, GitHub = {github}, GitLab = {gitlab}, Instagram = {instagram}, Pipefy = {pipefy}, Pokeapi = {poke}, Shopify = {shopify},Twiter = {tw}")
        
    tw = 0
    anilist = 0
    apple = 0
    artsy = 0
    fb = 0
    github = 0
    gitlab = 0
    instagram = 0
    pipefy = 0
    poke = 0
    shopify = 0
    brain = 0
    api = ["AniList", "AppleMusic", "Artsy", "Braintree", "Facebook", "GitHub", "GitLab", "Instagram", "Pipefy", "Pokeapi", "Shopify", "Twitter"]
    for row1 in db:
        if row1[2] == api[0].strip():
            anilist += 1
        elif row1[2] == api[1].strip():
            apple += 1
        elif row1[2] == api[2].strip():
            artsy += 1
        elif row1[2] == api[3].strip():
            brain += 1
        elif row1[2] == api[4].strip():
            fb += 1
        elif row1[2] == api[5].strip():
            github += 1
        elif row1[2] == api[6].strip():
            gitlab += 1
        elif row1[2] == api[7].strip() and row1[1] == "GraphQL":
            instagram += 1
        elif row1[2] == api[8].strip():
            pipefy += 1
        elif row1[2] == api[9].strip():
            poke += 1
        elif row1[2] == api[10].strip() and row1[1] == "GraphQL":
            shopify += 1
        elif row1[2] == api[11].strip():
            tw += 1
    print(f"AniList = {anilist}, AppleMusic +{apple}, Artsy = {artsy}, Braintree{brain}, Facebook = {fb}, GitHub = {github}, GitLab = {gitlab}, Instagram = {instagram}, Pipefy = {pipefy}, Pokeapi = {poke}, Shopify = {shopify},Twiter = {tw}")
     

private_api = ["Adobe Audience Manager", "Apple App Store Connect", "BroadCom", "GroupWise", "Survey"]
public_api = ["Amazon AWS Core IoT","Arduino IoT Cloud","Cisco Flare","ClearBlade","Dropbox","Droplit.io","Facebook Graph API""Google Nest", "IBM Watson IoT","Instagram", "Linkedin","Losant","Microsoft Azure IoT","Microsoft Power BI","Node-RED","Samsung ARTIK Cloud","Sonos", "Stack Overflow", "The Things Network", "Twitter", "YouTube"]
partner_api = ["IBM Cloud Pak System", "LiveAgent", "Microsoft Partner Center", "Oracle Cloud Marketplace Publisher", "Prolateral Core Infrastructure", "QuickBooks", "Shopify", "Uber", "WM3 Multishop"]
graph_public = ["AniList", "AppleMusic", "Artsy", "Braintree", "Facebook", "GitHub", "GitLab", "Instagram", "Pipefy", "Pokeapi", "Shopify", "Twitter"]
def set_public_private(text, api):
    if api == "REST":
        if text in private_api:
            return "Private"
        elif text in public_api:
            return "Public"
        elif text in partner_api:
            return "Partner"
    else:
        if text in partner_api:
            return "Public"

print(set_public_private("BroadCom", "REST"))'''


from uri_cleaning import UriCleaning

text = "Creates a new StorefrontAccessToken.json new_palyer et v ge"
obj = UriCleaning()
node = "device/{ID}/name.jpg"
print(obj.get_uri_nodes(node))