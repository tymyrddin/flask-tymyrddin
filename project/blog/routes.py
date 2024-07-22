from . import blog_blueprint
from flask import render_template, abort


blog_post_titles = ['Improbability Blog', 'Cuisine Starlight', 'Oink Blog']


@blog_blueprint.route('/blog/')
def blog():
    return render_template('blog/blog.html')


@blog_blueprint.route('/about/')
def about():
    return render_template('blog/about.html')


@blog_blueprint.route('/documents/')
def documents():
    return render_template('blog/documents.html')


@blog_blueprint.route('/projects/')
def projects():
    return render_template('blog/projects.html')


@blog_blueprint.route('/ipa/')
def ipa():
    return render_template('recipes/ipa.html')


@blog_blueprint.route("/contact/")
def contact():
    return render_template("blog/contact.html")


@blog_blueprint.route("/thankyou/")
def thankyou():
    return render_template("blog/thankyou.html")
