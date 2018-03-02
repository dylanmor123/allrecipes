import allrecipes_scraper as ars
import time
import argparse

# def getAllIngredients(urls):
# 	ingredient_lists = []
# 	for url in urls:
# 		html = ars.get_recipe(url)
# 		ingredients = ars.get_ingredients(html)
# 		ingredient_lists.append(ingredients)
# 		time.sleep(1)
# 	return(ingredient_lists)

def getAllRecipeData(urls):
	recipe_lists = []
	for url in urls:
		recipe = ars.create_recipe_data(url)
		time.sleep(1)
		recipe_lists.append(recipe)
	print(recipe_lists)
	print(len(recipe_lists))
	return(recipe_lists)

def getIngredientsFromInput(cuisine, page_counter):
	counter = 0
	total_urls = set()
	while counter < page_counter+1:
		try:
			url = 'https://www.allrecipes.com/search/results/?wt=' + cuisine + '&sort=re&page=' + str(counter)
			html = ars.get_recipe(url)
			urls = get_urls(html)
			total_urls = total_urls|urls
			counter += 1
		except:
			print("link is broken")
			print(url)
			return None
	recipe_lists = getAllRecipeData(total_urls)
	print(recipe_lists)
	print("Number of recipes: ", len(recipe_lists))
	f = open("recipes.txt", "w+")
	for recipe in recipe_lists:
		f.write("%s\n" % recipe)
	f.close()
	return recipe_lists
	
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