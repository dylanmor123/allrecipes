from knowledgebase import *
import re

def to_veggie_recipe(recipe):
	#TODO: get more ingredients that are non-vegan. consider that ingredients are are complex: e.g. croa
	#TODO: change the quantity and measurement of the ingredient when necessary. e.g. 4 eggs -> 292g tofu
	#TODO: sometimes remove the steps that are associated with the ingredient: 
	# 	e.g. " Crack an egg into a small bowl and gently slip the egg into the simmering [...] Poach the
	#		   eggs until the whites are firm and the yolks have thickened but are not hard [...]"

	vegan_subtree = getKBSubtree(["substitutes", "vegan"])

	for ingredient in recipe["ingredients"]:
		for non_veg, substitute in vegan_subtree.items():
			substitute = list(substitute.keys())[0]
			if non_veg in ingredient["name"]:
				# TODO: get best substitute based on the role of the ingredient. Not just the last match.			
				print("substitutes for ", ingredient["name"], " -> ", substitute)
				ingredient["name"] = substitute
				break

	for idx, direction in enumerate(recipe["directions"]):
		for non_veg, substitute in vegan_subtree.items():
			substitute = list(substitute.keys())[0]

			# TODO: get best substitute based on the role of the ingredient. Not just the last match.
			direction = direction.replace(non_veg, substitute)

			if non_veg in direction:
				print(idx)
				print(non_veg, " -> ", substitute )
				print()

		recipe["directions"][idx] = direction

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