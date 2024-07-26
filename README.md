# flask-tymyrddin

[![Coverage](https://img.shields.io/badge/coverage-80%25-green)](https://github.com/tymyrddin/flask-tymyrddin/tree/main/tests)

[![Python flask application](https://github.com/tymyrddin/flask-tymyrddin/actions/workflows/python-app.yml/badge.svg)](https://github.com/tymyrddin/flask-tymyrddin/actions/workflows/python-app.yml) [![Netlify Status](https://api.netlify.com/api/v1/badges/a81949fc-2133-4808-b9a5-ebbad7ed1764/deploy-status)](https://app.netlify.com/sites/tymyrddin/deploys)

## Overview

This Flask application displays at https://tymyrddin.dev/.

## Website

[Frozen-Flask](https://pythonhosted.org/Frozen-Flask/) is
used to generate the static files based on the routes specified in the Flask app.  These static files are hosted on
[Netlify](https://www.netlify.com).

## Requirements

* Python 3.11
* Flask - micro-framework for web application development
* Jinga - templating engine
* Frozen-Flask - generates static files from Flask routes

## Installation Instructions

Pull down the source code from this GitLab repository:

```sh
git clone git@github.com:tymyrddin/flask-tymyrddin.git
```

Create a new virtual environment:

```sh
$ cd flask-tymyrddin
$ python3 -m venv venv
```

Activate the virtual environment:

```sh
$ source venv/bin/activate
```

Install the python packages in requirements.txt:

```sh
(venv) $ pip install -r requirements.txt
```

## Run the Development Server

In the top-level directory, set the file that contains the Flask application and specify that the development environment should be used:

```sh
(venv) $ export FLASK_APP=app.py
(venv) $ export FLASK_ENV=development
```

Run development server to serve the Flask application:

```sh
(venv) $ flask run -p 3000
```

Navigate to 'http://localhost:3000' to view the website!

## Build the Static Files

In the top-level directory, run the build script:

```sh
(venv) $ python build.py
```

The static files are generated in the */project/build/* directory, which can then be hosted on Netlify.

## Testing

To run all the tests:

```sh
(venv) $ pytest -v
```

To check the code coverage of the tests:

```sh
(venv) $ pytest --cov-report term-missing --cov=project
```

