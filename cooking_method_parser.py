import re
from knowledgebase import getKBSubtree
from collections import Counter

def load_recipes(file):
	dicts_from_file = []
	with open(file, encoding="utf8") as inf:
	    for line in inf:
	        dicts_from_file.append(eval(line))   
	return dicts_from_file 


units = ('cups cans teaspoons tablespoons pinches ounces '
 		 'packages jars slices cloves containers loaf loaves '
 		 'squares gallons bottles pounds sprigs leaves leaf '
 		 'bunches envelopes dashes heads slabs whole racks'
 		 'pieces drops stalks packets links quarts pints ')

ways_to_prepare = ('very and diced chopped shredded minced thinly '
				   'sliced crushed uncooked sifted frozen bone-in '
				   'skinless boneless dried slow-cooked dry coarsely active toasted '
				   'peeled deveined fresh or thawed skin-on unflavored fried cut flattened boiling '
				   'shelled pickled finely grated cubed lightly packed ')


def parse_cooking_methods(directions, cooktimes, all_cooking_methods):
	cooking_methods = {}

	for step in range(0, len(directions)):
		methods_in_step = []
		for word in directions[step].split():
			word = re.sub(r'[^\w\s]','',word).lower()
			if word in all_cooking_methods and ((len(word) > 3) or (len(word) == 3 and word == 'fry')) and word != 'cook' and word != 'cooking' and word != 'stir':
				methods_in_step.append(word)
		cooking_methods[step] =  set(methods_in_step)
	return cooking_methods

def get_main_cooking_method(parsed_cooking_methods, recipe):
	main_cooking_method = []
	for i in range(0, len(parsed_cooking_methods)):
		if len(parsed_cooking_methods[i]) != 0:
			for method in parsed_cooking_methods[i]:
				main_cooking_method.append(method)
	try:
		most_common,num_most_common = Counter(main_cooking_method).most_common(1)[0]
		print(most_common)
		return most_common
	except:
		return ''


subtree = getKBSubtree(['cooking-methods'])
cooking_methods = ' '.join(list(subtree.keys()))
recipes = load_recipes('vegan_recipes.txt')

for recipe in recipes:
	try:
		parsed_methods = parse_cooking_methods(recipe['directions'], recipe['cooktimes'], cooking_methods)
		get_main_cooking_method(parsed_methods, recipe)
	except:
		print("missing either directions or cooktimes for this recipe")
