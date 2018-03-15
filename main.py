# -*- coding: utf-8 -*-
import optparse
import webbrowser, os
from allrecipes_scraper import create_recipe_data
from recipe_parser import parse_directions, fully_parse_recipe
from style_transform import transform
from veggie_transformation import from_veggie_to_non_veggie_recipe as from_vegan
from veggie_transformation import from_veggie_to_non_veggie_recipe as from_vegetarian
from veggie_transformation import to_vegan_recipe as to_vegan
from veggie_transformation import to_vegeterian_recipe as to_vegeterian
from to_healthy_recipe import to_healthy_recipe as to_healthy
from to_healthy_recipe import to_unhealthy_recipe as from_healthy
from to_DIY_recipe import to_DIY_recipe as to_diy
from pretty_output import generate_html_page

def main():
	parser = optparse.OptionParser()
	parser.add_option('-u', '--url', action="store", dest="url", help="query string", default="")
	parser.add_option('-t', '--transformation', action="store", dest="transformation", help="transformation string", default="")

	options, args = parser.parse_args()

	url = options.url
	transformation = options.transformation

	if transformation not in ['chinese', 'italian', 'indian', 'to_vegan', 'from_vegan', 'to_vegetarian', 'from_vegetarian', 'to_healthy', 'from_healthy', 'to_diy']:
		print("Sorry, please choose one of the following transformations: 'chinese', 'italian', 'indian', 'to_vegan', 'from_vegan', 'to_vegetarian', 'from_vegetarian', 'to_healthy', 'from_healthy', 'to_diy'")
		return

	# Scrape Recipe
	recipe = create_recipe_data(url)
	if recipe == None:
		print("Sorry, URL invalid")
		return

	# Parse directions
	recipe = fully_parse_recipe(recipe)

	# Make transformation
	if transformation == 'chinese':
		new_recipe = transform(recipe, style='chinese')
	elif transformation == 'italian':
		new_recipe = transform(recipe, style='italian')
	elif transformation == 'indian':
		new_recipe = transform(recipe, style='indian')		
	elif transformation == 'to_vegan':
		new_recipe = to_vegan(recipe)
	elif transformation == 'from_vegan':
		new_recipe = from_vegan(recipe)	
	elif transformation == 'to_vegetarian':
		new_recipe = to_vegeterian(recipe)
	elif transformation == 'from_vegetarian':
		new_recipe = from_vegetarian(recipe)	
	elif transformation == 'from_healthy':
		new_recipe = from_healthy(recipe)	
	elif transformation == 'to_healthy':
		new_recipe = to_healthy(recipe)
	elif transformation == 'to_diy':
		new_recipe = to_diy(recipe)	
	else:
		print("Sorry, please choose one of the following transformations: 'chinese', 'italian', 'indian', 'to_vegan', 'from_vegan', 'to_vegetarian', 'from_vegetarian', 'to_healthy', 'from_healthy', 'to_diy'")
		return


	print('\n' * 6)
	print(new_recipe)
	print('\n')

	# Generate HTML page
	generate_html_page(new_recipe, recipe)
	webbrowser.open('pretty_output.html')


if __name__ == "__main__":
	main()


