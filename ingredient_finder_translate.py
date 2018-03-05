import allrecipes_scraper as ars
import time
import argparse
from multiprocessing import Pool


def getAllRecipeData(urls):
	recipe_lists = []
	for url in urls:
		recipe = ars.create_recipe_data(url)
		time.sleep(1)
		recipe_lists.append(recipe)
	print(recipe_lists)
	print(len(recipe_lists))
	return(recipe_lists)


def helper(pair):
	# print(pair[0], pair[1])
	try:
		url = "https://translate.google.com/translate?sl=en&tl=es&js=y&prev=_t&hl=en&ie=UTF-8&u=https%3A%2F%2F" + 'https://www.allrecipes.com/search/results/?wt=' + str(pair[1]) + '&sort=re&page=' + str(pair[0])
		time.sleep(2)
		html = ars.get_recipe(url)
		urls = get_urls(html)
		return urls
	except:
		print("link is broken")
		print(url)
		return None


def getIngredientsFromInput(cuisine, page_counter):
	# total_urls = set()
	p = Pool(page_counter)
	total_urls = p.map(helper, map(lambda num: [num, cuisine], list(range(1, page_counter + 1))))
	print(len(total_urls))
	url_list = [url for sublist in total_urls for url in sublist]
	#print(url_list)

	p2 = Pool(len(url_list))
	recipe_lists = p2.map(ars.create_recipe_data, url_list)

	#print(recipe_lists)
	print("Number of recipes: ", len(recipe_lists))
	f = open("{}_recipes.txt".format(cuisine), "w+")
	for recipe in recipe_lists:
		f.write("%s\n" % recipe)
	f.close()
	return recipe_lists


def get_urls(html):
	url_set = set()
	url_list_1 = html.find('section', {'id': 'grid'})
	for link in url_list_1.findAll('a', href=True):
		if '/recipe/' in link['href'] and 'https://www.allrecipes.com' in link['href']:
			link['href'] = "https://translate.google.com/translate?sl=en&tl=es&js=y&prev=_t&hl=en&ie=UTF-8&u=https%3A%2F%2F" + link['href']
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