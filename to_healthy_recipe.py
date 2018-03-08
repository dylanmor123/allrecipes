import allrecipes_scraper
from knowledgebase import *
import re


# 1 teaspoon of salt = 2325.5mg 
# 1 pinch of salt = 400mg
# 1 cup(1 block, 2 sticks, 0.5 pound) of butter = .75 cup of olive oil 
# 1 cup of butter = 1725 mg
# unsalted butter instead of normal butter

r2 = {'name': 'Vegan Totchos', 'description': 'When you love tots and you love nachos and you need a vegan recipe for totchos! Optional toppings include fresh or canned green chiles or jalapenos, sliced green onions, fresh cilantro, and/or hot sauce.', 'ingredients': [('', '', '', 'olive oil cooking spray'), ('1 (12 ounce)', 'package', '', "vegan beef crumbles (such as trader joe's beef-less ground beef®)"), ('1', 'cup', 'or to taste', 'mild green salsa'), ('1 (6 ounce)', 'can', 'drained', 'black olives'), ('1 (32 ounce)', 'package', 'frozen ', 'bite-size potato nuggets (such as tater tots®)'), ('1 (8 ounce)', 'package', 'shredded ', 'vegan cheese (such as daiya®)'), ('1', 'cup', '', 'vegan sour cream (such as tofutti®) (optional)')], 'directions': ['Preheat oven to 425 degrees F (220 degrees C).', 'Spray a skillet with cooking spray and add vegan crumbles. Cook and stir over medium heat until heated through and uniformly broken up, about 5 minutes. Stir in salsa and black olives. Remove from heat and cover to keep warm.', 'Spread taters on a baking sheet in a single layer.', 'Bake in the preheated oven for 10 minutes. Turn taters over; bake until crispy, about 10 minutes more.', 'Transfer taters to a shallow, oven-safe serving dish. Spread crumbles-salsa mixture evenly on top. Sprinkle vegan cheese on top.', "Set oven rack about 6 inches from the heat source and preheat the oven's broiler.", 'Place baking dish in the oven. Broil, watching closely to prevent burning, until vegan cheese is melted, about 3 minutes.', 'Top with dollops of vegan sour cream.'], 'nutrition_facts': 'Nutrition Facts\nPer Serving:\n382 calories;\n21.9 g fat;\n37.1 g carbohydrates;\n11.6 g protein;\n0 mg cholesterol;\n1283 mg sodium.\nPowered by the ESHA Research Database © 2018, ESHA Research, Inc. All Rights Reserved\n', 'num_servings': '10', 'num_calories': '382', 'cooktimes': [('Prep', '10m'), ('Cook', '28m'), ('Ready In', '38m')]}
r3 = {'name': 'Honeymoon Eggs Benedict', 'description': 'This is more or less the eggs Benedict dish my husband and I had on our honeymoon at a little mom-and-pop bed and breakfast. Eight years later, I still think this is great for breakfast!', 'ingredients': [('12', '', 'fresh ', 'asparagus spears'), ('4', '', '', 'eggs'), ('1', 'teaspoon', '', 'distilled white vinegar'), ('1', 'teaspoon', '', 'salt'), ('2', '', 'split', 'large croissants'), ('4', 'slices', '', 'canadian-style bacon'), ('1', 'cup', 'grated ', 'asiago cheese'), ('1/2', 'cup', '', 'prepared hollandaise sauce'), ('4', 'tablespoons', '', 'butter')], 'directions': ['Place a steamer insert into a saucepan and fill with water to just below the bottom of the steamer. Cover pan and bring the water to a boil. Add asparagus, cover, and steam until just tender, 2 to 6 minutes depending on thickness.', 'Fill a large saucepan with 2 to 3 inches of water and bring to a boil. Reduce the heat to medium-low, pour in the vinegar, and keep the water at a gentle simmer. Stir in salt until dissolved. Crack an egg into a small bowl and gently slip the egg into the simmering water, holding the bowl just above the surface of the water. Repeat with the remaining eggs. Poach the eggs until the whites are firm and the yolks have thickened but are not hard, 3 to 5  minutes. Remove the eggs from the water with a slotted spoon, drain on plate lined with kitchen towels to remove excess water, then place onto a warm plate.', "Preheat the oven's broiler and set the oven rack about 6 inches from the heat source.", 'Arrange croissant halves on a baking sheet. Top each with 1 poached egg, 1 slice Canadian bacon, 3 spears asparagus, and 1/4 cup Asiago cheese.', 'Broil in preheated oven until cheese is melted and beginning to crisp, 2 to 3 minutes.', 'Heat hollandaise sauce in a saucepan over medium heat until bubbly and hot, about 5 minutes. Serve sauce poured over baked croissants.'], 'nutrition_facts': 'Nutrition Facts\nPer Serving:\n859 calories;\n60 g fat;\n36.5 g carbohydrates;\n44.5 g protein;\n625 mg cholesterol;\n3302 mg sodium.\nPowered by the ESHA Research Database © 2018, ESHA Research, Inc. All Rights Reserved\n', 'num_servings': '2', 'num_calories': '859', 'cooktimes': [('Prep', '10m'), ('Cook', '20m'), ('Ready In', '30m')]}


salt_sodium = {'teaspoon': 2325, 'teaspoons': 2325, 'pinch': 400, 'pinches': 400}
#butter_sodim = {'stick': 862.5, 'sticks': 862.5, 'cup': 1725, 'cups': 1725, 'pound': 3450, 'pounds': 3450, 'tablespoon': 101, 'tablespoons': 101}

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
	print(healthy_subtree)

	Sodium_nutri = getSodiumfromNutritions(recipe)
	servings = int(recipe['num_servings'])
	for index,ingredient in enumerate(recipe['ingredients']):
		if checkSodiumLevel(Sodium_nutri) is True:
			if 'salt' in ingredient and any(x in salt_sodium.keys() for x in ingredient):
				ingredient = list(ingredient)
				#sodium = int(ingredient[0])*salt_sodium[ingredient[1]]
				reduced_quantity = int(ingredient[0]) / 2
				ingredient[0] = str(reduced_quantity)
				ingredient = tuple(ingredient)
				print(ingredient['quantity'])
				#reduced_sodium = sodium / 2 
				#ingredient['quantity'] = reduced_quantity
		#for non_healthy, substitute in healthy_subtree.items():
			# print("non_healthy: ", non_healthy)
			# print("substitute: ", substitute)
			# substitute = list(substitute.keys())[0]
			# print("substitute = list ... : ", substitute)
		#TODO Update Nutrition for original_sod_perserving - reduced_per_seving
		# if ingredient['name'] in replacement:
		# 	ingredient['name'] = replacement[ingredient['name']]
	return recipe

			# if 'butter' in ingredient:
			# 	ingredient['name'] = 'unsalted butter'
			# 	#recipe['ingredients'][index][-1] = 'unsalted butter'



to_healthy_recipe(r3)


