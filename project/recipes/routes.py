from . import recipes_blueprint
from flask import render_template, abort


awareness_recipes_names = []
pentesting_recipes_names = []
teaming_recipes_names = []


@recipes_blueprint.route('/')
def recipes():
    return render_template('recipes/recipes.html',
                           number_of_awareness_recipes=len(awareness_recipes_names),
                           number_of_pentesting_recipes=len(pentesting_recipes_names),
                           number_of_teaming_recipes=len(teaming_recipes_names))


@recipes_blueprint.route('/awareness/')
def awareness_recipes():
    return render_template('recipes/awareness.html')


@recipes_blueprint.route('/pentesting/')
def pentesting_recipes():
    return render_template('recipes/pentesting.html')


@recipes_blueprint.route('/teaming/')
def teaming_recipes():
    return render_template('recipes/teaming.html')

