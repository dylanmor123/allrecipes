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
addToKB(["tools", "apple corer"])
addToKB(["tools", "apple cutter"])
addToKB(["tools", "baster"])
addToKB(["tools", "beanpot"])
addToKB(["tools", "biscuit cutter"])
addToKB(["tools", "biscuit press"])
addToKB(["tools", "blow torch"])
addToKB(["tools", "boil over preventer"])
addToKB(["tools", "bottle opener"])
addToKB(["tools", "bowl"])
addToKB(["tools", "bread knife"])
addToKB(["tools", "browning tray"])
addToKB(["tools", "butter curler"])
addToKB(["tools", "cake and pie server"])
addToKB(["tools", "cheese cutter"])
addToKB(["tools", "cheese knife"])
addToKB(["tools", "cheese slicer"])
addToKB(["tools", "cheesecloth"])
addToKB(["tools", "chef's knife"])
addToKB(["tools", "cherry pitter"])
addToKB(["tools", "chinois"])
addToKB(["tools", "clay pot"])
addToKB(["tools", "cleaver"])
addToKB(["tools", "colander"])
addToKB(["tools", "corkscrew"])
addToKB(["tools", "crab cracker"])
addToKB(["tools", "cutting board"])
addToKB(["tools", "dough scraper"])
addToKB(["tools", "edible tableware"])
addToKB(["tools", "egg piercer"])
addToKB(["tools", "egg poacher"])
addToKB(["tools", "egg separator"])
addToKB(["tools", "egg slicer"])
addToKB(["tools", "egg timer"])
addToKB(["tools", "fillet knife"])
addToKB(["tools", "fish scaler"])
addToKB(["tools", "fish slice"])
addToKB(["tools", "flour sifter"])
addToKB(["tools", "food mill"])
addToKB(["tools", "funnel"])
addToKB(["tools", "garlic press"])
addToKB(["tools", "grapefruit knife"])
addToKB(["tools", "grater"])
addToKB(["tools", "gravy strainer"])
addToKB(["tools", "herb chopper"])
addToKB(["tools", "honey dipper"])
addToKB(["tools", "ladle"])
addToKB(["tools", "lame"])
addToKB(["tools", "lemon reamer"])
addToKB(["tools", "lemon squeezer"])
addToKB(["tools", "lobster pick"])
addToKB(["tools", "mandoline"])
addToKB(["tools", "mated colander pot"])
addToKB(["tools", "measuring cup"])
addToKB(["tools", "measuring spoon"])
addToKB(["tools", "meat grinder"])
addToKB(["tools", "meat tenderiser"])
addToKB(["tools", "meat thermometer"])
addToKB(["tools", "melon baller"])
addToKB(["tools", "mezzaluna"])
addToKB(["tools", "microplane"])
addToKB(["tools", "mortar and pestle"])
addToKB(["tools", "nutcracker"])
addToKB(["tools", "nutmeg grater"])
addToKB(["tools", "oven glove"])
addToKB(["tools", "pastry bag"])
addToKB(["tools", "pastry blender"])
addToKB(["tools", "pastry brush"])
addToKB(["tools", "pastry wheel"])
addToKB(["tools", "peel"])
addToKB(["tools", "peeler"])
addToKB(["tools", "pepper mill"])
addToKB(["tools", "pie bird"])
addToKB(["tools", "pizza cutter"])
addToKB(["tools", "potato masher"])
addToKB(["tools", "potato ricer"])
addToKB(["tools", "pot-holder"])
addToKB(["tools", "poultry shears"])
addToKB(["tools", "roller docker"])
addToKB(["tools", "rolling pin"])
addToKB(["tools", "salt shaker"])
addToKB(["tools", "scales"])
addToKB(["tools", "scissors"])
addToKB(["tools", "scoop"])
addToKB(["tools", "sieve"])
addToKB(["tools", "slotted spoon"])
addToKB(["tools", "spatula"])
addToKB(["tools", "spider"])
addToKB(["tools", "sugar thermometer"])
addToKB(["tools", "tamis"])
addToKB(["tools", "tin opener"])
addToKB(["tools", "tomato knife"])
addToKB(["tools", "tongs"])
addToKB(["tools", "trussing needle"])
addToKB(["tools", "twine"])
addToKB(["tools", "whisk"])
addToKB(["tools", "wooden spoon"])
addToKB(["tools", "zester"])

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

####################################################################
### End of KB