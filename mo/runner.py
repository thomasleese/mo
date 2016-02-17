import select
import subprocess

import jinja2
import jinja2.meta

from .io import Urgency, Markup, Format


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

        env = jinja2.Environment()
        ast = env.parse(configuration['command'])
        self.required_variables = jinja2.meta.find_undeclared_variables(ast)

        command_template = jinja2.Template(configuration['command'])
        self.commands = command_template.render(variables).split('\n')

        self.after = configuration.get('after', [])

    def run(self, runner, args):
        for task in self.after:
            runner.run_task(task, args)

        runner.io.output(Urgency.normal, Markup.stage, Format.text,
                         'Running task: {}'.format(self.name))

        for command in self.commands:
            runner.io.output(Urgency.normal, Markup.progress,
                             Format.text, 'Executing: {}'.format(command))

            process = subprocess.Popen(command, shell=True,
                                       universal_newlines=True, bufsize=1,
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE)

            while True:
                reads = [process.stdout.fileno(), process.stderr.fileno()]
                ret = select.select(reads, [], [])

                for fd in ret[0]:
                    if fd == process.stdout.fileno():
                        line = process.stdout.readline().strip()
                        if line:
                            runner.io.output(Urgency.normal,
                                             Markup.plain,
                                             Format.unknown, line)
                    if fd == process.stderr.fileno():
                        line = process.stderr.readline().strip()
                        if line:
                            runner.io.output(Urgency.error, Markup.plain,
                                             Format.unknown, line)

                if process.poll() != None:
                    break

            for line in process.stdout.readlines():
                line = line.strip()
                if line:
                    runner.io.output(Urgency.normal, Markup.plain,
                                     Format.unknown, line)

            for line in process.stderr.readlines():
                line = line.strip()
                if line:
                    runner.io.output(Urgency.error, Markup.plain,
                                     Format.unknown, line)

            if process.returncode != 0:
                runner.io.output(Urgency.error, Markup.plain,
                                 Format.text,
                                 'Process did not exit successfully.')
                raise RuntimeError('Process exited with code: {}'
                                   .format(process.returncode))


class HelpTask(Task):
    def __init__(self):
        self.name = 'help'
        self.description = 'Show help about a task.'
        self.required_variables = []

    def run(self, runner, args):
        for name in args:
            task = runner.tasks[name]

            text = '# {}\n'.format(name)
            text += task.description

            runner.io.output(Urgency.normal, Markup.plain,
                             Format.markdown, text)


class Runner:
    def __init__(self, configuration, variables, io):
        self.tasks = {'help': HelpTask()}
        self.variables = {}
        self.io = io

        for name, variable in configuration.get('variables', {}).items():
            try:
                value = variables.pop(name)
            except KeyError:
                value = None

            self.variables[name] = Variable(name, variable, value)

        for name, task in configuration['tasks'].items():
            self.tasks[name] = Task(name, task, self.variables)

        if variables:
            keys = ', '.join(list(variables.keys()))
            self.io.output(Urgency.warning, Markup.plain, Format.text,
                           'Unknown variables: {}'.format(keys))
            self.io.output(Urgency.normal, Markup.separator, Format.text, '')

        self.tasks_run = []

    def run(self, name, args):
        self.run_task(name, args)

    def help(self):
        for task in self.tasks.values():
            self.io.output(Urgency.normal, Markup.stage, Format.text,
                           task.name)
            self.io.output(Urgency.normal, Markup.progress,
                           Format.markdown, task.description)

    def run_task(self, name, args):
        if name in self.tasks_run:
            self.io.output(Urgency.warning, Markup.stage, Format.text,
                           'Already run task: {}'.format(name))
        else:
            self.tasks_run.append(name)
            self.tasks[name].run(self, args)
