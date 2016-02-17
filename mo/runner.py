import subprocess

import jinja2


class Variable:
    def __init__(self, name, configuration, value=None):
        self.name = name
        self.default = configuration['default']
        self.value = value or self.default

    def __str__(self):
        return self.value


class Task:
    def __init__(self, name, configuration, variables):
        self.name = name
        self.description = configuration['description']

        command_template = jinja2.Template(configuration['command'])
        self.commands = command_template.render(variables).split('\n')

        self.after = configuration.get('after', [])

    def run(self, runner):
        for task in self.after:
            runner.run_task(task)

        for command in self.commands:
            print('>', command)
            subprocess.run(command, shell=True, check=True)


class Runner:
    def __init__(self, configuration, variables):
        self.tasks = {}
        self.variables = {}

        for name, variable in configuration['variables'].items():
            try:
                value = variables.pop(name)
            except KeyError:
                value = None

            self.variables[name] = Variable(name, variable, value)

        for name, task in configuration['tasks'].items():
            self.tasks[name] = Task(name, task, self.variables)

        if variables:
            print('unused variables:', variables)

        self.tasks_run = []

    def run_task(self, name):
        if name in self.tasks_run:
            print('Already run:', name)
        else:
            print('Running task:', name)
            self.tasks_run.append(name)
            self.tasks[name].run(self)
