"""Contains all the events that may come from steps."""

from collections import namedtuple
from enum import Enum


class EventKind(Enum):
    unknown = 'unknown'


Event = namedtuple('Event', ['name', 'kind', 'args'])


def invalid_mofile(filename):
    return Event('InvalidMofile', EventKind.unknown, {
        'filename': filename
    })


def undefined_variable(variable):
    return Event('UndefinedVariable', EventKind.unknown, {
        'variable': variable
    })


def unknown_step_type(step):
    return Event('UnknownStepType', EventKind.unknown, {'step': step})


def finding_task(name):
    return Event('FindingTask', EventKind.unknown, {'name': name})


def starting_task(task):
    return Event('StartingTask', EventKind.unknown, {'task': task})


def running_task(task):
    return Event('RunningTask', EventKind.unknown, {'task': task})


def skipping_task(name):
    return Event('SkippingTask', EventKind.unknown, {'name': name})


def running_step(step):
    return Event('RunningStep', EventKind.unknown, {'step': step})


def finished_task(task):
    return Event('FinishedTask', EventKind.unknown, {'task': task})


def help(project):
    return Event('Help', EventKind.unknown, {'tasks': project.tasks})


def help_output(output):
    return Event('HelpOutput', EventKind.unknown, {'output': output})


def command_output(pipe, output):
    return Event('CommandOutput', EventKind.unknown, {
        'pipe': pipe, 'output': output
    })


def command_failed(command, code, description):
    return Event('CommandFailed', EventKind.unknown, {
        'command': command, 'code': code, 'description': description,
    })


def running_command(command):
    return Event('RunningCommand', EventKind.unknown, {'command': command})


def task_not_found(name, similarities):
    return Event('TaskNotFound', EventKind.unknown, {
        'name': name, 'similarities': similarities
    })
