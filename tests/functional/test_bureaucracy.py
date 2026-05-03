"""
This file (test_bureaucracy.py) contains the functional tests for the `bureaucracy` blueprint.
"""


def test_get_simulator_page(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/bureaucracy/' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get('/bureaucracy/')
    assert response.status_code == 200


def test_simulator_page_contains_phrase_bank(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/bureaucracy/' page is requested (GET)
    THEN check that the phrase bank JSON is embedded in the page
    """
    response = test_client.get('/bureaucracy/')
    assert b'phrase-bank-data' in response.data
    assert b'bureaucracy.js' in response.data


def test_simulator_page_contains_intake_form(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/bureaucracy/' page is requested (GET)
    THEN check that the intake form fields are present
    """
    response = test_client.get('/bureaucracy/')
    assert b'concern-description' in response.data
    assert b'system-type' in response.data
    assert b'severity' in response.data
    assert b'urgency' in response.data


def test_simulator_page_contains_all_stage_panels(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/bureaucracy/' page is requested (GET)
    THEN check that all five stage panels are present
    """
    response = test_client.get('/bureaucracy/')
    for stage in [b'stage-submit', b'stage-classify', b'stage-route', b'stage-review', b'stage-close']:
        assert stage in response.data


def test_simulator_page_contains_ot_phrase_keys(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/bureaucracy/' page is requested (GET)
    THEN check that OT ontology category keys are present in the embedded phrase bank
    """
    response = test_client.get('/bureaucracy/')
    for key in [b'safety_constraint', b'vendor_lock', b'change_control', b'downtime']:
        assert key in response.data


def test_simulator_page_contains_audit_trail(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/bureaucracy/' page is requested (GET)
    THEN check that the audit trail container is present
    """
    response = test_client.get('/bureaucracy/')
    assert b'audit-trail' in response.data
    assert b'audit-list' in response.data