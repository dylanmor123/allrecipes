import allrecipes_scraper as ars
import time
import argparse
from multiprocessing import Pool


def chunks(l, n):
	for i in range(0, len(l), n):
		yield l[i:i + n]

def getAllRecipeData(urls):
	recipe_lists = []
	GROUP_SIZE = 4

	groups = list(chunks(urls, GROUP_SIZE))

	for group in groups:
		print(group[0])

		p = Pool(GROUP_SIZE)
		recipes = p.map(ars.create_recipe_data, group)  # ars.create_recipe_data(url)
		#print(recipes)
		time.sleep(2)
		recipe_lists.append(recipes)
	#print(len(recipe_lists))
	return(recipe_lists)


def helper(pair):
	# print(pair[0], pair[1])
	try:
		url = 'https://www.allrecipes.com/search/results/?wt=' + str(pair[1]) + '&sort=re&page=' + str(pair[0])
		html = ars.get_recipe(url)
		urls = get_urls(html)
		return urls
	except:
		print("link is broken")
		print(url)
		return None


def getIngredientsFromInput(cuisine, page_counter):
	# # total_urls = set()
	# p = Pool(page_counter)
	# total_urls = p.map(helper, map(lambda num: [num, cuisine], list(range(1, page_counter + 1))))
	# print(len(total_urls))
	# url_list = [url for sublist in total_urls for url in sublist]
	# print(len(url_list))

	counter = 1
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

	print(len(total_urls))
	recipe_lists = getAllRecipeData(list(total_urls))
	final_list = [rec for sublist in recipe_lists for rec in sublist]
	# p2.map(ars.create_recipe_data, url_list)

	print("Number of recipes: ", len(final_list))
	f = open("{}_recipes.txt".format(cuisine), "w+")
	for recipe in final_list:
		f.write("%s\n" % recipe)
	f.close()
	return final_list


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
