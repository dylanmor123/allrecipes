from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from allrecipes_scraper import get_ingredients as get_ingredients

def get_recipe(url):
	hdr = {'User-Agent': 'Mozilla/5.0'}
	req = Request(url, headers=hdr)
	page = urlopen(req)
	soup = BeautifulSoup(page, 'html.parser')
	return soup

# def getNameFromHandle(handle):
# 	try:
# 		url = 'https://api.twitter.com/1.1/users/lookup.json?screen_name=' + handle
# 		auth = OAuth1(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
# 		r = requests.get(url, auth=auth)
# 		return json.loads(r.text)[0]['name']
# 	except:
# 		return None

def get_urls(html):
	url_set = set()
	url_list_1 = html.find('section', {'id': 'grid'})
	for link in url_list_1.findAll('a', href=True):
		if '/recipe/' in link['href'] and 'https://www.allrecipes.com' in link['href']:
			url_set.add(link['href'])
		else:
			continue
	return url_set

#https://www.allrecipes.com/search/results/?wt=mexican&sort=re&page=6#6

def main():
	ingredients_list = []
	urls = get_urls(get_recipe('https://www.allrecipes.com/?page=2'))
	for url in urls:
		html = get_recipe(url)
		ingredients = get_ingredients(html)
		ingredients_list.append(ingredients)
	print(ingredients_list)

main()



