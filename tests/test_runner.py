import unittest

from mo.runner import Task, Variable


class TestVariable(unittest.TestCase):
    def test_default(self):
        v = Variable('name', 'default')
        self.assertEqual(v.value, 'default')
        self.assertEqual(str(v), 'default')

    def test_value(self):
        v = Variable('name', 'default', 'value')
        self.assertEqual(v.value, 'value')
        self.assertEqual(str(v), 'value')

    def test_str(self):
        v = Variable('name', 'abc')
        self.assertEqual(str(v), v.value)


class TestTask(unittest.TestCase):
    def test_variables(self):
        t = Task('name', {'description': '', 'command': '{{ v }}'},
                 {'v': 'variable'})
        self.assertEqual(t.commands[0], 'variable')
