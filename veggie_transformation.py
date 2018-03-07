from knowledgebase import *

#def from_veggie_recipe(recipe):

def to_veggie_recipe(recipe):

	vegan_subtree = getKBSubtree(["substitutes", "vegan"])
	
	for non_veg, substitute in vegan_subtree


	for ingredient in recipe["ingredients"]:
		ingredient_substitute = None
		for token in ingredient["name"].split():
			# gettting the first substitute for now
			subtree = getKBSubtree(["substitutes", "vegan", ".*%s.*" % token], regex=True)
			if subtree is None:
				continue

			ingredient_substitute = list(subtree.keys())[0]
			print("substitutes for ", ingredient["name"], " -> ", ingredient_substitute)
			break
			
		if ingredient_substitute is not None:
			ingredient["name"] = ingredient_substitute
			
		# TODO(danilo): work on replacing the ingredients in the directions.
		for direction in recipe["directions"]:
			for idx, token in enumerate(direction.split()) :
				subtree = getKBSubtree(["substitutes", "vegan", token.lower()])
				if subtree is None:
					continue
				ingredient_substitute = list(subtree.keys())[0]
	return recipe

############################
## OLD METHOD

# def to_veggie_recipe(recipe):
# 	for ingredient in recipe["ingredients"]:
# 		ingredient_substitute = None
# 		for token in ingredient["name"].split():
# 			# gettting the first substitute for now
# 			subtree = getKBSubtree(["substitutes", "vegan", ".*%s.*" % token], regex=True)
# 			if subtree is None:
# 				continue
# 			ingredient_substitute = list(subtree.keys())[0]
# 			print("substitutes for ", ingredient["name"], " -> ", ingredient_substitute)
# 			break
# 		if ingredient_substitute is not None:
# 			ingredient["name"] = ingredient_substitute
# 		# TODO(danilo): work on replacing the ingredients in the directions.
# 		for direction in recipe["directions"]:
# 			for idx, token in enumerate(direction.split()) :
# 				subtree = getKBSubtree(["substitutes", "vegan", token.lower()])
# 				if subtree is None:
# 					continue
# 				ingredient_substitute = list(subtree.keys())[0]
# 	return recipe