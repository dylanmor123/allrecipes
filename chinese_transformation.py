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

mylist = ['https://www.allrecipes.com/recipe/222000/spaghetti-aglio-e-olio/?internalSource=hub%20recipe&referringContentType=search%20results&clickId=cardslot%203',
          'https://www.allrecipes.com/recipe/258817/chicken-pasta-with-artichoke-hearts/?internalSource=rotd&referringContentType=home%20page&clickId=cardslot%201']
test_recipe = make_object(mylist[1])
pp = pprint.PrettyPrinter(indent=4, depth=4)
# pp.pprint(test_recipe)
print('#######################################################################')
# print(test_recipe)


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


def list_ingredients():
	acc = ""
	CH_subtree = getKBSubtree(["ingredients"])
	print("# on ingredients:", len(list(CH_subtree.keys())))
	# pp.pprint(CH_subtree)
	for key in list(CH_subtree.keys())[300:349]:
		print(key)

		url = "https://www.google.com.tr/search?q={}".format(key)
		webbrowser.open(url)

		tags = input("List Categories: ").split()

		if "exit" in tags:
			break

		for tag in tags:
			acc += "addToKB([\"ingredients\", \"{}\", \"{}\"])\n".format(key, tag)
	print(acc)


# pp.pprint(toChinese(test_recipe))

list_ingredients()
