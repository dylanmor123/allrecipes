# This is a data structure with representing our knowledge base.

# NOTE: If you are adding a new fields (e.g. name) make sure to
#   update all the relevant entries and try to make the field name
#   self explanatory.

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
            "name": "Sauté",
            "description": 
        },    
    ],
}