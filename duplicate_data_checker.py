from file_handler import FileReadWrite
def check_duplicates(file_path):
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


#file_path = '.\GraphQL-APIs\AniList\AniList.txt

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
            print("\nNo duplicate rows found.")
