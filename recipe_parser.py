import re 
from knowledgebase import getKBSubtree
from collections import Counter
from nltk import word_tokenize, pos_tag
import nltk


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
	with open(file) as inf:
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

def parse_directions(recipe):
	# Get ingredient names from recipe
	list_of_ingredients = []
	all_sentences = []
	for ingredient in recipe['ingredients']:
		list_of_ingredients.append(ingredient['name'])

	sentences = get_sentences(' '.join(recipe['directions']))

	for sentence in sentences:
		raw_text = sentence
		sentence = sentence.replace("-", ".").lower()

		duration = get_duration(sentence)

		action_verbs = match_from_kb(sentence, list(getKBSubtree(["cooking-actions"]).keys()), 'verb')

		cooking_methods = match_from_kb(sentence, list(getKBSubtree(["cooking-methods"]).keys()), 'verb')
		tools = match_from_kb(sentence, list(getKBSubtree(["tools"]).keys()), 'noun')

		ingredients = []
		kb_ingredients = match_from_kb(sentence, list(getKBSubtree(["ingredients"]).keys()), 'noun')

		for ingredient in kb_ingredients:
			match_ingredient_list_indices = []
			for i in range(0, len(list_of_ingredients)):
				curr_ingredient = list_of_ingredients[i].replace('(', '').replace(')', '')
				if match_noun_in_sentence(curr_ingredient, ingredient) or match_noun_in_sentence(ingredient, curr_ingredient):
					match_ingredient_list_indices.append(i)
			ingredients.append({'name': ingredient, 'match_ingredient_list_indices': match_ingredient_list_indices})
		all_sentences.append(
							{'raw_text': raw_text,
							'ingredients': ingredients,
							'cooking_methods': cooking_methods,
							'tools': tools,
							'action_verbs': list(set(action_verbs)),
							'duration': duration
			})
	return all_sentences


def match_from_kb(sentence, kb_items, query):
	matches_in_sentence = []
	for item in kb_items:
		item_match = []
		if query == 'noun':
			item_match = match_noun_in_sentence(item, sentence)
		if query == 'verb':
			item_match = match_verb_in_sentence(item, sentence)
		if item_match:
			matches_in_sentence.append(item_match[0][1])
	return matches_in_sentence

def match_noun_in_sentence(word, sentence):
	return re.findall("(^| |\"|')((%s.?(s|es|ies))|(%s.?(s|es|ies))|%s)($| |,|\.|!|\"|'|;)" % (word[:-1], word, word), sentence, re.IGNORECASE)

def match_verb_in_sentence(word, sentence):
	return re.findall("(^| |\"|')((%s.?(s|ing|ed|ied|x|en))|(%s.?(s|ing|ed|ied|x|en))|%s)($| |,|\.|!|\"|'|;)" % (word[:-1], word, word), sentence, re.IGNORECASE)

def get_duration(sentence):
	time_scale = ['day', 'hour', 'minute', 'second']
	duration = ''
	for unit in time_scale:
		if unit in sentence:
			duration += sentence.split(unit)[0].split()[-1] + ' ' + unit + 's '
	return duration.strip()

def get_sentences(directions):
	tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
	return tokenizer.tokenize(directions)


def parse_recipe(recipe):
	if type(recipe) == dict:
		recipe['sentences'] = parse_directions(recipe)
		return recipe

if __name__ == "__main__":
	parse_recipe(load_recipes('italian_recipes.txt')[0])


# def parse_recipe(recipe):
# 	if type(recipe) == str:
# 		try:
# 			recipe = create_recipe(recipe)
# 		except:
# 			try:
# 				recipe = load_recipes(recipe)
# 			except:
# 				print("There was a problem")
# 				return "There was a problem"

# 	elif type(recipe) == dict:
# 		recipe['sentences'] = parse_directions(recipe)
# 		print(recipe)
# 		return recipe


# def main():
# 	parse_recipe(load_recipes('italian_recipes.txt')[0])
# main()


