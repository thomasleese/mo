"""Contains all the events that may come from steps."""

from collections import namedtuple


Event = namedtuple('Event', ['name', 'args'])


def invalid_mofile(filename):
    return Event('InvalidMofile', {'filename': filename})


def undefined_variable(variable):
    return Event('UndefinedVariable', {'variable': variable})


def unknown_step_type(step):
    return Event('UnknownStepType', {'step': step})


def finding_task(name):
    return Event('FindingTask', {'name': name})


def starting_task(task):
    return Event('StartingTask', {'task': task})


def running_task(task):
    return Event('RunningTask', {'task': task})


def skipping_task(name):
    return Event('SkippingTask', {'name': name})


def running_step(step):
    return Event('RunningStep', {'step': step})


def finished_task(task):
    return Event('FinishedTask', {'task': task})


def help(project):
    return Event('Help', {'tasks': project.tasks})


def help_output(output):
    return Event('HelpOutput', {'output': output})


def command_output(pipe, output):
    return Event('CommandOutput', {'pipe': pipe, 'output': output})


def command_failed(command, code, description):
    return Event('CommandFailed', {
        'command': command, 'code': code, 'description': description,
    })


def running_command(command):
    return Event('RunningCommand', {'command': command})


def task_not_found(name, similarities):
    return Event('TaskNotFound', {'name': name, 'similarities': similarities})
