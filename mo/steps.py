"""Contains all the steps available."""

import select
import shlex
import subprocess

from . import events


class StopTask(StopIteration):
    pass


available_steps = {}


def step(func=None, name=None):
    def decorator(func):
        nonlocal name

        if name is None:
            name = func.__name__

        available_steps[name] = func

        return func

    if func is None:
        return decorator
    else:
        return decorator(func)


def _run_command(command_line):
    command_args = shlex.split(command_line)

    yield events.running_command(command_args)

    process = subprocess.Popen(
        command_line, shell=True, universal_newlines=True, bufsize=1,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )

    streams = ['stdout', 'stderr']

    def send_line(stream, line):
        line = line.strip()
        if line:
            yield events.command_output(stream, line)

    def flush_line(fd, stream):
        if fd == getattr(process, stream).fileno():
            line = getattr(process, stream).readline()
            yield from send_line(stream, line)

    while True:
        reads = [getattr(process, stream).fileno() for stream in streams]
        ret = select.select(reads, [], [])

        for fd in ret[0]:
            for stream in streams:
                flush_line(fd, streams)

        if process.poll() != None:
            break

    def flush_remaining_lines(stream):
        for line in getattr(process, stream).readlines():
            yield from send_line(stream, line)

    for stream in streams:
        yield from flush_remaining_lines(stream)

    if process.returncode != 0:
        yield events.command_failed(command_args, process.returncode)
        raise StopTask


@step
def command(project, task, step, variables):
    command_line = step.args.format(**variables)
    yield from _run_command(command_line)


@step
def help(project, task, step, variables):
    """Run a help step."""

    task_name = step.args or variables['task']

    try:
        task = project.find_task(task_name)
    except NoSuchTaskError as e:
        yield events.task_not_found(task_name, e.similarities)
        raise StopTask

    text = f'# {task.name}\n'
    text += '\n'
    text += task.description
    text += '\n\n'
    text += 'Variables: {}'.format(', '.join(task.variables))

    yield events.help_step_output(text)


@step
def brew(project, task, step, variables):
    package = step.args

    exit_code = subprocess.call(['brew', 'ls', '--versions', package],
                                stdout=subprocess.PIPE)

    if exit_code == 0:
        return

    yield from _run_command(f'brew install {package}')


@step(name='print')
def print_step(project, task, step, variables):
    yield events.command_output('stdout', step.args)
