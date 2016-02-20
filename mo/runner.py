import select
import subprocess

from .io import Urgency, Markup, Format
from .project import NoSuchTaskError, HelpStep, CommandStep


class UndefinedVariableError(ValueError):
    pass


class TaskError(RuntimeError):
    pass


class Runner:
    def __init__(self, project, variables, io):
        self.project = project
        self.variables = variables
        self.io = io

        self.tasks_run = []

    def run(self, name):
        self.run_task(name)

    def help(self):
        for task in self.project.tasks.values():
            self.io.output(Urgency.normal, Markup.stage, Format.text,
                           task.name)
            self.io.output(Urgency.normal, Markup.progress,
                           Format.markdown, task.description)

    def find_task(self, name):
        return self.project.find_task(name)

    def resolve_variables(self, task):
        variables = {**task.variables, **self.project.variables}

        values = {}

        for variable in variables.values():
            value = self.variables.get(variable.name) or variable.default
            if value is None:
                raise UndefinedVariableError(variable.name)
            values[variable.name] = value

        return values

    def run_command_step(self, task, step):
        variables = self.resolve_variables(task)
        command = step.command.format(**variables)

        self.io.output(Urgency.normal, Markup.progress,
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
                        self.io.output(Urgency.normal,
                                         Markup.plain,
                                         Format.unknown, line)
                if fd == process.stderr.fileno():
                    line = process.stderr.readline().strip()
                    if line:
                        self.io.output(Urgency.error, Markup.plain,
                                         Format.unknown, line)

            if process.poll() != None:
                break

        for line in process.stdout.readlines():
            line = line.strip()
            if line:
                self.io.output(Urgency.normal, Markup.plain,
                                 Format.unknown, line)

        for line in process.stderr.readlines():
            line = line.strip()
            if line:
                self.io.output(Urgency.error, Markup.plain,
                                 Format.unknown, line)

        if process.returncode != 0:
            self.io.output(Urgency.error, Markup.plain,
                             Format.text,
                             'Process did not exit successfully.')
            raise TaskError('Process exited with code: {}'
                            .format(process.returncode))

    def run_help_step(self, task, step):
        variables = self.resolve_variables(task)
        task = self.project.find_task(variables['task'])

        text = '# {}\n'.format(task.name)
        text += '\n'
        text += task.description
        text += '\n\n'
        text += 'Variables: {}' \
            .format(', '.join(task.variables))

        self.io.output(Urgency.normal, Markup.plain, Format.markdown, text)

    def run_task(self, name):
        if name in self.tasks_run:
            self.io.output(Urgency.normal, Markup.stage, Format.text,
                           'Running task: {}'.format(name))
            self.io.output(Urgency.warning, Markup.plain, Format.text,
                           'Already run.')
        else:
            try:
                task = self.find_task(name)
            except NoSuchTaskError as e:
                self.io.output(Urgency.normal, Markup.stage, Format.text,
                               'Running task: {}'.format(name))
                self.io.output(Urgency.error, Markup.plain, Format.text,
                               'No such task exists.')
                if e.similarities:
                    names = ', '.join(task.name for task in e.similarities)
                    self.io.output(Urgency.warning, Markup.plain, Format.text,
                                   'Did you mean: {}'.format(names))
                raise TaskError

            for name in task.dependencies:
                self.run_task(name)

            self.tasks_run.append(name)

            self.io.output(Urgency.normal, Markup.stage, Format.text,
                           'Running task: {}'.format(task.name))

            for step in task.steps:
                if isinstance(step, HelpStep):
                    self.run_help_step(task, step)
                elif isinstance(step, CommandStep):
                    self.run_command_step(task, step)
