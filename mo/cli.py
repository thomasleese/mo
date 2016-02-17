from argparse import ArgumentParser

import yaml

from .io import MAPPINGS as IO_MAPPINGS
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
    parser.add_argument('-i', '--io', default='human')
    parser.add_argument('task', nargs='?')
    args, extra_args = parser.parse_known_args()

    with open(args.file) as file:
        configuration = yaml.load(file.read())

    variables = parse_variables(args.variables)

    io = IO_MAPPINGS[args.io]()

    io.begin()

    runner = Runner(configuration, variables, io)

    if args.task is not None:
        runner.run(args.task, extra_args)
    else:
        runner.help()

    io.end()
