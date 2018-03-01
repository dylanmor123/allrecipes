from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from allrecipes_scraper import get_ingredients as get_ingredients
import operator as operator
import time
import argparse

def get_recipe(url):
	hdr = {'User-Agent': 'Mozilla/5.0'}
	req = Request(url, headers=hdr)
	page = urlopen(req)
	soup = BeautifulSoup(page, 'html.parser')
	return soup

def getAllIngredients(urls):
	ingredient_lists = []
	for url in urls:
		html = get_recipe(url)
		ingredients = get_ingredients(html)
		ingredient_lists.append(ingredients)
		time.sleep(1)
	return(ingredient_lists)

def getIngredientsFromInput(cuisine, page_counter):
	counter = 0
	total_urls = set()
	while counter < page_counter+1:
		try:
			url = 'https://www.allrecipes.com/search/results/?wt=' + cuisine + '&sort=re&page=' + str(counter)
			html = get_recipe(url)
			urls = get_urls(html)
			total_urls = total_urls|urls
			counter += 1
		except:
			print("link is broken")
			return None
	ingredient_lists = getAllIngredients(total_urls)
	print(ingredient_lists)
	print("Number of recipes: ", len(ingredient_lists))
	return ingredient_lists
	
def get_urls(html):
	url_set = set()
	url_list_1 = html.find('section', {'id': 'grid'})
	for link in url_list_1.findAll('a', href=True):
		if '/recipe/' in link['href'] and 'https://www.allrecipes.com' in link['href']:
			url_set.add(link['href'])
		else:
			continue
	return url_set

def main(cuisine_style, count):
    getIngredientsFromInput(cuisine_style, count)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('cuisine_style', type=str) 
    parser.add_argument('count', type=int)
    args = parser.parse_args()
    main(args.cuisine_style, args.count)