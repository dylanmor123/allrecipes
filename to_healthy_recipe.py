import allrecipes_scraper
from knowledgebase import *
import re


# 1 teaspoon of salt = 2325.5mg 
# 1 pinch of salt = 400mg
# 1 cup(1 block, 2 sticks, 0.5 pound) of butter = .75 cup of olive oil 
# 1 cup of butter = 1725 mg
# unsalted butter instead of normal butter

r3 = {'name': 'Fall 5-Spice Soup', 'description': 'I am a soup fanatic, and found that Chinese 5-spice, made up of anise, fennel, cloves, cinnamon, and white or Szechwan pepper was a great way to jazz-up common fall vegetables.', 'ingredients': [{'name': 'vegetable broth', 'quantity': '6', 'measurement': 'cups', 'preparation': ''}, {'name': 'vegetable oil', 'quantity': '1', 'measurement': 'tablespoon', 'preparation': ''}, {'name': 'onion', 'quantity': '1/2', 'measurement': '', 'preparation': 'chopped'}, {'name': 'celery', 'quantity': '2', 'measurement': 'stalks', 'preparation': 'chopped'}, {'name': 'chinese 5-spice powder', 'quantity': '1 1/2', 'measurement': 'teaspoons', 'preparation': ''}, {'name': 'sweet potatoes', 'quantity': '4', 'measurement': '', 'preparation': 'chopped'}, {'name': 'apples', 'quantity': '2', 'measurement': '', 'preparation': 'peeled'}, {'name': 'salt', 'quantity': '1 1/2', 'measurement': 'teaspoons', 'preparation': ''}], 'directions': ['Pour vegetable broth into a pot and bring to a boil.', 'Heat oil in a skillet over medium heat; cook and stir onion and celery in hot oil until tender, 5 to 10 minutes. Add Chinese 5-spice powder to onion mixture, stir to coat, and cook until fragrant, about 1 minute.', 'Mix sweet potatoes, apples, salt, and onion mixture into broth; cook until sweet potatoes are tender, 20 to 25 minutes. Cool soup for at least 5 minutes.', 'Pour soup into a blender no more than half full. Cover and hold lid down; pulse a few times before leaving on to blend. Puree in batches until smooth.'], 'nutrition_facts': 'Nutrition Facts\nPer Serving:\n324 calories;\n4.6 g fat;\n66.7 g carbohydrates;\n5.7 g protein;\n0 mg cholesterol;\n1705 mg sodium.\nPowered by the ESHA Research Database © 2018, ESHA Research, Inc. All Rights Reserved\n', 'num_servings': '4', 'num_calories': '324', 'cooktimes': [('Prep', '20m'), ('Cook', '25m'), ('Ready In', '50m')]}
term2 = 'low-fat milk'
term = ['low-fat', 'low-sodium', 'low-calorie', 'reduced-calorie', 'reduced-sodium', 'reduced-fat', 'fat-free']
salt_sodium = {'teaspoon': 2325, 'teaspoons': 2325, 'pinch': 400, 'pinches': 400, 'tablespoon': 1000, 'tablespoons': 1000}
butter_sodim = {'stick': 862.5, 'sticks': 862.5, 'cup': 1725, 'cups': 1725, 'pound': 3450, 'pounds': 3450, 'tablespoon': 101, 'tablespoons': 101}

# replacement = {'flour': 'gluten-free flour', 'couscous': 'quinoa', 'bread crumbs': 
# 'ground flaxseeds', 'tortilla': 'corn tortilla', 'pita': 'large collard leaf',
# 'sugar': 'unsweetened applesauce', 'white sugar': 'unsweetened applesauce', 
# 'peanut butter': 'natural peanut butter',
# 'butter': 'unsweetened butter', 'milk': 'almond milk', 'cream': 'coconut milk',
# 'soy sauce': 'low-sodium soy sauce', 'rice': 'brown rice', 'white rice': 'brown rice',
# 'bread': 'whole-wheat bread', 'white bread': 'whole-wheat bread', 'sour cream': 'greek yogurt', 
# 'mayonnaise': 'greek yogurt with hint of herbs and lemon juice', 'ground beef': 'ground turkey',
# 'ground pork': 'ground turkey',
# 'bacon': 'lean prosciutto', 'cream cheese': 'fat-free cream cheese', 'lettuce': 'arugula',
# 'penne pasta': 'brown rice pasta', 'syrup': 'applesauce', 'ketchup': 'sun-dried tomato hummus'}

def checkS(lst, term):
	lst2 = term.split()
	for label in lst:
		if label in lst2: 
			lst2.remove(label)
			ad = ' '.join(lst2)
		break
	print(ad)

checkS(term, term2)

def getSodiumfromNutritions(recipe):
	wordList = re.sub("[^\w]", " ",  recipe["nutrition_facts"]).split()
	sod_amount = wordList[wordList.index('sodium') - 2]
	return int(sod_amount)


def checkSodiumLevel(amount):
	if amount > 140:
		return True
	else:
		return False	


def to_healthy_recipe(recipe):
	print(recipe)
	
	healthy_subtree = getKBSubtree(["substitutes", "healthy"])
	Sodium_nutri = getSodiumfromNutritions(recipe)
	servings = int(recipe['num_servings'])
	sodium_int = 0
	for index,ingredient in enumerate(recipe['ingredients']):
		#If sodium level is not considered low sodium,
		#half the amount of salt if present in ingredients
		if checkSodiumLevel(Sodium_nutri) is True:
			if 'salt' in ingredient['name'] or 'kosher salt' in ingredient['name'] or 'sea salt' in ingredient['name'] and ingredient['measurement'] in salt_sodium.keys():
				measurements = ingredient['quantity'].split() 
				for i in range(len(measurements)):
					if measurements[i] == '1/2':
						measurements[i] = 0.5
						sodium_int += measurements[i]
					elif measurements[i] == '1/4':
						measurements[i] = 0.25
						sodium_int += measurements[i]						
					try:
						measurements[i] = int(measurements[i])
						sodium_int += measurements[i]
					except:
						continue
				sodium_int = sodium_int / 2
				ingredient["quantity"] = str(sodium_int)
				print(ingredient["quantity"])
				#ngredient = list(ingredient)
				#sodium = int(ingredient[0])*salt_sodium[ingredient[1]]
				#ingredient['quantity'] = int(ingredient['quantity'])
				#print(ingredient['quantity'])
				#reduced_quantity = int(ingredient[0]) / 2
				#ingredient[0] = str(reduced_quantity)
				#ingredient = tuple(ingredient)
				#reduced_sodium = sodium / 2 
				#ingredient['quantity'] = reduced_quantity

		for non_healthy, substitute in healthy_subtree.items():
			substitute = list(substitute.keys())[0]
			if non_healthy in ingredient['name']:
				print("substitutes for ", ingredient["name"], " -> ", substitute)
				ingredient["name"] = substitute
				break
	for idx, direction in enumerate(recipe["directions"]):
		for non_healthy, substitute in healthy_subtree.items():
			substitute = list(substitute.keys())[0]

			direction = direction.replace(non_healthy, substitute)

			if non_healthy in direction:
				print(idx)
				print(non_healthy, " -> ", substitute )
				print()

		recipe["directions"][idx] = direction
	print(recipe)
	return recipe
		# print("substitute = list ... : ", substitute)
		# if ingredient['name'] in replacement:
		# 	ingredient['name'] = replacement[ingredient['name']]

		# if 'butter' in ingredient:
		# 	ingredient['name'] = 'unsalted butter'
		# 	recipe['ingredients'][index][-1] = 'unsalted butter'
# to_healthy_recipe(r3)

# def to_unhealthy_recipe(recipe):
# 	healthy_subtree = getKBSubtree(["substitutes", "healthy"])
# 	for index,ingredient in enumerate(recipe['ingredients']):
# 		if 'sugar' in ingredient['name'] or 'white sugar' in ingredient['name'] or 'brown sugar' in ingredient['name'] or 'salt' in ingredient['name'] or 'kosher salt' in ingredient['name'] or 'sea salt' in ingredient['name'] and ingredient['measurement'] in salt_sodium.keys():
# 			measurements = ingredient['quantity'].split() 
# 			for i in range(len(measurements)):	
# 				if measurements[i] == '1/2':
# 					measurements[i] = 0.5
# 					amount += measurements[i]
# 				elif measurements[i] == '1/4':
# 					measurements[i] = 0.25
# 					amount += measurements[i]						
# 				try:
# 					measurements[i] = int(measurements[i])
# 					amount += measurements[i]
# 				except:
# 					continue
# 				amount = amount * 2
# 				ingredient["quantity"] = str(amount)
# 				print(ingredient["quantity"])
# 		if 'butter' in ingredient['name'] and ingredient['measurement'] in butter_sodium.keys():
# 				if measurements[i] == '1/2':
# 					measurements[i] = 0.5
# 					amount += measurements[i]
# 				elif measurements[i] == '1/4':
# 					measurements[i] = 0.25
# 					amount += measurements[i]						
# 				try:
# 					measurements[i] = int(measurements[i])
# 					amount += measurements[i]
# 				except:
# 					continue
# 				amount = amount * 2
# 				ingredient["quantity"] = str(amount)
# 				print(ingredient["quantity"])
# 		ingredient_lst = ingredient['name'].split
# 		for label in term:
# 			if label in ingredient_lst:
# 				ingredient_lst.remove(label)
# 				ingredient['name'] = ' '.join(ingredient_lst)
# 				break
# 		for non_healthy, substitute in healthy_subtree.items():
# 			substitute = list(substitute.keys())[1]
# 			if non_healthy in ingredient['name']:
# 				print("substitutes for ", ingredient["name"], " -> ", substitute)
# 				ingredient["name"] = substitute
# 				break
# 	# for idx, direction in enumerate(recipe["directions"]):
# 	# 	for non_healthy, substitute in healthy_subtree.items():
# 	# 		substitute = list(substitute.keys())[1]

# 	# 		direction = direction.replace(non_healthy, substitute)

# 	# 		if non_healthy in direction:
# 	# 			print(idx)
# 	# 			print(non_healthy, " -> ", substitute )
# 	# 			print()

# 	# 	recipe["directions"][idx] = direction
# 	# print(recipe)
# 	return recipe


# def to_healthy_recipe(recipe):
# 	print(recipe)
	
# 	healthy_subtree = getKBSubtree(["substitutes", "healthy"])
# 	Sodium_nutri = getSodiumfromNutritions(recipe)
# 	servings = int(recipe['num_servings'])
# 	sodium_int = 0
# 	for index,ingredient in enumerate(recipe['ingredients']):
# 		#If sodium level is not considered low sodium,
# 		#half the amount of salt if present in ingredients
# 		if checkSodiumLevel(Sodium_nutri) is True:
# 			if 'salt' in ingredient['name'] or 'kosher salt' in ingredient['name'] or 'sea salt' in ingredient['name'] and ingredient['measurement'] in salt_sodium.keys():
# 				measurements = ingredient['quantity'].split() 
# 				for i in range(len(measurements)):
# 					if measurements[i] == '1/2':
# 						measurements[i] = 0.5
# 						sodium_int += measurements[i]
# 					elif measurements[i] == '1/4':
# 						measurements[i] = 0.25
# 						sodium_int += measurements[i]						
# 					try:
# 						measurements[i] = int(measurements[i])
# 						sodium_int += measurements[i]
# 					except:
# 						continue
# 				sodium_int = sodium_int / 2
# 				ingredient["quantity"] = str(sodium_int)
# 				print(ingredient["quantity"])
# 				#ngredient = list(ingredient)
# 				#sodium = int(ingredient[0])*salt_sodium[ingredient[1]]
# 				#ingredient['quantity'] = int(ingredient['quantity'])
# 				#print(ingredient['quantity'])
# 				#reduced_quantity = int(ingredient[0]) / 2
# 				#ingredient[0] = str(reduced_quantity)
# 				#ingredient = tuple(ingredient)
# 				#reduced_sodium = sodium / 2 
# 				#ingredient['quantity'] = reduced_quantity

# 		for non_healthy, substitute in healthy_subtree.items():
# 			substitute = list(substitute.keys())[0]
# 			if non_healthy in ingredient['name']:
# 				print("substitutes for ", ingredient["name"], " -> ", substitute)
# 				ingredient["name"] = substitute
# 				break
# 	for idx, direction in enumerate(recipe["directions"]):
# 		for non_healthy, substitute in healthy_subtree.items():
# 			substitute = list(substitute.keys())[0]

# 			direction = direction.replace(non_healthy, substitute)

# 			if non_healthy in direction:
# 				print(idx)
# 				print(non_healthy, " -> ", substitute )
# 				print()

# 		recipe["directions"][idx] = direction
# 	print(recipe)
# 	return recipe

# def main():
# 	healthy_subtree = getKBSubtree(["substitutes", "healthy"])

# 	content = ""
# 	with open("chinese_recipes.txt", mode="r", encoding="utf-8") as f:
# 	    content = f.readlines()

# 	ingredients = set()
# 	for line in content:
# 		recipe = eval(line)
# 		recipe["ingredients"] = parse_ingredients(recipe["ingredients"])


# 		for x in recipe["ingredients"]:
# 			ingredients.add(x["name"])

# 	for x in ingredients:
# 		print(x)
# 		for non_healthy, substitute in healthy_subtree.items():
# 			substitute = list(substitute.keys())[0]
# 			if non_healthy in x:
# 				print("##### substitutes for ", x, " -> ", substitute)
# 				print()	

# if __name__ == "__main__":
# 	main()
