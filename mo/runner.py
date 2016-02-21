from collections import namedtuple
import select
import subprocess

from .project import NoSuchTaskError, Step


class StopTask(StopIteration):
    pass


Event = namedtuple('Event', ['name', 'args'])


def make_event(event, **kwargs):
    """A convenience function to make an Event."""

    return Event(event, kwargs)


# all the events are definied here
def ResolvingTaskVariablesEvent(variables):
    return make_event('ResolvingTaskVariables', variables=variables)


def UndefinedVariableErrorEvent(variable):
    return make_event('UndefinedVariableError', variable=variable)


def UnknownStepTypeErrorEvent(step):
    return make_event('UnknownStepTypeError', step=step)


def FindingTaskEvent(name):
    return make_event('FindingTask', name=name)


def StartingTaskEvent(task):
    return make_event('StartingTask', task=task)


def RunningTaskEvent(task):
    return make_event('RunningTask', task=task)


def SkippingTaskEvent(name):
    return make_event('SkippingTask', name=name)


def RunningStepEvent(step):
    return make_event('RunningStep', step=step)


def FinishedTaskEvent(task):
    return make_event('FinishedTask', task=task)


def HelpEvent(project):
    return make_event('Help', project=project)


def HelpStepOutputEvent(output):
    return make_event('HelpStepOutput', output=output)


def CommandOutputEvent(pipe, output):
    return make_event('CommandOutput', pipe=pipe, output=output)


def RunningCommandEvent(command):
    return make_event('RunningCommand', command=command)


def TaskNotFoundEvent(name, similarities):
    return make_event('TaskNotFound', name=name, similarities=similarities)

class Runner:
    """A runner takes a project and some variables and runs it."""

    def __init__(self, project, variables):
        self.project = project
        self.variables = variables

        self.tasks_run = []
        self.task_queue = []

    def run(self):
        """Run any queued tasks."""

        for name in self.task_queue:
            yield from self.run_task(name)

    def help(self):
        """Run a help event."""

        yield HelpEvent(self.project)

    def queue_task(self, name):
        """Queue a task for execution."""

        self.task_queue.append(name)

    def find_task(self, name):
        """Find a task by name."""

        return self.project.find_task(name)

    def resolve_variables(self, task):
        """
        Resolve task variables based on input variables and the default
        values.

        Raises
        ------
        LookupError
            If a variable is missing.
        """

        variables = {**task.variables, **self.project.variables}

        values = {}

        for variable in variables.values():
            value = self.variables.get(variable.name) or variable.default
            if value is None:
                raise LookupError(variable)
            values[variable.name] = value

        return values

    def run_command_step(self, task, step, variables):
        """Run a command step."""

        command = step.args.format(**variables)

        yield RunningCommandEvent(command)

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
                        yield CommandOutputEvent('stdout', line)
                if fd == process.stderr.fileno():
                    line = process.stderr.readline().strip()
                    if line:
                        yield CommandOutputEvent('stderr', line)

            if process.poll() != None:
                break

        for line in process.stdout.readlines():
            line = line.strip()
            if line:
                yield CommandOutputEvent('stdout', line)

        for line in process.stderr.readlines():
            line = line.strip()
            if line:
                yield CommandOutputEvent('stderr', line)

        if process.returncode != 0:
            yield CommandFailed(process.returncode)
            raise StopTask

    def run_help_step(self, task, step, variables):
        """Run a help step."""

        task_name = step.args or variables['task']

        try:
            task = self.project.find_task(task_name)
        except NoSuchTaskError as e:
            yield TaskNotFoundEvent(task_name, e.similarities)
            raise StopTask

        text = '# {}\n'.format(task.name)
        text += '\n'
        text += task.description
        text += '\n\n'
        text += 'Variables: {}' \
            .format(', '.join(task.variables))

        yield HelpStepOutputEvent(text)

    def run_task(self, name):
        """Run a task."""

        if name in self.tasks_run:
            yield SkippingTaskEvent(name)
        else:
            yield FindingTaskEvent(name)
            try:
                task = self.find_task(name)
            except NoSuchTaskError as e:
                yield TaskNotFoundEvent(name, e.similarities)
                raise StopTask

            yield StartingTaskEvent(task)

            for name in task.dependencies:
                yield from self.run_task(name)

            self.tasks_run.append(name)

            yield RunningTaskEvent(task)

            for step in task.steps:
                yield RunningStepEvent(step)

                try:
                    variables = self.resolve_variables(task)
                except LookupError as e:
                    yield UndefinedVariableErrorEvent(e.args[0])
                    raise StopTask

                if step.type == 'help':
                    yield from self.run_help_step(task, step, variables)
                elif step.type == 'command':
                    yield from self.run_command_step(task, step, variables)
                else:
                    yield UnknownStepTypeErrorEvent(step)
                    raise StopTask

            yield FinishedTaskEvent(task)
