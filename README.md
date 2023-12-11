# Final Project Report

* Student Name: Andrea Prado
* Github Username: apradomares
* Semester: Fall 2023
* Course: CS 5001



## Description
General overview of the project, what you did, why you did it, etc.

##    
This project is based on the premise of creating a system where users can look at certain pets and learn about their fundamental characteristics, it would inform the user of their difficulty of care, their lifespan, their likely size and so on. It would also display a small blurb of extra info describing more relevant info about how to handle and care for them. User would be able to sort through the pets in case they want something small or perhaps cheap instead. They would also be able to add or remove pets from the database.
    
I did it because I enjoyed working with files and wanted to create something relating to them, extensively manipulating them and modifying them through coding. For the purposes of this project, the pet database from which the dictionary is created is a .json file because I found that it is much easier to manipulate and modify than a simple text file. However, I also did use text files for simple stuff like storing any information the user wants saved, or the extended information blurb that appears when requested.

## Key Features
Highlight some key features of this project that you want to show off/talk about/focus on.


##    
The main feature is the pet dictionary and database. All the pets created are stored in a JSON file where they can easily be modified, more pets can be added or removed. This file is then processed to become a dictionary from which another key feature, the sorting function is able to sort through the pets based on their values, the user can decide whether they want a specific type of pet. The dictionary itself and the class function are deeply interlinked. 

The Pet class I made is the blueprint of sorts that allow for the creation of these individual pet objects. The pet dictionary serves as a way to build up the Pet class as well, where each value is extracted from the dictionary and added to its respective Pet class in the location they are supposed to go. Lastly, I integrated some RICH into the project but did not have enough time to explore its full capabilities, what is there though enhances certain option, highlighting key words the user can use.

## Guide
How do we run your project? What should we do to see it in action? - Note this isn't installing, this is actual use of the project.. If it is a website, you can point towards the gui, use screenshots, etc talking about features.

##
It is a Python script, all text based, simply start it and select the choices pertinent to you based on the prompts. The script makes sure the user does not enter incorrect prompts and gives guidance if unsure of what to input.


## Installation Instructions
If we wanted to run this project locally, what would we need to do?  If we need to get API key's include that information, and also command line startup commands to execute the project. If you have a lot of dependencies, you can also include a requirements.txt file, but make sure to include that we need to run `pip install -r requirements.txt` or something similar.

## 
The only thing to install would be the rich library
    pip install rich
Other than that, there is some pre made files I have created that I will submit alongside that must be in the same folder. These are the pet_dictionary.json which has already some premade pets on it and serves as the database where all pets are stored, there is other minor text files for each pre made pet where their extended info is saved.

## Code Review
Go over key aspects of code in this section. Both link to the file, include snippets in this report (make sure to use the [coding blocks](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet#code)).  Grading wise, we are looking for that you understand your code and what you did.

```python
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
```

##
This first block in create_pet_dictionary builds up the core of the aforemented dictionary and Pet class relation. Here the dictionary retrieves info from the JSON file. There is the first key with the pet name on it and inside there are subkeys with values attached to them. For each item in the file, the key is the pet name then, pet_data looks for the spific value I want and assigns it to a variable of the same name. Once all values have been found and assigned a variable, they create a new Pet object and assigns it to the pet dictionary with the name of the pet as the key.

```python
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
```

##
This second block in add_new_pet is what led to the creation of get_valid_input. I needed a way for users to only select the choices I wanted them to make as to not create too many values in the dictionary and the Pet class, that way the sorting function would be much more navihable and not filled with dozens of redundant options (having small and smaller or something like that). I did this by making sure each input had a preselected list of valid option, which were then all sent together to the get_valid_input function together. 
Finally, what this function does is assign all the recieved user input into a smaller dicitonary which was then added to the bigger dictionary, the pet_name the user initially inputted becomes the key, and the collected data its values. This is then added to the JSON file, in main I have the dictionary refresh with this new pet once the add_new_pet function is done.

```python
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
        elif criteria == 'complexity' and secondary_criteria in pet.complexity:
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
```

##
The last major code snippet is the sorting function. It works by getting two criteria the user wants to sort by, first it asks for one of the keys in the nested dictionaries (size, complexity, cost, or lifespan). Once one of these is selected, it looks for the values of each of these keys as an available option (the pre existing values only such that for size only small/medium/large is valid). Once both are found, an empty pet list is created, if a pet with such value is found it is added to the list. For the actually filtering, we look at the existing pet objects and see if their respective sizes/complexity/cost/lifespan are found there. If so, it appends the name of the pet onto the empty pet list and then prints it out.


### Major Challenges
Key aspects could include pieces that your struggled on and/or pieces that you are proud of and want to show off.

##

Major challenge was setting up the dictionary and the JSON file that needed to be update every time the user added a new pet or removed one. Initially I used a text file for the dictionary as well but as my code got more complex when modying these, I found that JSON files were more suited to this task especially because the dump function had a lot of usability to it was easy to use when writting in the file as needed. I had the idea of making pets a class from the beginning which paired well with the dictionary, it was intially a challenge to rework the change from a text file to a JSON file as I had to make the first key the names of the pets, such that cat or dog were the first, then there is the nested keys and values within. These new keys are the attributes (name, sizes, complexity, cost, lifespan, food) and their values are the corresponing facet of the pet (for sizes these can be small, medium, or large).

Finally, the sorting function was also a major work that led to the creation of the input validator function as I wanted to make sure the user could only select from the available existing values in the dictionary. This worked in conjunction with the pet class which stored those attributes neatly and allowed the sorting to work.

## Example Runs
Explain how you documented running the project, and what we need to look for in your repository (text output from the project, small videos, links to videos on youtube of you running it, etc)

##
I kept running test where I tried out all functions as I went, whenever an error ocurred I took the time to see what was causing it and fixing it. In some cases it was when I tried to exit midway through something and the program didn't let me such as when I was adding a pet which led to more exit paths to be put in place. In other cases, the error was on the dictionary being read, before I put the indentation on the JSON file, all the keys and value would be squished into a single line leading to issue with it being read on a second run.

I was able to save one documentation of such exit error, but I began the process of filling out this too late so those others have been fixed already. I did attached a couple testing run text files where I tried out different pets and different inputs.

## Testing
How did you test your code? What did you do to make sure your code was correct? If you wrote unit tests, you can link to them here. If you did run tests, make sure you document them as text files, and include them in your submission.

##
I tested by running the program and trying all possible combinations of words until I recieved an error relating to a valid option not parsing properly or such. I have attached the runs where I tried out multiple things here like mentioned before as text files.

> _Make it easy for us to know you *ran the project* and *tested the project* before you submitted this report!_


## Missing Features / What's Next
Focus on what you didn't get to do, and what you would do if you had more time, or things you would implement in the future. 

##
Main thing is for when an user adds a new pet, I want them to be able to submit them as lists, only the premade pets have lists as their values in some cases (such as dogs falling on the small/medium/large category due to their variable sizes). Users can only select one of each value to add their pets as for practicality, in theory they could go to the JSON file and add more attributes there as a list once the barebones of the pet has been created but that is not within expectations. I would have like more time to implement that but I was afraid it would break apart too many functions when the base function was already working.

Another thing, I would like to implement RICH more in the future, I only had a brief amount of time to add modules I like that worked, and while they added some nice looks to the code, it could have been implemented much more strongly throughout. Lastly, I would have liked to add more methods to my Pet class since as it is it is pretty barebones, I was struggling to think of ways to make it more robust, in the future I would have liked to implement more of these such as updating already exiisting exisint objects rather than deleting old ones and creating new ones. Maybe I could have done something to compare pets more directly as well, but it probably have required the creeation of a separate function.

## Final Reflection
Write at least a paragraph about your experience in this course. What did you learn? What do you need to do to learn more? Key takeaways? etc.

##
I learnt a lot about the basics of coding, the set ups that looks kind of basic such as looping and recursiveness, that build up to create more complex and demanding code. At times it felt like I only learned the bare basics, which is technically the point, took a lot of self study and investment to see how they worked more deeply. I feel like I am still shaky on the foundations of how things work and how they connect to each other, it is really a problem that I think will go away with practice. Certaintly, during this project the repetition and new found familiarity with the creation of some functions made it much easier to create the others.

I believe learning which tool to use for each situation is the main thing I need to learn more about, at times I was not using the right file format or the right loop which led to overly complicated code that would have been much easier to do had I known from the beginning which to use. It led to a couple rewrites and frustation that could have been avoided had I taken the time to think more deeply about the problem. I certaintly will put more thought in making one of the graphs to path my code.

Overall, I feel I am better a recognizing what the code does and why, even when it works and I do not understand why I can take the time to examine each line and understand. I certaintly need more practice though, because I had heard it was like learning a language before, but doing it in practice certaintly made it apparant. There are patterns to how everything works, lines of code that while different, are quite similar in terms of what they ultimately seek to do.
