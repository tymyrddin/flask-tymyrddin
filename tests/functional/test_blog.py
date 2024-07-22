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


def test_get_about_page(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/about/' page is requested (GET)
    THEN check the response is valid
    """
    headings = [b'No instant transportation', b'Never Up To Date', b'With Love']
    response = test_client.get('/about/')
    assert response.status_code == 200
    for heading in headings:
        assert heading in response.data


def test_get_projects_page(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/projects/' page is requested (GET)
    THEN check the response is valid
    """
    headings = [b'I have room']
    response = test_client.get('/projects/')
    assert response.status_code == 200
    for heading in headings:
        assert heading in response.data


def test_get_ipa_page(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/ipa/' page is requested (GET)
    THEN check the response is valid
    """
    headings = [b'IPA project']
    response = test_client.get('/ipa/')
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
    WHEN the '/about/' page is requested (GET)
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
