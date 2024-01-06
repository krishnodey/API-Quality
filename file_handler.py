class FileReadWrite:
    def __init__(self, file_path):
        self.file_path = file_path

    def read_file(self, file_path=None):
        file_path = file_path if file_path else self.file_path
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                return content
        except FileNotFoundError:
            print(f"File '{file_path}' not found.")
            return None
        except Exception as e:
            print(f"Error reading file: {e}")
            return None

    def write_file(self, data, file_path=None):
        file_path = file_path if file_path else self.file_path
        try:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(data)
            #print(f"Data has been written to '{file_path}' successfully.")
        except Exception as e:
            print(f"Error writing to file: {e}")

    def write_data(self, ap_count, result_AP, p_count, result_P, selected, pattern_type):
        try:
            data_to_write = f"***Anti-Pattern*** \nCount: {ap_count}\n"
            for item in result_AP:
                data_to_write += item + "\n"
            data_to_write += f"\n***Patterns*** \nCount: {p_count}\n"
            for item in result_P:
                data_to_write += item + "\n"

            out_path = "Outputs/" + selected + "-" + pattern_type + "URI.txt"
            self.write_file(data_to_write, out_path)
        except Exception as e:
            print(f"Error writing AmorphousURI data to file: {e}")
