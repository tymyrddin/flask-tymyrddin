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
    header_items = [b'Ty Myrddin']
    response = test_client.get('/')
    assert response.status_code == 200
    for header_item in header_items:
        assert header_item in response.data


def test_get_portfolio(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/' page is requested (GET)
    THEN check the response is valid
    """
    header_items = [b'Portfolio']
    response = test_client.get('/portfolio/')
    recipe_types = [b'See around corners']
    assert response.status_code == 200
    for header_item in header_items:
        assert header_item in response.data
    for recipe_type in recipe_types:
        assert recipe_type in response.data


def test_get_about_page(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/about/' page is requested (GET)
    THEN check the response is valid
    """
    headings = [b'Why I do this']
    response = test_client.get('/about/')
    assert response.status_code == 200
    for heading in headings:
        assert heading in response.data


def test_get_documents_page(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/documents/' page is requested (GET)
    THEN check the response is valid
    """
    headings = [b'Legalities']
    response = test_client.get('/documents/')
    assert response.status_code == 200
    for heading in headings:
        assert heading in response.data


def test_get_contact_page(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/contact/' page is requested (GET)
    THEN check the response is valid
    """
    headings = [b'Contact']
    response = test_client.get('/contact/')
    assert response.status_code == 200
    for heading in headings:
        assert heading in response.data


def test_get_thankyou_page(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/thankyou/' page is requested (GET)
    THEN check the response is valid
    """
    headings = [b'Thank you']
    response = test_client.get('/thankyou/')
    assert response.status_code == 200
    for heading in headings:
        assert heading in response.data


def test_get_404_page(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/404/' page is requested (GET)
    THEN check the response is valid
    """
    headings = [b'Uh,oh, 404, not found', b'Here, for whatever reason, is the world']
    response = test_client.get('/404/')
    assert response.status_code == 200
    for heading in headings:
        assert heading in response.data


def test_get_invalid_request(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/idonotexist' page is requested (GET)
    THEN check that the 404 page is returned
    """
    headings = [b'Uh,oh, 404, not found', b'Here, for whatever reason, is the world']
    response = test_client.get('/idonotexist/')
    assert response.status_code == 404
    for heading in headings:
        assert heading in response.data

