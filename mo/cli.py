from argparse import ArgumentParser
from pathlib import Path
import sys

import yaml

from .frontend import MAPPINGS as FRONTEND_MAPPINGS
from .project import Project
from .runner import Runner, TaskError


def parse_variables(args):
    variables = {}

    if args is not None:
        for variable in args:
            tokens = variable.split('=')
            name = tokens[0]
            value = '='.join(tokens[1:])
            variables[name] = value

    return variables


def main():
    parser = ArgumentParser()
    parser.add_argument('-f', '--file', default='mo.yaml')
    parser.add_argument('-v', '--var', dest='variables', nargs='*')
    parser.add_argument('--frontend', default='human')
    parser.add_argument('tasks', metavar='task', nargs='*')
    args = parser.parse_args()

    with open(args.file) as file:
        configuration = yaml.load(file.read())

    project = Project(configuration, Path(args.file).resolve().parent)

    variables = parse_variables(args.variables)

    frontend = FRONTEND_MAPPINGS[args.frontend]()

    frontend.begin()

    runner = Runner(project, variables, frontend)

    exit_code = 0

    if args.tasks:
        for task in args.tasks:
            try:
                runner.run(task)
            except TaskError:
                exit_code = 1
                break
    else:
        runner.help()

    frontend.end()

    sys.exit(exit_code)
