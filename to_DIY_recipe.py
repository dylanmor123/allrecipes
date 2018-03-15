import allrecipes_scraper
from knowledgebase import *
import re
from fractions import Fraction 

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


