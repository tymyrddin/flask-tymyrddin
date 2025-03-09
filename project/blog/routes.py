from . import blog_blueprint
from flask import render_template


blog_post_titles = ['Improbability Blog', 'Cuisine Starlight', 'Oink Blog']


@blog_blueprint.route('/blog/')
def blog():
    return render_template('blog/blog.html')

