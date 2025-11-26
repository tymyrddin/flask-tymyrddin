from flask import Flask, render_template
import json
import os


######################################
#### Application Factory Function ####
######################################

def create_app():
    # Create the Flask application
    app = Flask(__name__)

    # Load news data
    news_path = os.path.join(app.root_path, '..', 'news.json')
    try:
        with open(news_path, 'r') as f:
            news_data = json.load(f)
    except FileNotFoundError:
        news_data = []
    except json.JSONDecodeError:
        news_data = []

    # Make news available to all templates
    @app.context_processor
    def inject_news():
        return {'news_items': news_data[:3]}  # Latest 3 items

    register_blueprints(app)
    register_routes(app)
    register_error_pages(app)
    return app


########################
### Helper Functions ###
########################

def register_blueprints(app):
    # Import the blueprints
    from project.recipes import recipes_blueprint
    from project.blog import blog_blueprint

    # Since the application instance is now created, register each Blueprint
    # with the Flask application instance (app)
    app.register_blueprint(recipes_blueprint)
    app.register_blueprint(blog_blueprint)

def register_routes(app):
    @app.route("/search/")
    def search_page():
        return render_template("search.html")

def register_error_pages(app):
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404
