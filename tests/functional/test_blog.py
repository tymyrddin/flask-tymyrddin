"""
This file (test_blog.py) contains the functional tests for the `blog` blueprint.
"""
from project.blog.routes import blog_post_titles


def test_get_blog_page(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/blog/' page is requested (GET)
    THEN check the response is valid
    """
    titles = [b'Improbability Blog',
              b'Cuisine Starlight',
              b'Oink Blog']
    response = test_client.get('/blog/')
    assert response.status_code == 200
    for title in titles:
        assert title in response.data


def test_get_about_page(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/about/' page is requested (GET)
    THEN check the response is valid
    """
    headings = [b'Ingredients for success', b'Services', b'Contact']
    response = test_client.get('/about/')
    assert response.status_code == 200
    for heading in headings:
        assert heading in response.data


def test_get_invalid_request(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/idonotexist' page is requested (GET)
    THEN check that the 404 page is returned
    """
    headings =[b'Page Not Found (404)', b'Go Home']
    response = test_client.get('/idonotexist/')
    assert response.status_code == 404
    for heading in headings:
        assert heading in response.data
