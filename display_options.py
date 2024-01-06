from file_handler import FileReadWrite

#file_handler = FileReadWrite(path)
# Read from the file
#content = file_handler.read_file()

class APIChoice:
    def __init__(self, file_path):
        file = FileReadWrite(file_path)
        content = file.read_file()
        self.choices = content.split('\n')
        self.selected_choice = None

    def display_choices(self):
        print("Choose An API:")
        for index, choice in enumerate(self.choices, start=1):
            print(f"{index}. {choice}")

    def select_choice(self):
        self.display_choices()
        try:
            choice_index = int(input("Enter the number corresponding to your choice: ")) - 1
            if 0 <= choice_index < len(self.choices):
                self.selected_choice = self.choices[choice_index]
                #print(f"You selected: {self.selected_choice}")
            else:
                print("Invalid choice. Please enter a valid number.")
                self.select_choice()
        except ValueError:
            print("Invalid input. Please enter a number.")
            self.select_choice()

    def get_selected_choice(self):
        return self.selected_choice

'''
# Usage example:
if __name__ == "__main__":
    file_path = 'APIs/APIList.txt'  # Replace with your CSV file path
    api_choice = APIChoice(file_path)
    #api_choice.display_choices()
    api_choice.select_choice()
    selected = api_choice.get_selected_choice()
    print(f"Your selected choice is: {selected}")
'''