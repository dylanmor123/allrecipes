"""
Essential Chinese Ingrediants

Light & Dark Soy Sauce
Shaoxing Wine / Dry Sherry
Black Vinegar
Oyster Sauce
Dried Shiitake Mushrooms
Dried Chili Peppers
Sichuan Peppercorn
Fermented Bean Paste
Star Anaise
Five spice powder

Hoisin Sauce
Peanut Oil
Toasted Sesame Oil
Deep fried Tofu
Dried Shrimp

Cooking methods
stir-frying
slow cooking
double boiling


"""
from knowledgebase import *
from allrecipes_scraper import create_recipe_data as make_object
import pprint
import webbrowser
import random

def toChinese(recipe):
	CH_subtree = getKBSubtree(["substitutes", "toChinese"])

	for ingredient in recipe["ingredients"]:
		for non_CH, substitute in CH_subtree.items():
			substitute = list(substitute.keys())[0]
			if non_CH in ingredient["name"].lower():
				# TODO: get best substitute based on the role of the ingredient. Not just the last match.
				print("substitutes for ", ingredient["name"].lower(), " -> ", substitute)
				ingredient["name"] = substitute
				break

	for idx, direction in enumerate(recipe["directions"]):
		# print(direction.lower())
		for non_CH, substitute in CH_subtree.items():
			substitute = list(substitute.keys())[0]

			# TODO: get best substitute based on the role of the ingredient. Not just the last match.
			direction = direction.lower().replace(non_CH, substitute)

			if non_CH in direction:
				print(idx)
				print(non_CH, " -> ", substitute)
				print()

		recipe["directions"][idx] = direction

	return recipe


def transform(recipe, style="chinese"):
	subtree = getKBSubtree(["ingredients"])
	for key in subtree.keys():
		subtree[key] = list(subtree[key].keys())
	transform_ingr = {k: v for k, v in subtree.items() if style in v}

	subs = {}
	for ingredient in recipe["ingredients"]:
		if ingredient["name"].lower() in list(subtree.keys()):
			ingr_tags = list(getKBSubtree(["ingredients", ingredient["name"].lower()]))

			if style not in ingr_tags:
				intersect_ingr = {k: len(set(ingr_tags) & set(v)) for k, v in transform_ingr.items()}
				max_value = max(intersect_ingr.values())
				max_keys = [k for k, v in intersect_ingr.items() if v == max_value]

				if max_keys and max_value > 0:
					sub = random.choice(max_keys)
					print("substitutes for", ingredient["name"].lower(), " -> ", sub)
					subs[ingredient["name"].lower()] = sub
					ingredient["name"] = sub
				else:
					print("no substitutes for", ingredient["name"].lower())
		else:
			print("what is", ingredient["name"].lower(), "?")

	for idx, direction in enumerate(recipe["directions"]):
		for original, new_ingr in subs.items():
			if original in direction:
				direction = direction.lower().replace(original, new_ingr)
				print(idx)
				print(original, " -> ", new_ingr)
				print()

		recipe["directions"][idx] = direction

	return recipe


def list_ingredients():
	acc = ""
	CH_subtree = getKBSubtree(["ingredients"])
	print("# on ingredients:", len(list(CH_subtree.keys())))
	# pp.pprint(CH_subtree)
	for key in list(CH_subtree.keys())[:]:
		print(key)

		url = "https://www.google.com.tr/search?q={}".format(key)
		webbrowser.open(url)

		tags = input("List Categories: ").split()

		if "exit" in tags:
			break

		for tag in tags:
			acc += "addToKB([\"ingredients\", \"{}\", \"{}\"])\n".format(key, tag)
	print(acc)


if __name__ == '__main__':
	mylist = ['https://www.allrecipes.com/recipe/222000/spaghetti-aglio-e-olio/?internalSource=hub%20recipe&referringContentType=search%20results&clickId=cardslot%203',
		      'https://www.allrecipes.com/recipe/258817/chicken-pasta-with-artichoke-hearts/?internalSource=rotd&referringContentType=home%20page&clickId=cardslot%201']
	test_recipe = make_object(mylist[0])
	pp = pprint.PrettyPrinter(indent=4, depth=4)
	# pp.pprint(test_recipe)
	print('#######################################################################')
	# print(test_recipe)

	pp.pprint(transform(test_recipe))
	# list_ingredients()
