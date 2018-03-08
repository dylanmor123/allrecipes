import re 


def quantity_str_to_float(quantity_str):
	total = 0
	all_nums = re.findall("([0-9]+(/[0-9]+)?)", quantity_str)
	for num in all_nums:
		num = num[0]
		if "/" in num:
			x, y = num.split("/")
			total += float(x) / float(y)
		else:
			total += float(num)

	return total

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


def parse_ingredients(list_of_ingredients):

	parsed_ingredients = []

	for item in list_of_ingredients:
		separated_item = re.findall('\[[^\]]*\]|\([^\)]*\)|\"[^\"]*\"|\S+',item)
		quantity = ''
		unit = ''
		preparation = ''
		ingredient = ''

		if ':' in item:
			continue

		else:
			if any(char.isdigit() for char in separated_item[0]):
				quantity += separated_item[0]
				del separated_item[0]
				if any(char.isdigit() for char in separated_item[0]):
					quantity += ' ' + separated_item[0].lower()
					del separated_item[0]
			if separated_item[0] in units:
				unit = separated_item[0]
				del separated_item[0]

			while len(separated_item) > 0 and separated_item[0] in ways_to_prepare:
				preparation += separated_item[0].lower() + ' '
				del separated_item[0]
			ingredient = ' '.join(separated_item).lower()

			if ':' in ingredient:
				print(list_of_ingredients)
				print(ingredient, item)

			if 'skinless, boneless' in ingredient or 'boneless, skinless' in ingredient:
				if len(ingredient.split(', ')) > 2:
					preparation = ingredient.split(', ')[2].strip()
					ingredient = ', '.join(ingredient.split(', ')[0:2]).strip()

			elif len(ingredient.split(',')) > 1:
				preparation = ingredient.split(',')[1][1:].lower().strip()
				ingredient = ingredient.split(',')[0].lower().strip()

			if len(ingredient.split(' - ')) > 1:
				preparation = ingredient.split(' - ')[1].lower().strip()
				ingredient = ingredient.split(' - ')[0].lower().strip()

		parsed_ingredients.append({
				"name": ingredient,
				"quantity": quantity,
				"measurement": unit,
				"preparation": preparation,
			}
		)

	return parsed_ingredients



# recipes = load_recipes('chinese_recipes.txt')
# for recipe in recipes:
# 	ingredients = parse_ingredients(recipe['ingredients'])
# 	for ingredient in ingredients:
# 		print(ingredient)
# 	print()
