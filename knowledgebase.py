import json
import re

# This is a data structure with representing our knowledge base.
# NOTE: If you are adding new entries try to make the field name
#   self explanatory.
KNOWLEDGE_BASE = {}

# Set this to true if you are adding new data to the KB.
TESTING_KNOWLEDGE_BASE = False

# Adds information to the knowledge base (KB)
# Args - 
#   tuple: list of string 
#   kb_subtree (optional): a defaultdict that represents a KB tree  
def addToKB(tuple, kb_subtree = KNOWLEDGE_BASE):
    current_entry = kb_subtree
    for i in range(len(tuple)):
        if not tuple[i] in current_entry:
            current_entry[tuple[i]] = {}
        current_entry = current_entry[tuple[i]]

# Verifies if tuple is in knowledge base (KB)
# Args - 
#   tuple: list of string
#   kb_subtree (optional): a defaultdict that represents a KB tree
#   regex (optional): boolean value, if true will match the keys in the
#       dictionary using regex.
# Returns -
#   True if tuple is part of the KB.
def isInKB(tuple, kb_subtree = KNOWLEDGE_BASE, regex = False):
    return getKBSubtree(tuple, kb_subtree, regex) is not None

# Gets a subtree of the knowledge base associated with the tuple.
# E.g. running getKBSubtree(["ingredients"]]) will return a defaultdict
# where the list of keys are ingredients.
# Args - 
#   tuple: list of string
#   kb_subtree (optional): a defaultdict that represents a KB tree
#   regex (optional): boolean value, if true will match the keys in the
#       dictionary using regex. If more than one key matches the regex,
#       will return the first match.   
# Returns -
#   A dict that is a subtree of the KB or None if not present.
def getKBSubtree(tuple, kb_subtree = KNOWLEDGE_BASE, regex=False):
    current_entry = kb_subtree
    for i in range(len(tuple)):
        if regex:
            for key in current_entry:
                if re.match(tuple[i], key) is None:
                    return None
                # TODO(danilo): we should consider returning all the subtrees
                # from here, or getting the most likely matching key.
                current_entry = current_entry[key]
                break
        else:
            if not tuple[i] in current_entry:
                return None
            current_entry = current_entry[tuple[i]]
    return current_entry

# Adds information to the knowledge base (KB)
# Args - 
#   knowledge_subtre (optional): a defaultdict that represents a KB tree
def prettyPrintKBsubtree(kb_subtree = KNOWLEDGE_BASE):
    print(json.dumps(kb_subtree, sort_keys=True, indent=4))

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
### List of substitutes
        
### Vegan substitutes
addToKB(["substitutes", "vegan", "meat", "veggie deli slice"])
addToKB(["substitutes", "vegan", "burger", "veggie burger"])
addToKB(["substitutes", "vegan", "meatball", "veggie meatball"])
addToKB(["substitutes", "vegan", "bacon", "veggie bacon"])
addToKB(["substitutes", "vegan", "chicken", "soy chicken patties"])
addToKB(["substitutes", "vegan", "chicken nuggets", "soy chicken nuggets"])
addToKB(["substitutes", "vegan", "jerky", "veggie jerky"])

addToKB(["substitutes", "vegan", "milk", "soy milk"])
addToKB(["substitutes", "vegan", "milk", "rice milk"])
addToKB(["substitutes", "vegan", "milk", "oat milk"])

addToKB(["substitutes", "vegan", "ice cream", "soy ice cream"])
addToKB(["substitutes", "vegan", "ice cream", "rice ice cream"])

addToKB(["substitutes", "vegan", "cheese", "tofu"])
addToKB(["substitutes", "vegan", "cheese", "crumbled tofu"])
addToKB(["substitutes", "vegan", "cheese", "soaked raw nuts"])
addToKB(["substitutes", "vegan", "parmesan cheese", "vegan parmesan cheese"])
addToKB(["substitutes", "vegan", "scrambled eggs", "tofu scramble"])

addToKB(["substitutes", "vegan", "baked eggs", "applesauce"])
addToKB(["substitutes", "vegan", "baked eggs", "pureed soft tofu"])
addToKB(["substitutes", "vegan", "baked eggs", "flax egg"])
addToKB(["substitutes", "vegan", "baked eggs", "mashed bananas"])

addToKB(["substitutes", "vegan", "binding eggs", "soy flour"])
addToKB(["substitutes", "vegan", "binding eggs", "bread crumbs"])
addToKB(["substitutes", "vegan", "binding eggs", "rolled oats"])

addToKB(["substitutes", "vegan", "chicken broth", "vegetable broth"])
addToKB(["substitutes", "vegan", "chicken stock", "vegetable broth"])
addToKB(["substitutes", "vegan", "beef broth", "vegetable broth"])
addToKB(["substitutes", "vegan", "beef stock", "vegetable broth"])

addToKB(["substitutes", "vegan", "butter", "margarine"])

addToKB(["substitutes", "vegan", "yogurt", "soy yogurt"])
addToKB(["substitutes", "vegan", "yogurt", "coconut yogurt"])
addToKB(["substitutes", "vegan", "yogurt", "almond yogurt"])

addToKB(["substitutes", "vegan", "sour cream", "vegan sour cream"])

addToKB(["substitutes", "vegan", "mayonnaise", "vegan mayonnaise"])

addToKB(["substitutes", "vegan", "gelatin", "agar flakes"])

addToKB(["substitutes", "vegan", "honey", "liquid sweetener"])

addToKB(["substitutes", "vegan", "chocolate", "non-dairy chocolate chips"])
addToKB(["substitutes", "vegan", "chocolate", "non-dairy cocoa powders"])

### Healthy substitutes

### End of KB
####################################################################

# Testing

if TESTING_KNOWLEDGE_BASE:
    print(isInKB(["ingredients", "milk"]))
    print(isInKB(["ingredients", "xx"]))
    print(isInKB(["cooking-methods", "baking"]))
    print(isInKB(["cooking-methods", "baking", "dry"]))
    print(isInKB(["cooking-methods", "baking", "wet"]))
    print(isInKB(["cooking-methods", "baking", "wet"]))
    print(isInKB(["cooking-methods", "baking", "wet"]))

    prettyPrintKBsubtree(kb_subtree = getKBSubtree(["cooking-methods"]))

    print("list of ingredients = ")
    print(list(getKBSubtree(["ingredients"]).keys()))