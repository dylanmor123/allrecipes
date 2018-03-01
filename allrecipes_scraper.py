from bs4 import BeautifulSoup
from urllib.request import Request, urlopen


def get_recipe(url):
	hdr = {'User-Agent': 'Mozilla/5.0'}
	req = Request(url, headers=hdr)
	page = urlopen(req)
	soup = BeautifulSoup(page, 'html.parser')
	return soup

def get_description(html):
	description = html.find('div', {'class': 'submitter__description'})
	description = description.text.strip()
	return description[1:len(description)-1]

def get_name(html):
	name = html.find('h1', {'class': 'recipe-summary__h1'}).text
	return name

def get_ingredients(html):
	#ingredients broken into 2 drop down lists from html
	ingredients = []
	ingredients_list_1 = html.find('ul', {'class': 'checklist dropdownwrapper list-ingredients-1'})
	ingredients_list_2 = html.find('ul', {'class': 'checklist dropdownwrapper list-ingredients-2'})
	ingredients_list_1 = ingredients_list_1.findAll('li', {'class': 'checkList__line'})
	ingredients_list_2 = ingredients_list_2.findAll('li', {'class': 'checkList__line'})
	list_of_ingredients = ingredients_list_1 + ingredients_list_2
	for item in list_of_ingredients:
		ingredients.append(str(item.contents[1].text).strip())
	return ingredients[0:len(ingredients)-1]

def get_directions(html):
	directions = []
	directions_list = html.find('ol', {'class': 'list-numbers recipe-directions__list'})
	directions_list = directions_list.findAll('li', {'class': 'step'})
	for step in directions_list:
		directions.append(step.text)
	return directions

def get_nutrition(html):
	nutrition_info = html.find('section', {'itemprop': 'nutrition'}).text
	nutrition_info = [line.strip() for line in nutrition_info.split('\n')]
	nutrition_facts_str = ''
	for line in nutrition_info:
		if line:
			nutrition_facts_str += line + '\n'
	return(nutrition_facts_str)

url = 'https://www.allrecipes.com/recipe/50054/portuguese-pork-with-red-peppers/?internalSource=previously%20viewed&referringContentType=home%20page&clickId=cardslot%208'
#url = 'https://www.allrecipes.com/recipe/236776/slow-cooker-sweet-and-sour-pot-roast/?internalSource=previously%20viewed&referringContentType=home%20page&clickId=cardslot%2011'
#url = 'https://www.allrecipes.com/recipe/221987/honeymoon-eggs-benedict/?internalSource=previously%20viewed&referringContentType=home%20page&clickId=cardslot%2014'

print(url)
print()
recipe_html = get_recipe(url)
name = get_name(recipe_html)
print(name)
print()
description = get_description(recipe_html)
print(description)
print()
ingredients = get_ingredients(recipe_html)
print(ingredients)
print()
directions = get_directions(recipe_html)
print(directions)
print()
nutrition_facts = get_nutrition(recipe_html)
print(nutrition_facts)
print()