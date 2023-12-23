# Turn a function into a module
"""
This is the “nester2023.py" module, and it provides one function called
print_lol() which prints lists that may or may not include nested lists.
"""


# A module is simply a text file that contains Python code. The main requirement is that
# the name of the file needs to end in .py (here its nester2023.py):

# isinstance() BIF checks whether an identifier refers to a data object of some specified type.
def print_lol(nested_list, level):  # print list of list
    """This function takes a positional argument called 'nested_list', which is any
    Python list (of, possibly, nested lists). Each data item in the provided list
    is (recursively) printed to the screen on its own line.
    A second argument "level" is used to insert tab-stops when a nested list is encountered."""
    for each_item in nested_list:
        if isinstance(each_item, list):
            print_lol(each_item, level+1)  # increment the value of level by 1 each time you recursively invoke your fun
        else:
            for tab_stops in range(level):  # use the value of "level" to control how many tab-stops are used.
                print("\t", end=" ")  # Display a TAB character for each level of indentation.
            print(each_item)


