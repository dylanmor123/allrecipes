from knowledgebase import *

#def from_veggie_recipe(recipe):

def to_veggie_recipe(recipe):
	for ingredient in recipe["ingredients"]:
		name_index = 3
		for token in ingredient[name_index].split():
			# gettting the first substitute for now
			subtree = getKBSubtree(["substitutes", "vegan", ".*%s.*" % token], regex=True)
			if subtree is None:
				continue
			ingredient_substitute = list(subtree.keys())[0]
			print("substitutes for ", ingredient[name_index], " -> ", ingredient_substitute)
			
		# TODO(danilo): work on replacing the ingredients in the directions.
		# for direction in recipe["directions"]:
		# 	for idx, token in enumerate(direction.split()) :
		# 		subtree = getKBSubtree(["substitutes", "vegan", token])
		# 		if subtree is None:
		# 			continue
		# 		ingredient_substitute = list(subtree.keys())[0]
	return recipe