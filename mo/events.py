"""Contains all the events that may come from steps."""

from collections import namedtuple
from enum import Enum


class EventKind(Enum):
    other = 'other'
    error = 'error'
    output = 'output'


Event = namedtuple('Event', ['name', 'kind', 'args'])


def invalid_mofile(filename):
    return Event('InvalidMofile', EventKind.error, {
        'filename': filename
    })


def undefined_variable(variable):
    return Event('UndefinedVariable', EventKind.error, {
        'variable': variable
    })


def unknown_step_type(step):
    return Event('UnknownStepType', EventKind.error, {'step': step})


def finding_task(name):
    return Event('FindingTask', EventKind.other, {'name': name})


def starting_task(task):
    return Event('StartingTask', EventKind.other, {'task': task})


def running_task(task):
    return Event('RunningTask', EventKind.other, {'task': task})


def skipping_task(name):
    return Event('SkippingTask', EventKind.other, {'name': name})


def running_step(step):
    return Event('RunningStep', EventKind.other, {'step': step})


def finished_task(task):
    return Event('FinishedTask', EventKind.other, {'task': task})


def help(project):
    return Event('Help', EventKind.output, {'tasks': project.tasks})


def help_output(output):
    return Event('HelpOutput', EventKind.output, {'output': output})


def command_output(pipe, output):
    return Event('CommandOutput', EventKind.output, {
        'pipe': pipe, 'output': output
    })


def command_failed(command, code, description):
    return Event('CommandFailed', EventKind.error, {
        'command': command, 'code': code, 'description': description,
    })


def running_command(command):
    return Event('RunningCommand', EventKind.other, {'command': command})


def task_not_found(name, similarities):
    return Event('TaskNotFound', EventKind.error, {
        'name': name, 'similarities': similarities
    })
