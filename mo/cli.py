"""Utilities for working with the command line interface."""

from argparse import ArgumentParser

from . import events, frontends, mofile
from .runner import Runner


available_frontends = {
    'human': frontends.Human,
    'debug': frontends.Debug,
    'json': frontends.Json
}


def parse_variables(args):
    """
    Parse variables as passed on the command line.

    Returns
    -------
    dict
        Mapping variable name to the value.
    """

    if args is None:
        return {}

    def parse_variable(string):
        tokens = string.split('=')
        name = tokens[0]
        value = '='.join(tokens[1:])
        return name, value

    return {
        name: value
        for name, value in (parse_variable(v) for v in args)
    }


def parse_args():
    parser = ArgumentParser()
    parser.add_argument('-f', '--file', default='Mofile')
    parser.add_argument('-v', '--var', dest='variables', nargs='*')
    parser.add_argument('--frontend', default='human',
                        choices=available_frontends.keys())
    parser.add_argument('tasks', metavar='task', nargs='*')
    return parser.parse_args()


def run(args):
    try:
        project = mofile.load(args.file)
    except FileNotFoundError:
        yield events.invalid_mofile(args.file)
        return
    except mofile.InvalidMofileFormat:
        yield events.invalid_mofile(args.file)
        return

    variables = parse_variables(args.variables)

    runner = Runner(project, variables)

    if args.tasks:
        for task in args.tasks:
            runner.queue_task(task)

        yield from runner.run()
    else:
        yield from runner.help()


def main():
    """Run the CLI."""

    args = parse_args()

    frontend = available_frontends[args.frontend]()

    frontend.begin()

    try:
        for event in run(args):
            frontend.output(event)
    finally:
        frontend.end()
