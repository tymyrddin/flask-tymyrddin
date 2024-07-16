from . import blog_blueprint
from flask import render_template, abort


blog_post_titles = ['Improbability Blog', 'Cuisine Starlight', 'Oink Blog']


@blog_blueprint.route('/blog/')
def blog():
    return render_template('blog/blog.html')


@blog_blueprint.route('/about/')
def about():
    return render_template('blog/about.html')


@blog_blueprint.route("/contact/")
def contact():
    return render_template("blog/contact.html")
