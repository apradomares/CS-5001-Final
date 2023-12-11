import os
import json
from rich import print
from rich import pretty
from rich.console import Console
from rich.traceback import install

# Change directory
'''
new_directory = r"C:\Users\aprad\Desktop\MSCS\5001\final\pets"
os.chdir(new_directory)
'''

# RICH setup
pretty.install()
install(show_locals=True)

# Class
class Pet:
    """
    Class: Pet

    Attributes:
        name (str): Pet species.
        sizes (list): Standard size of the pet.
        complexity (str): The skill required to care for the pet.
        cost (list): Expected cost of raising pet.
        lifespan (list): Lifespan range.
        food (str): Food required to feed pet.

    Methods:
        __init__: Creates a new pet with all of the previous attributes.
        display_info: Displays information about the pet, info taken from the dictionary.
    """
    def __init__(self, name, sizes: list, complexity: list, cost, lifespan: list, food):
        self.name = name
        self.sizes = sizes
        self.complexity = complexity
        self.cost = cost
        self.lifespan = lifespan
        self.food = food

    def display_info(self):
        """
        Function to display information about the pet.
        """
        info = (
            f"[bold]Information about {self.name.title()}:[/bold]\n"
            f"Size: [green]{self.sizes}[/green]\n"
            f"Complexity: [yellow]{self.complexity}[/yellow]\n"
            f"Cost: [blue]{self.cost}[/blue]\n"
            f"Expected Lifespan: [magenta]{self.lifespan}[/magenta]\n"
            f"Food: [cyan]{self.food}[/cyan]\n"
        )
        print(info)
        return info


# FIRST MAJOR BLOCK - creates dictionary of pets, adds pets to dict, remove pets from dict
def create_pet_dictionary(filename: str):
    """
    Reads pet data from a json file and creates a dictionary of Pet objects.
    Each pet in the file is set up like this:
    "betta fish": {
        "name": "betta fish",
        "sizes": [
            "small"
        ],
        "complexity": "beginner",
        "cost": [
            "cheap"
        ],
        "lifespan": [
            "short"
        ],
        "food": "fish flakes"
    },

    Args:
        filename (str): The name of the file to load the pets from.

    Returns:
        dict: A dictionary where each key is a pet's species and each value is a Pet object.
    """
    pet_dictionary = {}
    dictionary_file = open(filename, 'r')
    data = json.load(dictionary_file)

    for key, pet_data in data.items():
        name = pet_data['name']
        sizes = pet_data['sizes']
        complexity = pet_data['complexity']
        cost = pet_data['cost']
        lifespan = pet_data['lifespan']
        food = pet_data['food']

        pet_dictionary[key] = Pet(name, sizes, complexity, cost, lifespan, food)

    dictionary_file.close()
    return pet_dictionary


def add_new_pet(filename: str):
    """
    When the user adds a new pet to the database file through the main menu of options they are redirected here.
    Here, there are more input requests where the user names the new pet and this is set up as the key, if the pet already exists
    then they are prompted to name it something else.
    Then the function asks the user to input the characteristics of each pet, first its size, then complexity, cost, lifespan, and food.
    All attributes but food are checked to make sure they are valid and from the pre-selected options available, so for size they can only
    be small, medium, large - not tiny or giant. They can leave this section at any point. All this info is compiled together.
    Then the compiled pet info is added to the database stored in the JSON file.
    Lastly, they get the prompt to write and extended info blurb that is stored as a text file if they wish to and get redirected there.

    Args:
        filename (str): The JSON file where the database is stored.

    Returns:
        None: No value is returned, the databased is updated and the user is redirected somewhere else depending on choices.
    """
    print("Add a new pet to the database (type 'exit' at any point to cancel):")

    file = open(filename, 'r')
    pet_dictionary = json.load(file)
    file.close()

    # Here user adds every characteristic of the pet, alt they leave in the process
    pet_name = input("Enter the name of the new pet: ").lower()
    if pet_name == 'exit':
        return

    # Check if pet already exists in the dictionaryc
    if pet_name in pet_dictionary:
        print(f"The pet '{pet_name.title()}' already exists in the database. Please try a different name or type 'exit'.")
        return

    valid_sizes = ['small', 'medium', 'large']
    sizes = get_valid_input("Enter sizes (small/medium/large): ", valid_sizes)
    if sizes == 'exit':
        return

    valid_complexities = ['beginner', 'intermediate', 'advanced']
    complexity = get_valid_input("Enter complexity (beginner/intermediate/advanced): ", valid_complexities)
    if complexity == 'exit':
        return

    valid_costs = ['cheap', 'moderate', 'expensive']
    cost = get_valid_input("Enter cost (cheap/moderate/expensive): ", valid_costs)
    if cost == 'exit':
        return

    valid_lifespans = ['short', 'medium', 'long']
    lifespan = get_valid_input("Enter lifespan (short/medium/long): ", valid_lifespans)
    if lifespan == 'exit':
        return

    food = input("Enter food: ")
    if food == 'exit':
        return

    new_pet_data = {
        "name": pet_name,
        "sizes": [sizes],
        "complexity": complexity,
        "cost": [cost],
        "lifespan": [lifespan],
        "food": food
    }

    # Add new pet to dictionary
    pet_dictionary[pet_name] = new_pet_data

    # Pet is written onto file
    file = open(filename, 'w')
    json.dump(pet_dictionary, file, indent=4)
    file.close()

    print(f"{pet_name.title()} has been added to the database.")

    # prompt for extended info
    extended_info_choice = get_valid_input("Do you want to upload extended information for this pet now? (yes/no): ", ['yes', 'no'])
    if extended_info_choice == 'yes':
        upload_extended_info(pet_name)


def remove_pet(filename: str):
    """
    The opposite of add a pet, if a user would like to remove a pet from the database they are asked to specify which one (key) and
    then the selected pet is deleted. This function also deletes any extended file associated with that pet as well to not fill up the
    folder with unnecessary files.
    This works by directly modifying the JSON file that stores the keys and values.

    Args:
        filename (str): The JSON file where the database is stored.

    Returns:
        None: No value is returned, the databased is updated and the user is redirected to main.
    """

    print("Remove a pet from the database (type 'exit' to cancel):")

    # Open the file for reading
    file = open(filename, 'r')
    pet_dictionary = json.load(file)
    file.close()

    pet_name_to_delete = get_valid_input("Enter the name of the pet to remove: ", list(pet_dictionary.keys()))

    if pet_name_to_delete == 'exit':
        return

    if pet_name_to_delete not in pet_dictionary:
        print(f"The pet '{pet_name_to_delete}' does not exist in the database, please try again.")
        return

    del pet_dictionary[pet_name_to_delete]

    # Makes the changes to the actual json file
    file = open(filename, 'w')
    json.dump(pet_dictionary, file, indent=4)
    file.close()
    print(f"{pet_name_to_delete.title()} has been removed from the database.")

    # Deletes the extended info file as well for that pet if it exists
    extended_info_filename = pet_name_to_delete.lower() + "_exinfo.txt"
    if os.path.exists(extended_info_filename):
        os.remove(extended_info_filename)


# SECOND MAJOR BLOCK - read about the pets, see their dictionary summaries, also read their extended info if it exists (if it doesnt add one)
def check_pets(pet_dictionary):
    """
    This is where the dictionary gets used, the JSON file creates the dictionary which is then able to be perused by the user here.
    They type out the name of the pet they wish to view, get the summaries of their values/attributes and then get the prompt to view
    the file containing more extended information about their care.
    This function also has an option to save the displayed of their selected pet, if they want to save the info they get redirected there.
    Lastly, as a precaution, if the user previously created a pet and did not add an extended file on creation, they get the option to upload
    one here instead every time just in case they ever change their mind. This way they would not have re-create the pet all over again.

    Args:
        pet_dictionary (dict): The created dictionary from which each key is the pet's species/name and each value is its size/complexity/etc.

    Returns:
        None: No value is returned. This function prints out information and then also allows the user to save that info
    """
    print("\nChoose a pet to learn about:")
    for pet_name in pet_dictionary.keys():
        print(f"- {pet_name.title()}")

    pet_choice = get_valid_input("\nEnter your choice: ", list(pet_dictionary.keys())).lower()
    if pet_choice == "exit":
        return

    # After they select the pet, it is searched in the dictionary and displayed if it exist
    elif pet_choice in pet_dictionary:
        pet = pet_dictionary[pet_choice]
        basic_info = pet.display_info()

        extended_info = ""
        extended_info_choice = get_valid_input("Do you want to read extended information about this pet? (yes/no): ", ['yes', 'no'])
        if extended_info_choice == 'yes':
            extended_info = read_extended_info(pet_choice)

        # Combine dictionary and extended info, this is for the purpose of saving both the summary and the extended info together
        combined_info = basic_info + "\n" + extended_info

        # Asking to save information
        save_info_choice = get_valid_input("Do you want to save this information to a file? (yes/no): ", ['yes', 'no'])
        if save_info_choice == 'yes':
            save_info_to_file(combined_info)
    else:
        print("Invalid choice. Please try again.")


def read_extended_info(pet_name):
    """
    If the user previously requested to read the extended info on a certain pet, here that info is displayed by looking into a text
    file that has name_exinfo.txt name to it. If such file cannot be found, the user is prompted to add their own instead if they wish to.

    Args:
        pet_name (str): The name of the pet the user is trying to read more about

    Returns:
        extended_info (str): It prints out the text on the exinfo.txt file that the user requested
    """
    filename = pet_name.lower() + "_exinfo.txt"
    extended_info = ""

    try:
        file = open(filename, 'r')
        extended_info = file.read()
        file.close()
    except FileNotFoundError:
        print(f"No extended information file exists for {pet_name.title()}.")
        upload_choice = get_valid_input("Do you want to upload extended information for this pet now? (yes/no): ", ['yes', 'no'])
        if upload_choice == 'yes':
            upload_extended_info(pet_name)
            return read_extended_info(pet_name)
        else:
            extended_info = "No extended information available or uploaded."

    print(f"\nExtended Information for {pet_name.title()}:\n{extended_info}")
    return extended_info


def upload_extended_info(pet_name):
    """
    If the user wants to create an _exinfo.txt file either at pet creation or when searching later, this is where it is done.
    User inputs info line by line, once done they start a new line and only type 'DONE' in there.
    The text is saved as a file under the name of "pet_exinfo.txt" with pet being whatever species they named and created.

    Args:
        pet_name (str): The name of the pet for which extended information is being added.

    Returns:
        None: Nothing is returned, it only saves whatever the user inputted into a file
    """
    filename = pet_name.lower() + "_exinfo.txt"

    print("Enter the detailed information for this pet (type 'DONE' on a new line to finish):")
    info_lines = []
    while True:
        line = input()
        if line == 'DONE':
            break
        info_lines.append(line)

    file = open(filename, 'w')
    for line in info_lines:
        file.write(line + "\n")
    file.close()
    print(f"Extended information for {pet_name.title()} has been created.")


# THRID MAJOR BLOCK - misc function, sorting based on dictionary, saving any info on pets to your own file, and a validator for user input
def save_info_to_file(info):
    """
    If the user wishes to save the info they have gotten about a certain pet they like, they can do so here. It is saved to a text file
    they can name. If such file already exists, in case the user keeps looking at other pets, they can decide whether to overwrite it or to
    append to the file instead.

    Args:
        info (str): The info recieved by check_pets, this is the combined text info from the summary + extended file

    Returns:
        None: Nothing is returned. This function writes the information requested to a separate file
    """
    try:
        filename = input("Enter a file name to save to: ") + ".txt"

        if os.path.exists(filename):
            action = input(f"{filename} already exists. Append (a) or Overwrite (o)? ").lower()
            if action == 'a':
                mode = "a"
            elif action == 'o':
                mode = "w"
            else:
                print("Invalid choice. Not saving to file.")
                return
        else:
            mode = "w"

        file = open(filename, mode)
        file.write(info + "\n\n")
        file.close()
        print(f"Information saved to {filename}.")

    except PermissionError:
        print(f"Permission not granted, cannot access {filename}.")


def sort_pets_by_criteria(pet_dictionary):
    """
    This function lets the user view pets based on a criteria they set, the first criteria is to search which exact attribute
    they want to look (size/complexity/cost/lifespan) and the second criteria is for the specific value (small or intermediate or long...)
    It then looks for those parameters on the dictionary and displays the pets which have them.

    Args:
        pet_dictionary (dict): The created dictionary from which each key is the pet's species/name and each value is its size/complexity/etc.

    Returns:
        None: Nothing is returned. It just prints out the specific list the user looked for
    """
    criteria = get_valid_input("Sort by 'size', 'complexity', 'cost', or 'lifespan'? ", ['size', 'complexity', 'cost', 'lifespan']).lower()
    if criteria == 'exit':
        return

    valid_options = []
    if criteria == 'size':
        valid_options = ['small', 'medium', 'large']
    elif criteria == 'complexity':
        valid_options = ['beginner', 'intermediate', 'advanced']
    elif criteria == 'cost':
        valid_options = ['cheap', 'moderate', 'expensive']
    elif criteria == 'lifespan':
        valid_options = ['short', 'medium', 'long']

    secondary_criteria = get_valid_input(f"Choose a {criteria} ({'/'.join(valid_options)}): ", valid_options)
    if secondary_criteria == 'exit':
        return

    pet_list = []

    for pet_name, pet in pet_dictionary.items():
        if criteria == 'size' and secondary_criteria in pet.sizes:
            pet_list.append(pet_name)
        elif criteria == 'complexity' and pet.complexity == secondary_criteria:
            pet_list.append(pet_name)
        elif criteria == 'cost' and secondary_criteria in pet.cost:
            pet_list.append(pet_name)
        elif criteria == 'lifespan' and secondary_criteria in pet.lifespan:
            pet_list.append(pet_name)

    # if nothing was found this first block happens, else it gets printed out
    if not pet_list:
        print(f"No pets found with {criteria} '{secondary_criteria}'.")
    else:
        print(f"\nPets with {criteria} '{secondary_criteria}':")
        for pet_name in pet_list:
            print(pet_name.title())

    # Return to main menu or sort again
    sort_again = get_valid_input("Would you like to sort again? (yes/no): ", ['yes', 'no']).lower()
    if sort_again == 'yes':
        return sort_pets_by_criteria(pet_dictionary)
    else:
        return


def get_valid_input(prompt, valid_options):
    """
    This is a convinience function. A lot of the functions in this program rely on valid user input, this make sure the user inputs the
    right word. If they do not, they get told to choose one of the valid options instead.
    It works by making it so that whatever function redirected here, had a certain keywords that were deemed valid and attached in a variable
    when sent here. They are checked and if valid they are returned. If the user types exit, the word exit is returned which the original
    function has been set up to parse.

    Args:
        prompt (str): The orginal prompt message that was displayed to the user.
        valid_options (list): A list of valid input options that the user can choose from.

    Returns:
        user_input (str): The user's input if it is valid, or 'exit' if the user types 'exit'.
    """
    while True:
        try:
            user_input = input(prompt).lower()
            if user_input in valid_options:
                return user_input
            elif user_input == 'exit':
                return 'exit'
            else:
                print(f"Invalid input. Please choose from {valid_options}.")
        except ValueError as v:
            print("Error ", v , ". Please try again.")
        except TypeError as t:
            print("Error ", t , ". Please try again.")


def main():
    console = Console()
    dictionary_file = "pet_dictionary.json"
    pet_dictionary = create_pet_dictionary(dictionary_file)


    while True:
        console.print(" C - Choose a pet to learn about\n",
                "F - Filter pets by a specific attributes\n",
                "A - Add a new pet to the database\n",
                "R - Remove existing pet from the database\n",
                "Q - Quit", style="bold")
        choice = input("\nEnter your choice: ").upper()

        if choice == 'C':
            check_pets(pet_dictionary)
        elif choice == 'F':
            sort_pets_by_criteria(pet_dictionary)
        elif choice == 'A':
            add_new_pet(dictionary_file)
            pet_dictionary = create_pet_dictionary(dictionary_file)
        elif choice == 'R':
            remove_pet(dictionary_file)
            pet_dictionary = create_pet_dictionary(dictionary_file)
        elif choice == 'Q':
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
