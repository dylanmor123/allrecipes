import re 

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
 		 ' ')

ways_to_prepare = ('diced chopped shredded minced thinly '
				   'sliced crushed uncooked sifted frozen bone-in '
				   'skinless boneless dried slow-cooked dry coarsely active toasted '
				   'peeled fresh or thawed skin-on unflavored ')

def parse_ingredients(list_of_ingredients):
	for item in list_of_ingredients:
		separated_item = re.findall('\[[^\]]*\]|\([^\)]*\)|\"[^\"]*\"|\S+',item)
		quantity = ''
		unit = ''
		preparation = ''
		ingredient = ''
		if any(char.isdigit() for char in separated_item[0]):
			quantity += separated_item[0]
			del separated_item[0]
			if any(char.isdigit() for char in separated_item[0]):
				quantity += ' ' + separated_item[0].lower()
				del separated_item[0]
		if separated_item[0] in units:
			unit = separated_item[0]
			del separated_item[0]
		while separated_item[0] in ways_to_prepare:
			preparation += separated_item[0].lower() + ' '
			del separated_item[0]
		ingredient = ' '.join(separated_item).lower()

		
		if len(ingredient.split(',')) > 1:
			preparation = ingredient.split(',')[1][1:].lower()
		ingredient = ingredient.split(',')[0].lower()	


		return quantity, unit, preparation, ingredient



recipes = load_recipes('chinese_recipes.txt')
for recipe in recipes:
	print(parse_ingredients(recipe['ingredients']))
