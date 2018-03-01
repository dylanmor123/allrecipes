from bs4 import BeautifulSoup
from urllib.request import Request, urlopen



def get_recipe(url):
	hdr = {'User-Agent': 'Mozilla/5.0'}
	req = Request(url, headers=hdr)
	page = urlopen(req)
	soup = BeautifulSoup(page, "html.parser")
	return soup

print(get_recipe('https://www.allrecipes.com/recipe/50054/portuguese-pork-with-red-peppers/?internalSource=previously%20viewed&referringContentType=home%20page&clickId=cardslot%208'))