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
			print("found", ingredient["name"].lower())
			ingr_tags = list(getKBSubtree(["ingredients", ingredient["name"].lower()]))

			if style not in ingr_tags:
				if "chinese" in ingr_tags: ingr_tag = ingr_tags.remove("chinese")
				if "italian" in ingr_tags: ingr_tag = ingr_tags.remove("italian")
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
		elif any(filter(lambda x: x in ingredient["name"].lower(), list(subtree.keys()))):
			substring_keys = [name for name in list(subtree.keys()) if name in ingredient["name"].lower()]
			match = max(substring_keys, key=len)
			print("found", match)

			ingr_tags = list(getKBSubtree(["ingredients", match]))

			if style not in ingr_tags:
				if "chinese" in ingr_tags: ingr_tag = ingr_tags.remove("chinese")
				if "italian" in ingr_tags: ingr_tag = ingr_tags.remove("italian")				
				intersect_ingr = {k: len(set(ingr_tags) & set(v)) for k, v in transform_ingr.items()}
				max_value = max(intersect_ingr.values())
				max_keys = [k for k, v in intersect_ingr.items() if v == max_value]

				if max_keys and max_value > 0:
					sub = random.choice(max_keys)
					print("substitutes for", match, " -> ", sub)
					subs[ingredient["name"].lower()] = sub
					ingredient["name"] = sub

			else:
				print("swapped", ingredient["name"].lower(), " -> ", match)
				subs[ingredient["name"].lower()] = match
				ingredient["name"] = match

		else:
			print("what is", ingredient["name"].lower(), "?")

	print()
	print("Direction Swaps:")
	for idx, direction in enumerate(recipe["directions"]):
		for original, new_ingr in subs.items():
			if original in direction.lower():
				direction = direction.lower().replace(original, new_ingr)
				#print(idx)
				print(original, " -> ", new_ingr)
				#print()

		recipe["directions"][idx] = direction

	return recipe


def list_ingredients():
	acc = ""
	CH_subtree = getKBSubtree(["ingredients"])
	print("# on ingredients:", len(list(CH_subtree.keys())))
	# pp.pprint(CH_subtree)
	for key in list(CH_subtree.keys())[131:]:
		print(key)

		url = "https://www.google.com.tr/search?q={}".format(key)
		webbrowser.open(url)

		tags = input("List Categories: ").split()

		if "exit" in tags:
			break

		for tag in tags:
			acc += "addToKB([\"ingredients\", \"{}\", \"{}\"])\n".format(key, tag)
	print(acc)


def add_new_ingredients():
	acc = ""
	while True:

		name = input("Ingredient name: ")
		tags = input("Tags: ").split()

		if "exit" in tags:
			break

		for tag in tags:
			acc += "addToKB([\"ingredients\", \"{}\", \"{}\"])\n".format(name, tag)
	print(acc)


def things_from_list(things, category):
	acc = ""
	for thing in things:
		acc += "addToKB([\"\", \"{}\"])\n".format(category, thing)
	print(acc)


if __name__ == '__main__':
	mylist = ['https://www.allrecipes.com/recipe/222000/spaghetti-aglio-e-olio/?internalSource=hub%20recipe&referringContentType=search%20results&clickId=cardslot%203',
		      'https://www.allrecipes.com/recipe/258817/chicken-pasta-with-artichoke-hearts/?internalSource=rotd&referringContentType=home%20page&clickId=cardslot%201']
	test_recipe = make_object(mylist[1])
	pp = pprint.PrettyPrinter(indent=4, depth=4)
	# pp.pprint(test_recipe)
	print('###################################################################')
	# print(test_recipe)

	#pp.pprint(toChinese(test_recipe, "italian"))
	#pp.pprint(transform(test_recipe, "italian"))
	list_ingredients()
	#add_new_ingredients()
	#actions_from_list(["dab", "trace", "dump", "dash", "unwrap", "turn", "reduce", "mince", "empty", "chill", "serve", "unmold", "cook", "halve", "pound", "smash", "wrap", "blend", "nestle", "unlock", "grate", "increase", "bind", "grind", "break", "flatten", "unseal", "crust", "refrigerate", "overlap", "wiggle", "check", "skim", "whip", "distribute", "criss-cross", "tilt", "spray", "plunge", "tear", "secure", "slit", "sift", "lift", "segment", "punch", "soften", "decrease", "apply", "refill", "tap", "position", "rotate", "center", "temper", "pop", "pulse", "shred", "process", "wash", "melt", "save", "assemble", "flip", "seal", "discard", "swirl", "store", "lubricate", "repeat", "throw", "pin", "strain", "invert", "stream", "mash", "pre-heat", "paint", "rest", "adjust", "extract", "scrub", "clean", "incorporate", "submerge", "crumble", "drain", "thin", "crack", "steep", "dice", "thread", "retain", "pour", "smooth", "garnish", "spoon", "shake", "pat", "rinse", "knead", "flick", "shape", "pass", "light", "zest", "cool", "fan", "scoop", "switch", "splash", "lie", "mop", "close", "peel", "thaw", "add", "without", "even", "alternate", "fermentation", "scatter", "spread", "stuff", "unfold", "fold", "chop", "estimate", "skin", "slide", "uncover", "fluff", "start", "push", "avoid", "ferment", "drop", "remember", "freeze", "coat", "arrange", "dollop", "lay", "finish", "deep", "mist", "trim", "balance", "squeeze", "watch", "puncture", "replace", "split", "portion", "place", "grill", "pierce", "stir", "massage", "taper", "whisk", "separate", "rub", "skewer", "reshape", "double-wrap", "snip", "remove", "slip", "reheat", "brush", "cut", "drape", "release", "debone", "select", "open", "glaze", "oil", "stretch", "scrape", "tamp", "crush", "set", "hollow", "dot", "combine", "wait", "pull", "thicken", "reselect", "round", "frost", "dry", "attach", "soak", "pry", "pack", "wad", "lower", "reposition", "slice", "puree", "loosen", "taste", "stack", "sweeten", "truss", "trim", "husk", "roll", "flake", "keep", "prick", "moisten", "unroll", "wet", "tie", "draw", "pick", "deflate", "mix", "wipe", "dissolve", "cube", "fill", "season", "prepare", "hoisin", "immerse", "tighten", "scramble", "ration", "plop", "use", "pinch", "measure", "decorate", "top", "layer", "dip", "poke", "snap", "grab", "transfer", "divide", "drizzle", "warm", "marinate", "force", "insert", "hold", "slather", "pressure", "braid", "crimp", "sprinkle", "press", "untie", "whirl", "dampen", "fry", "toss", "beat", "sterilize", "twist", "trickle", "cover", "rewarm", "carve", "stick", "rinse"])
