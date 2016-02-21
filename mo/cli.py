from argparse import ArgumentParser
from pathlib import Path
import sys

import yaml

from .frontend import MAPPINGS as FRONTEND_MAPPINGS
from .project import Project
from .runner import Runner


def parse_variables(args):
    """
    Parse variables as passed on the command line.

    Returns
    -------
    dict
        Mapping variable name to the value.
    """

    variables = {}

    if args is not None:
        for variable in args:
            tokens = variable.split('=')
            name = tokens[0]
            value = '='.join(tokens[1:])
            variables[name] = value

    return variables


def main():
    """Run the CLI."""

    parser = ArgumentParser()
    parser.add_argument('-f', '--file', default='mo.yaml')
    parser.add_argument('-v', '--var', dest='variables', nargs='*')
    parser.add_argument('--frontend', default='human',
                        choices=FRONTEND_MAPPINGS.keys())
    parser.add_argument('tasks', metavar='task', nargs='*')
    args = parser.parse_args()

    with open(args.file) as file:
        configuration = yaml.load(file.read())

    project = Project(configuration, Path(args.file).resolve().parent)

    variables = parse_variables(args.variables)

    runner = Runner(project, variables)

    if args.tasks:
        for task in args.tasks:
            runner.queue_task(task)

        func = runner.run
    else:
        func = runner.help

    frontend = FRONTEND_MAPPINGS[args.frontend]()

    frontend.begin()

    for event in func():
        frontend.output(event)

    frontend.end()
