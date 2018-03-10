import re
from knowledgebase import getKBSubtree
from collections import Counter
from nltk import word_tokenize, pos_tag
import nltk

def load_recipes(file):
	dicts_from_file = []
	with open(file, encoding="utf8") as inf:
	    for line in inf:
	        dicts_from_file.append(eval(line))   
	return dicts_from_file 



subtree = getKBSubtree(['cooking-methods'])
cooking_methods = ' '.join(list(subtree.keys()))
recipes = load_recipes('chinese_recipes.txt')


def directions_sentence_parser(recipe):
	cooking_methods = []
	i = 0
	for direction in recipe['directions']:
		tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
		data = direction
		sentences = tokenizer.tokenize(data)
		for sentence in sentences:
			sentence = sentence.replace("-", ".").lower()
			cooking_methods = get_regex_match_directions(sentence, list(getKBSubtree(["cooking-methods"]).keys()))
			ingredients = get_regex_match_directions(sentence, list(getKBSubtree(["ingredients"]).keys()))
			if len(cooking_methods) == 0:
				print(sentence)
			# if len(cooking_methods) == 0:
			# 	words = sentence.split()
			# 	method = words[0].replace(r"\(.*\)","")
			# 	method = re.sub(r'[^\w\s]','',method)
			# 	if method[len(method)-2:len(method)] == "ly":
			# 		methods_in_sentence.append(words[1])
			# 	else:
			# 		methods_in_sentence.append(method)
			# print(methods_in_sentence)

	print(cooking_methods, ingredients)
	return cooking_methods


def get_regex_match_directions(sentence, kb_subtree):

	matches_in_sentence = []
	for item in kb_subtree:
		item_match = re.findall("(^| |\"|')%s.?(s|es|ies|ing|ed|ied|x|en)?($| |,|\.|!|\"|'|;)" % (item[:-1]), sentence, re.IGNORECASE)
		if len(item_match) > 0:
			matches_in_sentence.append(item)
	return matches_in_sentence


methods = set([''])
for recipe in recipes:
	methods = directions_sentence_parser(recipe)

# for word in methods:
# 	print(word) 
	
# print(methods)