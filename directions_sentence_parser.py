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


def directions_parser(recipe):
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

		# TODO
		# action_verbs = match_from_kb(sentence, list(getKBSubtree(["cooking-actions"]).keys()), 'verb')

		cooking_methods = match_from_kb(sentence, list(getKBSubtree(["cooking-methods"]).keys()), 'verb')
		tools = match_from_kb(sentence, list(getKBSubtree(["tools"]).keys()), 'noun')

		ingredients = []
		kb_ingredients = match_from_kb(sentence, list(getKBSubtree(["ingredients"]).keys()), 'noun')

		for ingredient in kb_ingredients:
			match_ingredient_list_indices = []
			for i in range(0, len(list_of_ingredients)):
				if match_noun_in_sentence(list_of_ingredients[i], ingredient) or match_noun_in_sentence(ingredient, list_of_ingredients[i]):
					match_ingredient_list_indices.append(i)
			ingredients.append({'name': ingredient, 'match_ingredient_list_indices': match_ingredient_list_indices})
		print(ingredients)
		all_sentences.append(
							{'raw_text': raw_text,
							'ingredients': ingredients,
							'cooking_methods': cooking_methods,
							'tools': tools,
							# Need to add all non-cooking techniques to knolwedge base
							# For now, just use the first word
							'action_verbs': sentence.split()[0],
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



def main():
	recipe = load_recipes('chinese_recipes.txt')[0]
	directions = directions_parser(recipe)
	for direction in directions:
		print(direction)

main()
