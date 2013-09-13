"""
Bottle routes
"""
import json
import os

import util
from bottle import abort, request, route, static_file

# Static file paths
CLASSES = os.path.join(os.path.dirname(__file__), 'classes')
CSS = os.path.join(os.path.dirname(__file__), 'css')
IMG = os.path.join(os.path.dirname(__file__), 'img')
JS = os.path.join(os.path.dirname(__file__), 'js')
TEMPLATES = os.path.join(os.path.dirname(__file__), 'templates')

#
# Static file routes
#
@route('/testing/')
def automated_testing():
    """ Serves index file """
    return static_file('testing.html', '')

@route('/testing/data/classes/<filename>')
def css(filename):
    """ Serves all classes files """
    return static_file(filename, root=CLASSES)

@route('/testing/css/<filename>')
def css(filename):
    """ Serves all CSS files """
    return static_file(filename, root=CSS)

@route('/testing/img/<filename>')
def img(filename):
    """ Serves all image files """
    return static_file(filename, root=IMG)

@route('/testing/js/<filename>')
def js(filename):
    """ Serves all JS files """
    return static_file(filename, root=JS)

@route('/testing/data/templates/<filename>')
def css(filename):
    """ Serves all template files """
    return static_file(filename, root=TEMPLATES)

#
# Dynamic routes
#
@route('/testing/json/templates/')
def templates():
    """ Returns all JSON templates. """
    pass

@route('/testing/json/add-template/', method="POST")
def templates():
    """ Convert template into JSON and write to file. """
    pass
