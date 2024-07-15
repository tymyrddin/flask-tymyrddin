from . import recipes_blueprint
from flask import render_template, abort


awareness_recipes_names = ['programs', 'acai_bowl', 'honey_bran_muffins', 'breakfast_scramble',
                           'pumpkin_donuts', 'waffles', 'omelette', 'chocolate_donuts', 'oatmeal',
                           'morning_glory_muffins', 'blueberry_smoothie_bowl']
pentesting_recipes_names = ['steak_fajitas', 'ground_beef_tacos', 'pizza', 'sweet_fire_chicken', 'tri_tip',
                            'shredded_chicken', 'taquitos', 'red_lentil_chili']
teaming_recipes_names = ['sweet_potatoes', 'spanish_rice', 'jasmine_rice', 'fruit_salad']


@recipes_blueprint.route('/')
def recipes():
    return render_template('recipes/recipes.html',
                           number_of_awareness_recipes=len(awareness_recipes_names),
                           number_of_pentesting_recipes=len(pentesting_recipes_names),
                           number_of_teaming_recipes=len(teaming_recipes_names))


@recipes_blueprint.route('/awareness/')
def awareness_recipes():
    return render_template('recipes/awareness.html')


@recipes_blueprint.route('/awareness/<recipe_name>/')
def awareness_recipe(recipe_name):
    if recipe_name not in awareness_recipes_names:
        abort(404)

    return render_template(f'recipes/{recipe_name}.html')


@recipes_blueprint.route('/pentesting/')
def pentesting_recipes():
    return render_template('recipes/pentesting.html')


@recipes_blueprint.route('/pentesting/<recipe_name>/')
def pentesting_recipe(recipe_name):
    if recipe_name not in pentesting_recipes_names:
        abort(404)

    return render_template(f'recipes/{recipe_name}.html')


@recipes_blueprint.route('/teaming/')
def teaming_recipes():
    return render_template('recipes/teaming.html')


@recipes_blueprint.route('/teaming/<recipe_name>/')
def teaming_recipe(recipe_name):
    if recipe_name not in teaming_recipes_names:
        abort(404)

    return render_template(f'recipes/{recipe_name}.html')
