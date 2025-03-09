"""
This file (test_blog.py) contains the functional tests for the `blog` blueprint.
"""
# from project.blog.routes import blog_post_titles


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





