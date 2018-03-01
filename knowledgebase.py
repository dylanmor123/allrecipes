# This is a data structure with representing our knowledge base.

# NOTE 1: If you are adding new fields (e.g. name) make sure to
#   update all the relevant entries and try to make the field name
#   self explanatory.

# NOTE 2: Make sure the code is not broken after modifications! 
#   Make sure to check open and closing brackets

KNOWLEDGE_BASE = {
    "ingredients": [
        {
            "name": "milk",
            "sub-groups": [
                {
                    "name": "cow milk",
                    "vegan": "no",
                },
                {
                    "name": "soy milk",
                    "vegan": "yes",
                },
                {
                    "name": "rice milk",   
                    "vegan": "yes",
                },
                {
                    "name": "oat milk",
                    "vegan": "yes",
                },
            ]
        },
    ],
    "tools": [
        {
            "name": "pot",
        },
    ],
    "methods": [
        {
            "name": "Baking",
            "sub-groups": [
                {
                    "name": "Shirring",
                },
            ],
            "Dry": "yes",
        }, 
        {
            "name": "Broiling",
            "Dry": "yes",
        },
        {
            "name": "Frying",
            "sub-groups": [
                {
                    "name": "Deep fat frying",
                },
                {
                    "name": "Sautéing",
                },
                {
                    "name": "Stir-Frying",
                },
                {
                    "name": "Deglazing",
                },
            ],
            "Dry": "yes",
        },
        {
            "name": "Grilling",
            "Dry": "yes",
        },
        {
            "name": "Bain-marie",
            "Wet": "yes",
        },
        {
            "name": "Basting",
            "Wet": "yes",
        },
        {
            "name": "Blanching",
            "Wet": "yes",
        },
        {
            "name": "Boiling",
            "Wet": "yes",
        },
        {
            "name": "Clay pot cooking",
            "Wet": "yes",
        },
        {
            "name": "Poaching",
            "Wet": "yes",
        },
        {
            "name": "Pressure cooking",
            "Wet": "yes",
        },
        {
            "name": "Scalding",
            "Wet": "yes",
        },
        {
            "name": "Simmering",
            "Wet": "yes",
        },
        {
            "name": "Sous-vide",
            "Wet": "yes",
        },
        {
            "name": "Steaming",
            "Wet": "yes",
        },
        {
            "name": "Stewing",
            "Wet": "yes",
        },
        {
            "name": "Tempering",
            "Wet": "yes",
        },
        {
            "name": "Thermal Cooking",
            "Wet": "yes",
        },
        {
            "name": "Caramelizing",
            "Wet": "yes",
        },
    ],
}

print(KNOWLEDGE_BASE)