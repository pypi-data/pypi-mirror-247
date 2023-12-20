# Turn a function into a module
"""
This is the “nester2023.py" module, and it provides one function called
print_lol() which prints lists that may or may not include nested lists.
"""


# A module is simply a text file that contains Python code. The main requirement is that
# the name of the file needs to end in .py (here its nester2023.py):

# isinstance() BIF checks whether an identifier refers to a data object of some specified type.
def print_lol(nested_list):  # print list of list
    """This function takes a positional argument called 'nested_list', which is any
    Python list (of, possibly, nested lists). Each data item in the provided list
    is (recursively) printed to the screen on its own line."""
    for each_item in nested_list:
        if isinstance(each_item, list):
            print_lol(each_item)
        else:
            print(each_item)


