from collections import defaultdict

# This is a data structure with representing our knowledge base.

# NOTE 1: If you are adding new fields (e.g. name) make sure to
#   update all the relevant entries and try to make the field name
#   self explanatory.

# NOTE 2: Make sure the code is not broken after modifications! 
#   Make sure to check open and closing brackets

KNOWLEDGE_BASE = defaultdict(lambda: None)

# Adds information to the knowledge base (KB)
def addToKB(tuple):
    current_entry = KNOWLEDGE_BASE
    for i in range(len(tuple)):
        if current_entry[tuple[i]] is None:
            current_entry[tuple[i]] = defaultdict(lambda: None)
        current_entry = current_entry[tuple[i]]

def isInKB(tuple):
    current_entry = None
    for i in range(len(tuple)):
        if KNOWLEDGE_BASE[tuple[i]] is None:
            return False
        current_entry = KNOWLEDGE_BASE[tuple[i]]
    return True

def prettyPrintKBsubtree(subtree, level = 0):
    if subtree is not None:
        for key, value in subtree.items():
            print(level * 2 * " ", end='')
            if len(list(value.items())) == 0:
                print("'" + key + "': {}")
            else:
                print("'" + key + "': {")
                prettyPrintKBsubtree(value, level + 1)
                print(level * 2 * " ", end='')
                print("}")

####################################################################
### List of Ingredients
        
addToKB(["ingredients", "milk"])
addToKB(["ingredients", "meat"])
addToKB(["ingredients", "chicken"])
        
####################################################################
### List of Tools

addToKB(["tools", "pot"])

####################################################################
### List of cooking methods

### Dry methods
addToKB(["cooking-methods", "baking", "dry"])
addToKB(["cooking-methods", "shirring", "dry"])
addToKB(["cooking-methods", "broiling", "dry"])
addToKB(["cooking-methods", "frying", "dry"])
addToKB(["cooking-methods", "deep fat frying", "dry"])
addToKB(["cooking-methods", "sautéing", "dry"])
addToKB(["cooking-methods", "stir-frying", "dry"])
addToKB(["cooking-methods", "deglazing", "dry"])
addToKB(["cooking-methods", "grilling", "dry"])

### Wet methods
addToKB(["cooking-methods", "bain-marie", "wet"])
addToKB(["cooking-methods", "basting", "wet"])
addToKB(["cooking-methods", "blanching", "wet"])
addToKB(["cooking-methods", "boiling", "wet"])
addToKB(["cooking-methods", "clay pot cooking", "wet"])
addToKB(["cooking-methods", "poaching", "wet"])
addToKB(["cooking-methods", "pressure cooking", "wet"])
addToKB(["cooking-methods", "scalding", "wet"])
addToKB(["cooking-methods", "simmering", "wet"])
addToKB(["cooking-methods", "sous-vide", "wet"])
addToKB(["cooking-methods", "steaming", "wet"])
addToKB(["cooking-methods", "stewing", "wet"])
addToKB(["cooking-methods", "tempering", "wet"])
addToKB(["cooking-methods", "thermal cooking", "wet"])
addToKB(["cooking-methods", "caramelizing", "wet"])

####################################################################
### List of Transformations
        
### Vegan transformations
addToKB(["transformations", "vegan", "milk", "soy milk"])
addToKB(["transformations", "vegan", "milk", "rice milk"])
addToKB(["transformations", "vegan", "milk", "oat milk"])

### Healthy transformations

prettyPrintKBsubtree(KNOWLEDGE_BASE)