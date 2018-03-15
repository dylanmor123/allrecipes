import allrecipes_scraper
from knowledgebase import *
import re
from fractions import Fraction 

ex_recipe = {'name': 'Italian Sausage, Peppers, and Onions', 'description': 'My family has been using this very simple and delicious recipe for sausage, peppers, and onions for years and years now. For an extra kick, try using half sweet sausage and half hot sausage!', 'ingredients': [{'name': 'sweet italian sausage', 'quantity': '6 (4 ounce)', 'measurement': 'links', 'preparation': ''}, {'name': 'butter', 'quantity': '2', 'measurement': 'tablespoons', 'preparation': ''}, {'name': 'yellow onion', 'quantity': '1', 'measurement': '', 'preparation': 'sliced'}, {'name': 'onion', 'quantity': '1/2', 'measurement': '', 'preparation': 'sliced'}, {'name': 'garlic', 'quantity': '4', 'measurement': 'cloves', 'preparation': 'minced'}, {'name': 'large red bell pepper', 'quantity': '1', 'measurement': '', 'preparation': 'sliced'}, {'name': 'green bell pepper', 'quantity': '1', 'measurement': '', 'preparation': 'sliced'}, {'name': 'basil', 'quantity': '1', 'measurement': 'teaspoon', 'preparation': 'dried '}, {'name': 'oregano', 'quantity': '1', 'measurement': 'teaspoon', 'preparation': 'dried '}, {'name': 'white wine', 'quantity': '1/4', 'measurement': 'cup', 'preparation': ''}], 'directions': ['Place the sausage in a large skillet over medium heat, and brown on all sides. Remove from skillet, and slice.', 'Melt butter in the skillet. Stir in the yellow onion, red onion, and garlic, and cook 2 to 3 minutes. Mix in red bell pepper and green bell pepper. Season with basil, and oregano. Stir in white wine. Continue to cook and stir until peppers and onions are tender.', 'Return sausage slices to skillet with the vegetables. Reduce heat to low, cover, and simmer 15 minutes, or until sausage is heated through.'], 'nutrition_facts': 'Nutrition Facts\nPer Serving:\n461 calories;\n39.4 g fat;\n7 g carbohydrates;\n17.1 g protein;\n96 mg cholesterol;\n857 mg sodium.\nPowered by the ESHA Research Database © 2018, ESHA Research, Inc. All Rights Reserved\n', 'num_servings': '6', 'num_calories': '461', 'cooktimes': [('Prep', '15m'), ('Cook', '25m'), ('Ready In', '40m')]}

def get_veggie_list():
	healthy_subtree = getKBSubtree(["ingredients"])
	vegetables = []
	for ingredient in healthy_subtree:
		try:
			veggie = list(healthy_subtree[ingredient]["category"])[0]
			if veggie == "vegetables":
				vegetables.append(ingredient)
		except:
			continue
	return vegetables	

def to_DIY_recipe(recipe):
	print(recipe)
	vegetable_list = get_veggie_list()
	ingredient_list = []

	for index,ingredient in enumerate(recipe['ingredients']):
		for veggie in vegetable_list:
			if veggie in ingredient['name']:
				ingredient['name'] = 'ready-made ' + ingredient['preparation'] + ' ' + ingredient['name']
				ingredient['preparation'] = ''
				ingredient_list.append(ingredient['name'])
				print(ingredient['name'])
				break
			else:
				continue
		ingredient_list.append(ingredient['name'])
	
	ingredient_sentence = ', '.join(ingredient_list)
	#print('ingredient_sentece: ', ingredient_sentence)
	recipe['directions'] = ["Place " + ingredient_sentence + "in a slow cooker, cook for 4 -6 hours, and serve."]
	#print('directions: ', recipe['directions'])
	print(recipe)
	return recipe


