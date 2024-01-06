from file_handler import FileReadWrite
from display_options import APIChoice
from api_analyzer import ApiAnalyzer


base_path = "APIs/"


apilist_path = base_path + 'APIList.txt'  # Replace with your CSV file path
api_obj = APIChoice(apilist_path)
#api_choice.display_choices()
api_obj.select_choice()
selected = api_obj.get_selected_choice()
print(f"Your selected choice is: {selected}")

uri_path = base_path+selected+"/APITest.txt"
uri_obj = FileReadWrite(uri_path)
uri_content = uri_obj.read_file()
uri_content = uri_content.split("\n")
#print(uri_content)

analyzer_obj = ApiAnalyzer(uri_content)
#analyzer_obj.detect_amorphous_uri()

'''''''''''''''''''''''''Amorphous URIs'''''''''''''''''''''''''''''''''
print("Detection of AmorphousURI:")
result_AP, result_P, p_count, ap_count = analyzer_obj.detect_amorphous_uri()
# Create the data string to write in the file]
pattern_type = "Amorphous"
uri_obj.write_data(ap_count, result_AP, p_count, result_P, selected, pattern_type)
print(f"Finished Detection of AmorphousURI.")





'''
data_to_write = f"***Anti-Pattern*** \nCount: {ap_count}\n"
for item in result_AP:
    data_to_write += item + "\n"
data_to_write += f"\n***Patterns*** \nCount: {p_count}\n"
for item in result_P:
    data_to_write += item + "\n"
out_path = "Outputs/"+selected + "-AmorphousURI.txt"
# Write the data to a file
uri_obj.write_file(data_to_write, out_path)
print("Finished Detection of AmorphousURI:")'''







'''
file_handler = FileReadWrite(path)

# Read from the file
content = file_handler.read_file()
print(type(content))
if content:
    print(f"Content read from file: \n{content}")
# Write data to the file
data_to_write = "This is the data to write to the file."
file_handler.write_file(oudata_to_write)
'''