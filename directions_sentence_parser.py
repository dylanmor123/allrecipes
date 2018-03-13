import re
from knowledgebase import getKBSubtree
from collections import Counter
from nltk import word_tokenize, pos_tag
import nltk

def load_recipes(file):
	dicts_from_file = []
	with open(file) as inf:
	    for line in inf:
	        dicts_from_file.append(eval(line))   
	return dicts_from_file 



subtree = getKBSubtree(['cooking-methods'])
cooking_methods = ' '.join(list(subtree.keys()))
recipe = load_recipes('chinese_recipes.txt')[0]

BLACKLISTED_WORDS = ['large', 'small', ]

# "name": "recipe name",
# 	"description": "recipe description",
# 	"ingredients":  [{  
# 	    "name":    "sea salt",  
# 	    "quantity":    1,  
# 	    "measurement":    "pinch",
# 	    "preparation":    "none"  
# 	}],
# 	"directions" : [{
# 		"raw_text": "Task 1. Task 2."
# 		"sentences": [{
# 			"raw_text" : "Task 1."
# 			"cooking methods" : ["bake"]
# 			"ingredients_from_list" : [{
#                                         "ingredient_list_index": 1,
#                                         "sentence_spam": (3, 4)
#                                     }],
#                                     "ingredients_from_kb" : ["yolk", "whites"]
# 			"tools" : ["spoon", "oven"]
# 			"action_verbs" : ["crack", "pour"]
# 			"duration" : "3 to 5 minutes"
# 		}]
# 	}],
#     "cooking method": "primary cooking method",  
# 	"cooking tools": ["knife", "grater", "dutch oven"],    
# 	"nutrition_facts": [{
# 		"quantity": "104.8",
# 		"measurement": "g",
# 		"name": "carbohydrates"
# 	},],

def directions_sentence_parser(recipe):
	cooking_methods = []
	final_sentences = []
	list_of_ingredients = []
	for ingredient in recipe['ingredients']:
		list_of_ingredients.append(ingredient['name'])
	for direction in recipe['directions']:
		tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
		data = direction
		sentences = tokenizer.tokenize(data)
		for s in range(0, len(sentences)):
			raw_text = sentences[s]
			sentence = sentences[s].replace("-", ".").lower()
			cooking_methods = get_regex_match_directions(sentence, list(getKBSubtree(["cooking-methods"]).keys()), 'method')
			ingredients_from_kb = get_regex_match_directions(sentence, list(getKBSubtree(["ingredients"]).keys()), 'ingredient')
			duration = get_duration(sentence)
			ingredients_from_list = []
			tokens = ''.join(c for c in sentence if c not in ('!','.',':', ',', ';')).split()
			for i in range(0, len(list_of_ingredients)):
				ingredient_matches = get_regex_match_directions(list_of_ingredients[i], tokens, 'ingredient')
				if ingredient_matches:
					print(tokens)
					print(list_of_ingredients, ingredient_matches)
					print('\n')
				ingredient_number = i
			step = {'raw_text': raw_text,
					'ingredients_from_kb': ingredients_from_kb,
					'ingredients_from_list': ingredients_from_list,
					'cooking_methods': cooking_methods,
					'tools': 'TODO ADD TOOLS',
					'actions': 'TODO ADD NON-COOKING PREPARATION METHODS',
					'duration': duration
					}
			final_sentences.append(step) 
	recipe['directions'] = {'raw_text': recipe['directions'], 'sentences': final_sentences}
	return recipe


def get_regex_match_directions(sentence, kb_subtree, query = 'ingredient'):
	matches_in_sentence = []
	for item in kb_subtree:
		if query == 'method':
			item_match = match_verb_in_sentence(item, sentence)
		else:
			item_match = match_noun_in_sentence(item, sentence)
		if len(item_match) > 0:
			matches_in_sentence.append(item)

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

print(get_duration('here is a sample of 4 minutes and 45 hours you know'))

methods = set([''])
methods = directions_sentence_parser(recipe)
print(methods['directions'])
# for word in methods:
# 	print(word) 
	
# print(methods)