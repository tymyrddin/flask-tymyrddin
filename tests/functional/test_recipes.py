"""
This file (test_recipes.py) contains the functional tests for the `recipes` blueprint.
"""
# from project.recipes.routes import awareness_recipes_names, pentesting_recipes_names, \
#                                  baked_goods_recipes_names, side_dishes_recipes_names, \
#                                  dessert_recipes_names, drink_recipes_names


def test_get_home_page(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/' page is requested (GET)
    THEN check the response is valid
    """
    header_items = [b'Ty Myrddin', b'Home', b'Blogs', b'About']
    recipe_types = [b'Raising security awareness', b'Pentesting', b'Colourful teaming']
    response = test_client.get('/')
    assert response.status_code == 200
    for header_item in header_items:
        assert header_item in response.data
    for recipe_type in recipe_types:
        assert recipe_type in response.data


def test_get_awareness_page(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/awareness/' page is requested (GET)
    THEN check the response is valid
    """
    headings = [b'The usual suspects', b'Test driven efforts', b'Hands-on workshops']
    response = test_client.get('/awareness/')
    assert response.status_code == 200
    for heading in headings:
        assert heading in response.data


def test_get_pentesting_page(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/pentesting/' page is requested (GET)
    THEN check the response is valid
    """
    headings = [b'The difference between scanning and pentesting', b'What needs testing?', b'Bureaucracy required']
    response = test_client.get('/pentesting/')
    assert response.status_code == 200
    for heading in headings:
        assert heading in response.data


def test_get_teaming_page(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/teaming/' page is requested (GET)
    THEN check the response is valid
    """
    headings = [b'Red and blue teams', b'Purple teams', b'Ingredients for success']
    response = test_client.get('/teaming/')
    assert response.status_code == 200
    for heading in headings:
        assert heading in response.data

