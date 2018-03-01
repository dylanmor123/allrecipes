from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from allrecipes_scraper import get_ingredients as get_ingredients

def get_recipe(url):
	hdr = {'User-Agent': 'Mozilla/5.0'}
	req = Request(url, headers=hdr)
	page = urlopen(req)
	soup = BeautifulSoup(page, 'html.parser')
	return soup

def get_urls(html):
	url_set = set()
	url_list_1 = html.find('section', {'id': 'grid'})
	for link in url_list_1.findAll('a', href=True):
		if '/recipe/' not in link['href'] and 'https://www.allrecipes.com' not in link['href']:
			continue
		else:
			url_set.add(link['href'])
	return url_set

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

def main():
	ingredients_list = []
	urls = get_urls(get_recipe('https://www.allrecipes.com/?page=2#2'))
	print(urls)
	# for url in urls:
	# 	html = get_recipe(url)
	# 	ingredients = get_ingredients(html)
	# 	ingredients_list.append(ingredients)
	# print(ingredients_list)

main()



