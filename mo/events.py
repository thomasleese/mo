"""Contains all the events that may come from steps."""

from collections import namedtuple


Event = namedtuple('Event', ['name', 'args'])


def invalid_mofile(filename):
    return Event('InvalidMofile', {'filename': filename})


def resolving_task_variables(variables):
    return Event('ResolvingTaskVariables', {'variables': variables})


def undefined_variable_error(variable):
    return Event('UndefinedVariableError', {'variable': variable})


def unknown_step_type_error(step):
    return Event('UnknownStepTypeError', {'step': step})


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


def help_step_output(output):
    return Event('HelpStepOutput', {'output': output})


def command_output(pipe, output):
    return Event('CommandOutput', {'pipe': pipe, 'output': output})


def command_failed(command, exit_code):
    common_descriptions = {
        1: f'Details on how the command failed should be available above.',
        127: f'The command cannot be found.\nPerhaps installing {command[0]} would help.'
    }

    return Event('CommandFailedEvent', {
        'command': command,
        'code': exit_code,
        'description': common_descriptions.get(exit_code),
    })


def running_command(command):
    return Event('RunningCommand', {'command': command})


def task_not_found(name, similarities):
    return Event('TaskNotFound', {'name': name, 'similarities': similarities})
