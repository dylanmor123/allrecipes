from recipe_parser import parse_ingredients, quantity_str_to_float, parse_recipe, get_match_maybe_plural_noun_in_sentence_regex
from allrecipes_scraper import create_recipe_data

INGREDIENT_HTML = """
<li class="checkList__line">
    <label ng-class="{true: 'checkList__item'}[true]" title="1/4 cup butter, divided" class="checkList__item">
            <input data-id="16157" name="ingredientCheckbox" data-role="none" type="checkbox" value="N" ng-click="saveIngredient($event,16157)">
        <span class="recipe-ingred_txt added" data-id="16157" data-nameid="16157" itemprop="ingredients">%s %s %s%s %s</span>
    </label>
    <!-- ngRepeat: deal in deals["16157"] -->
</li>
"""

INGREDIENT_HTML_BOLD = """
<li class="checkList__line">
    <label ng-class="{true: 'checkList__item'}[true]" title="1/4 cup butter, divided" class="checkList__item">
            <input data-id="16157" name="ingredientCheckbox" data-role="none" type="checkbox" value="N" ng-click="saveIngredient($event,16157)">
        <span class="recipe-ingred_txt added" data-id="16157" data-nameid="16157" itemprop="ingredients" style="font-weight: bold;">%s %s %s%s %s</span>
    </label>
    <!-- ngRepeat: deal in deals["16157"] -->
</li>
"""

DIRECTION_HTML = """
<li class="step" ng-class="{&#39;finished&#39;: stepIsActive0}" ng-click="stepIsActive0 = !stepIsActive0"><span class="recipe-directions__list--item">
%s</span></li>
"""

def get_ingredient_ul_tag(ingredient, bold=False):
	html = INGREDIENT_HTML_BOLD if bold else INGREDIENT_HTML
	prep_separator = "" if ingredient["preparation"] == "" else ","
	return html % (ingredient["quantity"], ingredient["measurement"], ingredient["name"], prep_separator, ingredient["preparation"])

def get_ingredients_html(ingredients, old_ingredients):
	ingredients_html = ""
	for idx, ingredient in enumerate(ingredients):
		bold = not ingredient["name"] == old_ingredients[idx]["name"]
		ingredients_html += get_ingredient_ul_tag(ingredient, bold = bold)
	return ingredients_html

def get_directions_html(directions):
	directions_html = ""
	for direction in directions:
		directions_html += DIRECTION_HTML % (direction)
	return directions_html

def generate_html_page(recipe, old_recipe):
	with open("output.html", mode="r") as f:
		htmlpage = "\n".join(f.readlines())
		htmlpage = htmlpage.replace("NLP_INGREDIENTS_GO_HERE", get_ingredients_html(recipe["ingredients"], old_recipe["ingredients"]))
		htmlpage = htmlpage.replace("NLP_DIRECTIONS_GO_HERE", get_directions_html(recipe["directions"]))

		# Open a file
		output_file = open("pretty_output.html", "w")
		
		# Write to file
		output_file.write(htmlpage)

		# Close opend file
		output_file.close()

		print("HTML output created at: pretty_output.html")


if __name__ == "__main__":
	url = 'https://www.allrecipes.com/recipe/17205/eggs-benedict/?internalSource=hub%20recipe&referringContentType=search%20results&clickId=cardslot%201'
	recipe = parse_recipe(create_recipe_data(url))
	generate_html_page(recipe, recipe)