from knowledgebase import *

#def from_veggie_recipe(recipe):

def to_veggie_recipe(recipe):
	for ingredient in recipe["ingredients"]:
		for token in ingredient["name"].split():
			# gettting the first substitute for now
			ingredient_substitute = getKBSubtree(["substitutes", "vegan", "*%s*" % token], regex=True).keys()[0]
			ingredient["name"] = ingredient_substitute
		for direction in recipe["directions"]:
   			for idx, token in enumerate(direction.split()) :
   				ingredient_substitute = getKBSubtree(["substitutes", "vegan", "*%s*" % token], regex=True).keys()[0]