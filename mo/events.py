from collections import namedtuple


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


def CommandFailedEvent(exit_code):
    return make_event('CommandFailedEvent', code=exit_code)


def RunningCommandEvent(command):
    return make_event('RunningCommand', command=command)


def TaskNotFoundEvent(name, similarities):
    return make_event('TaskNotFound', name=name, similarities=similarities)
