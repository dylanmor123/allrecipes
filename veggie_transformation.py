from knowledgebase import *
from random import *
import re

from recipe_parser import parse_ingredients, quantity_str_to_float
from allrecipes_scraper import create_recipe_data
from cooking_method_parser import parse_cooking_methods, get_main_cooking_method

def best_substitute_ingredient(recipe, substitute_subtree):
	substitute_for_cooking_method = getKBSubtree([".*", "if-main-cooking-method", recipe["cooking method"]], kb_subtree=substitute_subtree, regex=True)
	if substitute_for_cooking_method is not None: 
		return substitute_for_cooking_method
	return substitute_subtree

def to_veggie_recipe(recipe):
	#TODO: get more ingredients that are non-vegan. consider that ingredients are are complex: e.g. croissant
	#TODO: change the quantity and measurement of the ingredient when necessary. e.g. 4 eggs -> 292g tofu
	#TODO: sometimes remove the steps that are associated with the ingredient: 
	# 	   e.g. " Crack an egg into a small bowl and gently slip the egg into the simmering [...] Poach the
	#		   eggs until the whites are firm and the yolks have thickened but are not hard [...]"
	#TODO: do not change any ingredient that has the word vegan or vegetarian or veggie
	#TODO: get best substitute based on the role of the ingredient. Not just the first match.
	#TODO: sometimes the ingredient is referenced differently. e.g. in ingredients "mascarpone cheese"
	# 	   gets replaces by "crumbled tofu", but it is not replaced in the directions because only says "mascarpone".

	vegan_subtree = getKBSubtree(["substitutes", "vegan"])

	for ingredient in recipe["ingredients"]:
		for non_veg, substitute_subtree in vegan_subtree.items():
			substitute_subtree = best_substitute_ingredient(recipe, substitute_subtree)
			substitute = list(substitute_subtree.keys())[0]
			non_veg_re = re.compile(re.escape(non_veg), re.IGNORECASE)

			if non_veg_re.search(ingredient["name"]) is not None:
				# TODO: get best substitute based on the role of the ingredient. Not just the first match.			
				print("substitutes for ", ingredient["name"], " -> ", substitute)
				ingredient["name"] = substitute

				for field in ["quantity", "measurement", "preparation"]:
					kb_field = (field + "_change")

				# TODO: maybe put that outside in a separate method.
				if "measurement_change" in substitute_subtree[substitute].keys():
					ingredient["measurement"] = list(substitute_subtree[substitute]["measurement_change"].keys())[0]

				if "preparation_change" in substitute_subtree[substitute].keys():
					ingredient["preparation"] = list(substitute_subtree[substitute]["preparation_change"].keys())[0]

				if "quantity_change" in substitute_subtree[substitute].keys():
					# has to multiply by the old quantity (e.g. 3 eggs to 3 * 1.4 oz tofu)
					ingredient["quantity"] = str(quantity_str_to_float(ingredient["quantity"]) * float(list(substitute_subtree[substitute]["quantity_change"].keys())[0]))

				break

	for idx, direction in enumerate(recipe["directions"]):

		substitutes = []
		for non_veg, substitute_subtree in vegan_subtree.items():
			substitute_subtree = best_substitute_ingredient(recipe, substitute_subtree)
			substitute = list(substitute_subtree.keys())[0]
			non_veg_re = re.compile(re.escape(non_veg), re.IGNORECASE)

			if len(non_veg_re.findall(direction)):
				print("direction", idx, ": ", end="")
				print(non_veg, " -> ", substitute )

				# use temp_substitute to avoid further substitution in this word. 
				# otherwise "vegan parmesan cheese" wouold become "vegan parmesan tofu"
				temp_substitute = str(randint(10000000000, 90000000000))
				substitutes.append((temp_substitute, substitute))
				direction = non_veg_re.sub(temp_substitute, direction)

		for temp_substitute, substitute in substitutes:
			direction = direction.replace(temp_substitute, substitute)

		recipe["directions"][idx] = direction

	return recipe

# This is here just for testing.
def test_ingredient_substitute():
	ingredients_subtree = getKBSubtree(["ingredients"])
	vegan_subtree = getKBSubtree(["substitutes", "vegan"])

	content = ""
	with open("chinese_recipes.txt", mode="r", encoding="utf-8") as f:
	    content = f.readlines()

	ingredients = set()
	for line in content:
		recipe = eval(line)

		for x in recipe["ingredients"]:
			ingredients.add(x["name"])

	for x in ingredients:
		print(x, end='')
		for kb_igredient in ingredients_subtree.keys():
			kb_igredient_re = re.compile(re.escape(kb_igredient), re.IGNORECASE)
			if kb_igredient_re.search(x) is not None:
				print(" -> ", kb_igredient, end='')
		print()
		for non_veg, substitute in vegan_subtree.items():
			substitute = list(substitute.keys())[0]
			if non_veg in x:
				print("##### substitutes for ", x, " -> ", substitute)
				


def main():
	# test_ingredient_substitute()

	url = 'https://www.allrecipes.com/recipe/7565/too-much-chocolate-cake/?internalSource=hub%20recipe&referringContentType=search%20results&clickId=cardslot%202'
	recipe = create_recipe_data(url)

	subtree = getKBSubtree(['cooking-methods'])
	cooking_methods = ' '.join(list(subtree.keys()))
	parsed_methods = parse_cooking_methods(recipe['directions'], recipe['cooktimes'], cooking_methods)
	recipe["cooking method"] = get_main_cooking_method(parsed_methods, recipe) 
	print("cooking method = ", recipe["cooking method"])


	print("ingredients = ", recipe["ingredients"])
	print("directions = ", recipe["directions"])

	print("\n=======================")
	recipe = to_veggie_recipe(recipe)
	print("=======================\n")

	print("ingredients = ", recipe["ingredients"])
	print("directions = ", recipe["directions"])

if __name__ == "__main__":
	main()