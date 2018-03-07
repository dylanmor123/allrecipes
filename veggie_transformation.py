from knowledgebase import *
import re

from recipe_parser import parse_ingredients

def to_veggie_recipe(recipe):
	#TODO: get more ingredients that are non-vegan. consider that ingredients are are complex: e.g. croa
	#TODO: change the quantity and measurement of the ingredient when necessary. e.g. 4 eggs -> 292g tofu
	#TODO: sometimes remove the steps that are associated with the ingredient: 
	# 	e.g. " Crack an egg into a small bowl and gently slip the egg into the simmering [...] Poach the
	#		   eggs until the whites are firm and the yolks have thickened but are not hard [...]"
	#TODO: do not change any ingredient that has the word vegan or vegetarian or veggie

	vegan_subtree = getKBSubtree(["substitutes", "vegan"])

	for ingredient in recipe["ingredients"]:
		for non_veg, substitute in vegan_subtree.items():
			substitute = list(substitute.keys())[0]
			if non_veg in ingredient["name"]:
				# TODO: get best substitute based on the role of the ingredient. Not just the first match.			
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


def main():
	vegan_subtree = getKBSubtree(["substitutes", "vegan"])

	content = ""
	with open("chinese_recipes.txt", mode="r", encoding="utf-8") as f:
	    content = f.readlines()

	ingredients = set()
	for line in content:
		recipe = eval(line)
		recipe["ingredients"] = parse_ingredients(recipe["ingredients"])


		for x in recipe["ingredients"]:
			ingredients.add(x["name"])

	for x in ingredients:
		print(x)
		for non_veg, substitute in vegan_subtree.items():
			substitute = list(substitute.keys())[0]
			if non_veg in x:
				print("##### substitutes for ", x, " -> ", substitute)
				print()	

if __name__ == "__main__":
	main()