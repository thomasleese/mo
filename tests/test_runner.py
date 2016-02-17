import unittest

from mo.runner import Variable


class TestVariable(unittest.TestCase):
    def test_default(self):
        v = Variable('name', {'default': 'default'})
        self.assertEqual(v.value, 'default')
        self.assertEqual(str(v), 'default')

    def test_value(self):
        v = Variable('name', {'default': 'default'}, 'value')
        self.assertEqual(v.value, 'value')
        self.assertEqual(str(v), 'value')

    def test_str(self):
        v = Variable('name', {'default': 'abc'})
        self.assertEqual(str(v), v.value)
