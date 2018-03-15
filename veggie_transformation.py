from knowledgebase import *
from random import *
import re
from collections import defaultdict
import pprint
import copy

from recipe_parser import parse_ingredients, quantity_str_to_float, parse_recipe, get_match_maybe_plural_noun_in_sentence_regex
from allrecipes_scraper import create_recipe_data
from cooking_method_parser import parse_cooking_methods, get_main_cooking_method
from pretty_output import generate_html_page


def best_substitute_ingredient(recipe, substitute_subtree):
	substitute_for_cooking_method = getKBSubtree([".*", "if-main-cooking-method", recipe["cooking method"]], kb_subtree=substitute_subtree, regex=True)
	if substitute_for_cooking_method is not None: 
		return substitute_for_cooking_method
	return substitute_subtree

def from_veggie_to_non_veggie_recipe(recipe):
	# TODO: remove 
	remove_list = ["non-dairy ", "vegan ", "dairy-free ", "dairy free ", "whole wheat "]
	for remove_word in remove_list:
		for ingredient in recipe["ingredients"]:
			if remove_word in ingredient["name"]:
				print("remove ", remove_word, " from ingredient", ingredient["name"])
			ingredient["name"] = ingredient["name"].replace(remove_word, "")

		for idx, direction in enumerate(recipe["directions"]):
			if remove_word in direction:
				print("remove ", remove_word, " from direction ", idx)
			recipe["directions"][idx] = recipe["directions"][idx].replace(remove_word, "")

	# apply the same transformation as to veggie, but with inverse list of substitutions.
	return to_veggie_recipe(recipe, getKBSubtree(["substitutes", "from_vegan"]))

def to_veggie_recipe(recipe, vegan_subtree = getKBSubtree(["substitutes", "vegan"])):
	#TODO: get more ingredients that are non-vegan. consider that ingredients are are complex: e.g. croissant
	#TODO: change the quantity and measurement of the ingredient when necessary. e.g. 4 eggs -> 292g tofu
	#TODO: sometimes remove the steps that are associated with the ingredient: 
	# 	   e.g. " Crack an egg into a small bowl and gently slip the egg into the simmering [...] Poach the
	#		   eggs until the whites are firm and the yolks have thickened but are not hard [...]"
	#TODO: do not change any ingredient that has the word vegan or vegetarian or veggie
	#TODO: get best substitute based on the role of the ingredient. Not just the first match.
	#TODO: sometimes the ingredient is referenced differently. e.g. in ingredients "mascarpone cheese"
	# 	   gets replaces by "crumbled tofu", but it is not replaced in the directions because only says "mascarpone".
	#TODO: for chicken parmesan eggplant is a better substitute than tofu according to TA.
	#TODO: make sure we change the cooking method / verb associated with ingredients in the direction.

	ingredients_remove_words = defaultdict(lambda: [])

	for ingredient in recipe["ingredients"]:
		for non_veg, substitute_subtree in vegan_subtree.items():

			substitute_subtree = best_substitute_ingredient(recipe, substitute_subtree)
			substitute = list(substitute_subtree.keys())[0]
			non_veg_re = re.compile(re.escape(non_veg), re.IGNORECASE)

			if non_veg_re.search(ingredient["name"]) is not None:

				# Update the list of words we might want to remove from directios.
				for remove_word in ingredient["name"].split():
						remove_word = remove_word.lower()
						matched_list = [remove_word for word in non_veg.split() if word in remove_word]
						if len(matched_list) == 0:
							ingredients_remove_words[non_veg].append(remove_word)

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

	# remove duplucates:
	new_ingredients = []
	for old_ingredient in recipe["ingredients"]:
		repeated = False
		for new_ingredient in new_ingredients:
			if old_ingredient["name"] == new_ingredient["name"] and old_ingredient["measurement"] == new_ingredient["measurement"] and old_ingredient["preparation"] == new_ingredient["preparation"]:
				new_ingredient["quantity"] = str(quantity_str_to_float(old_ingredient["quantity"]) + quantity_str_to_float(new_ingredient["quantity"]))
				repeated = True
				break
		if not repeated:
			new_ingredients.append(old_ingredient)

	recipe["ingredients"] = new_ingredients

	print("ingredients_remove_words -> ", dict(ingredients_remove_words))

	for idx, direction in enumerate(recipe["directions"]):
		new_sentences = [] 
		for sentence in direction.split("."):
			substitutes = []
			for non_veg, substitute_subtree in vegan_subtree.items():
				substitute_subtree = best_substitute_ingredient(recipe, substitute_subtree)
				substitute = list(substitute_subtree.keys())[0]
				non_veg_re = re.compile(re.escape(non_veg), re.IGNORECASE)

				if len(non_veg_re.findall(sentence)):
					print("direction", idx, ": ", end="")
					print(non_veg, " -> ", substitute)

					# remove the words found in the ingredients that are too specific.
					# for example, if ingredient is "monterey jack cheese" and non_veg is "cheese", 
					# will remove "monterey" and "cheese" from sentence.
					for remove_word in ingredients_remove_words[non_veg]:
						# use regex to dial with plural.
						sentence = re.compile(get_match_maybe_plural_noun_in_sentence_regex(
							re.escape(remove_word)), re.IGNORECASE).sub(" ", sentence)

					# use temp_substitute to avoid further substitution in this word. 
					# otherwise the folowing tranformation could happen: 
					# 	"parmesan cheese" -> "vegan parmesan cheese" -> "vegan parmesan tofu"
					temp_substitute = str(randint(10000000000, 90000000000))
					substitutes.append((temp_substitute, substitute))
					sentence = non_veg_re.sub(temp_substitute, sentence)

			for temp_substitute, substitute in substitutes:
				sentence = sentence.replace(temp_substitute, substitute)

			new_sentences.append(sentence)			

		recipe["directions"][idx] = ".".join(new_sentences)

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

	url = 'https://www.allrecipes.com/recipe/222399/smoked-salmon-dill-eggs-benedict/?internalSource=hub%20recipe&referringContentType=search%20results&clickId=cardslot%2014'
	recipe = parse_recipe(create_recipe_data(url))

	subtree = getKBSubtree(['cooking-methods'])
	cooking_methods = ' '.join(list(subtree.keys()))
	parsed_methods = parse_cooking_methods(recipe['directions'], recipe['cooktimes'], cooking_methods)
	recipe["cooking method"] = get_main_cooking_method(parsed_methods, recipe) 
	print("cooking method = ", recipe["cooking method"])

	print("ingredients = ", recipe["ingredients"])
	print("directions = ", recipe["directions"])
	pprint.pprint(recipe["sentences"])

	print("\n=======================")
	old_recipe = copy.deepcopy(recipe)
	recipe = to_veggie_recipe(recipe)
	print("=======================\n")

	print("ingredients = ", recipe["ingredients"])
	print("directions = ", recipe["directions"])

	generate_html_page(recipe, old_recipe)

if __name__ == "__main__":
	main()