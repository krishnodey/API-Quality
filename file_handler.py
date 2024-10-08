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
        
    def read_data(self, file_path=None):
        file_path = file_path if file_path else self.file_path
        try:
            data = []
            with open(file_path, 'r') as file:
                for line in file:
                    data.append(line)
                return data
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

    # def write_data(self, result_AP, result_P, p_count, ap_count, selected, pattern_type, base_path):
    #     try:
    #         data_to_write = f"***Anti-Pattern*** \nCount: {ap_count}\n"
    #         for item in result_AP:
    #             data_to_write += item + "\n"
    #         data_to_write += f"\n***Patterns*** \nCount: {p_count}\n"
    #         for item in result_P:
    #             data_to_write += item + "\n"

    #         out_path = f"Outputs-{base_path}/{selected}-{pattern_type}.txt"
    #         self.write_file(data_to_write, out_path)
    #     except Exception as e:
    #         print(f"Error writing AmorphousURI data to file: {e}")

    # def write_out_data(self, result, selected, pattern_type, base_path):
    #     try:
    #         api_type = 'REST-' if 'REST-API' in base_path else 'GraphQL-'
    #         data_to_write = ""
    #         for item in result:
    #             data_to_write += item + "\n"
    #         out_path = f"Out_All/{api_type}{selected}-{pattern_type}.txt"
    #         self.write_file(data_to_write, out_path)
    #     except Exception as e:
    #         print(f"Error writing AmorphousURI data to file: {e}")

