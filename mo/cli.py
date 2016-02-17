from argparse import ArgumentParser

import yaml

from .runner import Runner


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
    parser.add_argument('tasks', metavar='task', nargs='+')
    args = parser.parse_args()

    with open(args.file) as file:
        configuration = yaml.load(file.read())

    variables = parse_variables(args.variables)

    runner = Runner(configuration, variables)

    for task in args.tasks:
        runner.run_task(task)
