import allrecipes_scraper
from knowledgebase import *
import re
from fractions import Fraction 

term = ['low-fat', 'low-sodium', 'low-calorie', 'reduced-calorie', 'reduced-sodium', 'reduced-fat', 'fat-free']
salt_sodium = {'teaspoon': 2325, 'teaspoons': 2325, 'pinch': 400, 'pinches': 400, 'tablespoon': 1000, 'tablespoons': 1000, 'stick': 862.5, 'sticks': 862.5, 'cup': 1725, 'cups': 1725, 'pound': 3450, 'pounds': 3450, 'tablespoon': 101, 'tablespoons': 101}

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
	healthy_subtree = getKBSubtree(["substitutes", "healthy"])
	Sodium_nutri = getSodiumfromNutritions(recipe)
	servings = int(recipe['num_servings'])
	amount = 0
	for index,ingredient in enumerate(recipe['ingredients']):
		#If sodium level is not considered low sodium,
		#half the amount of salt if present in ingredients
		if checkSodiumLevel(Sodium_nutri) is True:
			if 'butter' in ingredient['name'] or 'sugar' in ingredient['name'] or 'white sugar' in ingredient['name'] or 'brown sugar' in ingredient['name'] or 'salt' in ingredient['name'] or 'kosher salt' in ingredient['name'] or 'sea salt' in ingredient['name'] and ingredient['measurement'] in salt_sodium.keys():
				measurements = ingredient['quantity'].split() 
				for i in range(len(measurements)):	
					amount = float(sum(Fraction(s) for s in measurements)) / 2 
					ingredient["quantity"] = str(amount)
					print(ingredient['name'] + ': ' + ingredient["quantity"])

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
	return recipe

# ===================================================================

def to_unhealthy_recipe(recipe):
	healthy_subtree = getKBSubtree(["substitutes", "healthy"])
	#print(healthy_subtree)
	amount = 0
	for index,ingredient in enumerate(recipe['ingredients']):
		if 'butter' in ingredient['name'] or 'sugar' in ingredient['name'] or 'white sugar' in ingredient['name'] or 'brown sugar' in ingredient['name'] or 'salt' in ingredient['name'] or 'kosher salt' in ingredient['name'] or 'sea salt' in ingredient['name'] and ingredient['measurement'] in salt_sodium.keys():
			measurements = ingredient['quantity'].split() 
			for i in range(len(measurements)):	
				amount = float(sum(Fraction(s) for s in measurements)) * 2 
				ingredient["quantity"] = str(amount)
				print(ingredient['name'] + ': ' + ingredient["quantity"])
		ingredient_lst = ingredient['name'].split()
		#print("before: ", ingredient['name'])
		for label in term:
			if label in ingredient_lst:
				ingredient_lst.remove(label)
		ingredient['name'] = ' '.join(ingredient_lst)
		#print("after: ", ingredient['name'])
		for substitute, healthy in healthy_subtree.items():
			healthy = list(healthy.keys())[0]
			#print(healthy)
			if healthy in ingredient['name']:
				#print("substitutes for ", ingredient["name"], " -> ", substitute)
				ingredient["name"] = substitute
				break
	for idx, direction in enumerate(recipe["directions"]):
		for substitute, healthy in healthy_subtree.items():
			healthy = list(healthy.keys())[0]
			#print(healthy)
			direction = direction.replace(healthy, substitute)

			if healthy in direction:
				print(idx)
				print(healthy, " -> ", substitute )
				print()

		recipe["directions"][idx] = direction
	return recipe

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
