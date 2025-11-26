from . import recipes_blueprint
from flask import render_template


awareness_recipes_names = []
pentesting_recipes_names = []
teaming_recipes_names = []


@recipes_blueprint.route('/')
def recipes():
    return render_template('recipes/recipes.html')


@recipes_blueprint.route('/portfolio/')
def portfolio_recipes():
    return render_template('recipes/portfolio.html')

@recipes_blueprint.route('/services/')
def services_recipes():
    return render_template('recipes/services.html')


@recipes_blueprint.route('/about/')
def about():
    return render_template('recipes/about.html')


@recipes_blueprint.route('/documents/')
def documents():
    return render_template('recipes/documents.html')


@recipes_blueprint.route('/404/')
def fourohfour_recipes():
    return render_template('recipes/404.html')


@recipes_blueprint.route("/contact/")
def contact():
    return render_template("recipes/contact.html")


@recipes_blueprint.route("/thankyou/")
def thankyou():
    return render_template("recipes/thankyou.html")

