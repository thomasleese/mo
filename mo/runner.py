from difflib import SequenceMatcher
import select
import subprocess

from .io import Urgency, Markup, Format


class UndefinedVariableError(ValueError):
    pass


class Variable:
    def __init__(self, name, default=None, value=None):
        self.name = name
        self.default = default
        self._value = value or self.default

    @property
    def value(self):
        if self._value is None:
            raise UndefinedVariableError(self.name)
        return self._value

    def __str__(self):
        return self.value


def load_variables(configuration, values):
    """
    Load variables from a dictionary-based configuration.

    Parameters
    ----------
    configuration : dict
        The configuration to load the variables from.
    values : dict
        Values to replace the default variable value with.

    Returns
    -------
    dict
        A dictionary mapping variable names with variables.
    """

    variables = {}

    for name, conf in configuration.items():
        default = conf.get('default')
        value = values.get(name)
        variables[name] = Variable(name, default, value)

    return variables


class Task:
    default_descriptions = {
        'bootstrap': 'Resolve all dependencies that an application requires to run.',
        'test': 'Run the tests.',
        'ci': 'Run the tests in an environment suitable for continous integration.',
        'console': 'Launch a console for the application.',
        'server': 'Launch the application server locally.',
        'setup': 'Setup the application for the first time after cloning.',
        'update': 'Update the application to run for its current checkout.',
        'deploy': 'Deploy the application to production.',
        'lint': 'Check the application for linting errors, this task is likely to be called by the test task.',
        'release': 'Make a new release of the software.',
        'docs': 'Generate the documentation.'
    }

    def __init__(self, name, configuration, global_variables, given_variables):
        self.name = name

        self.description = configuration.get('description')
        if self.description is None:
            try:
                self.description = self.default_descriptions[name]
            except KeyError:
                raise ValueError('Task must have a description.')

        command_template = configuration['command']

        local_variables = load_variables(configuration.get('variables', {}),
                                         given_variables)

        self.variables = {**local_variables, **global_variables}

        self.commands = command_template.format(**self.variables).split('\n')

        self.after = configuration.get('after', [])

    def run_pre(self, runner):
        for task in self.after:
            runner.run_task(task)

    def run(self, runner):
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
                raise TaskError('Process exited with code: {}'
                                .format(process.returncode))

    def run_post(self, runner):
        pass


class TaskError(RuntimeError):
    pass


class NoSuchTaskError(KeyError):
    def __init__(self, similarities):
        self.similarities = similarities


class HelpTask(Task):
    def __init__(self, given_variables):
        self.name = 'help'
        self.description = 'Show help about a task.'
        self.after = []

        self.variables = {
            'topic': Variable('topic', value=given_variables.get('topic'))
        }

        self.topic = self.variables['topic']

    def run(self, runner):
        task = runner.tasks[self.topic.value]

        text = '# {}\n'.format(task.name)
        text += '\n'
        text += task.description
        text += '\n\n'
        text += 'Variables: {}' \
            .format(', '.join(task.variables))

        runner.io.output(Urgency.normal, Markup.plain, Format.markdown, text)


class Runner:
    def __init__(self, configuration, variables, io):
        self.tasks = {'help': HelpTask(variables)}
        self.variables = load_variables(configuration.get('variables', {}),
                                        variables)
        self.io = io

        for name, task in configuration['tasks'].items():
            try:
                task = Task(name, task, self.variables, variables)
            except ValueError as e:
                self.io.output(Urgency.warning, Markup.plain, Format.text,
                               "Error while loading task '{}': {}"
                               .format(name, repr(e)))
                self.io.output(Urgency.normal, Markup.separator, Format.text,
                               '')
            else:
                self.tasks[name] = task

        self.tasks_run = []

    def run(self, name):
        self.run_task(name)

    def help(self):
        for task in self.tasks.values():
            self.io.output(Urgency.normal, Markup.stage, Format.text,
                           task.name)
            self.io.output(Urgency.normal, Markup.progress,
                           Format.markdown, task.description)

    def find_task(self, name):
        try:
            return self.tasks[name]
        except KeyError:
            pass

        similarities = []

        for task_name, task in self.tasks.items():
            ratio = SequenceMatcher(None, name, task_name).ratio()
            if ratio >= 0.75:
                similarities.append(task)

        if len(similarities) == 1:
            return similarities[0]
        else:
            raise NoSuchTaskError(similarities)

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

            task.run_pre(self)
            self.tasks_run.append(name)

            self.io.output(Urgency.normal, Markup.stage, Format.text,
                           'Running task: {}'.format(task.name))

            task.run(self)

            task.run_post(self)
