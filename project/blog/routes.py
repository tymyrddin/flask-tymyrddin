from . import blog_blueprint
from flask import render_template, abort


blog_post_titles = []


@blog_blueprint.route('/blog/')
def blog():
    return render_template('blog/blog.html')


@blog_blueprint.route('/about/')
def about():
    return render_template('blog/about.html')
