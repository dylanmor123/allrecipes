import re

from knowledgebase import *
from recipe_parser import parse_ingredients, quantity_str_to_float
from allrecipes_scraper import create_recipe_data

def words_not_in_kb():
	ingredients_subtree = getKBSubtree(["ingredients"])

	content = []
	for file in ["chinese_recipes.txt", "italian_recipes.txt", "low-carb_recipes.txt", "low-sodium_recipes.txt", "vegan_recipes.txt"]:
		print(file)
		with open(file, mode="r", encoding="utf-8", errors="ignore") as f:
			content = content + f.readlines()

	ingredients = set()
	for line in content:
		recipe = eval(line)

		if recipe is None or recipe["ingredients"] is None:
			continue

		for x in recipe["ingredients"]:
			ingredient = x[3] if not type(x) == type(dict()) else x["name"] 
			ingredient = ingredient.replace("(optional)", "").strip().lower()
			ingredients.add(ingredient)

	not_found = {}
	for x in ingredients:
		# print(x, end='')
		found = False
		for kb_igredient in ingredients_subtree.keys():
			x.replace("-", " ")
			if len(re.findall("(^| |\"|'|\()%s.?(s|es|ies|ing|ed|ied|x|en)?($| |,|\.|!|\"|'|;|\))" % (kb_igredient[:-1]), x, re.IGNORECASE)) > 0:
				# print(x, " -> ", kb_igredient)
				found = True
		if not found:
			for word in x.split():
			# for word_pair in zip(x.split()[:-1], x.split()[1:]):
			# 	word = word_pair[0] + " " + word_pair[1]
				if word in not_found:
					not_found[word] += 1
				else:
					not_found[word] = 1
		# print()

	print("\n==================n==================\n")
	
	top = sorted(list(not_found.items()), key= lambda x: x[1], reverse=True)
	print(top[:200])
	print("len = ", len(not_found))

def list_chinese_ingredients_from_kb():
	ingredients_subtree = getKBSubtree(["ingredients"])

	content = []
	for file in ["chinese_recipes.txt"]:
		print(file)
		with open(file, mode="r", encoding="utf-8", errors="ignore") as f:
			content = content + f.readlines()

	ingredients = set()
	for line in content:
		recipe = eval(line)

		if recipe is None or recipe["ingredients"] is None:
			continue

		for x in recipe["ingredients"]:
			ingredient = x[3] if not type(x) == type(dict()) else x["name"]
			ingredient.replace("(optional)", "").strip().lower()
			ingredients.add(ingredient)

	chinese_ingredients = []
	for x in ingredients:
		for kb_igredient in ingredients_subtree.keys():
			x = x.replace("-", " ")
			if len(re.findall(kb_igredient, x, re.IGNORECASE)) > 0:
				chinese_ingredients.append(kb_igredient)

	########################################################################################################################
	########################################################################################################################

	content = []
	for file in ["italian_recipes.txt"]:
		print(file)
		with open(file, mode="r", encoding="utf-8", errors="ignore") as f:
			content = content + f.readlines()

	ingredients = set()
	for line in content:
		recipe = eval(line)

		if recipe is None or recipe["ingredients"] is None:
			continue

		for x in recipe["ingredients"]:
			ingredient = x[3] if not type(x) == type(dict()) else x["name"]
			ingredient.replace("(optional)", "").strip().lower()
			ingredients.add(ingredient)

	italian_ingredients = []
	for x in ingredients:
		for kb_igredient in ingredients_subtree.keys():
			x = x.replace("-", " ")
			if len(re.findall("(^| |\"|'|\()%s.?(s|es|ies)?($| |,|\.|!|\"|'|;|\))" % (kb_igredient[:-1]), x, re.IGNORECASE)) > 0:
				italian_ingredients.append(kb_igredient)

	########################################################################################################################
	########################################################################################################################

	# content = []
	# for file in ["indian_recipes.txt"]:
	# 	print(file)
	# 	with open(file, mode="r", encoding="utf-8", errors="ignore") as f:
	# 		content = content + f.readlines()	

	# ingredients = set()
	# for line in content:
	# 	recipe = eval(line)

	# 	if recipe is None or recipe["ingredients"] is None:
	# 		continue

	# 	for x in recipe["ingredients"]:
	# 		ingredient = x[3] if not type(x) == type(dict()) else x["name"] 
	# 		ingredient.replace("(optional)", "").strip().lower()
	# 		ingredients.add(ingredient)

	# indian_ingredients = []
	# for x in ingredients:
	# 	for kb_igredient in ingredients_subtree.keys():
	# 		x = x.replace("-", " ")
	# 		if len(re.findall("(^| |\"|'|\()%s.?(s|es|ies)?($| |,|\.|!|\"|'|;|\))" % (kb_igredient[:-1]), x, re.IGNORECASE)) > 0:
	# 			indian_ingredients.append(kb_igredient)

	print("chinese len", len(set(chinese_ingredients)))
	print("italian len", len(set(italian_ingredients)))

	# print(list(set(italian_ingredients) - set(chinese_ingredients)))
	# print("intersection len", len(list(set(italian_ingredients) & set(chinese_ingredients))))
	# print("subtract len", len(list(set(italian_ingredients) - set(chinese_ingredients))))

def main():
	list_chinese_ingredients_from_kb()

if __name__ == "__main__":
	main()