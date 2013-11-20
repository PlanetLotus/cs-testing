import unittest
import os, sys

# This isn't the Python way, but I couldn't figure out another way
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import routes

class TestTemplate(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def test_add_template(self):
        self.assertEqual(0, 0)
