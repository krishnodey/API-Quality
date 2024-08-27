from file_handler import FileReadWrite
import json


output_file = 'All-Data\\merged_output.jsonl'

base_path = ["REST-APIs", "GraphQL-APIs"]
with open(output_file, 'w', encoding='utf-8') as outfile:
    for api in base_path:
        print(f"Merging {api}")
        api_path = f"{api.strip()}/APIList.txt"
        file_obj = FileReadWrite(api_path)
        content = file_obj.read_file()
        name_list = content.split('\n')
        api_type = 'REST' if 'REST-APIs' in api else 'GraphQL'
        for api_name in name_list:
            file = f"All-Data\\temp\\{api_type}\\{api_name}.jsonl"
            print(file)
            with open(file, 'r') as infile:
                for line in infile:
                    # Load the JSON object
                    line_dict = json.loads(line)
                    # Write to output file
                    json_string=json.dumps(line_dict,ensure_ascii=False)
                    outfile.write(json_string + '\n')
            
        print(f'Merged all files into {output_file}')
