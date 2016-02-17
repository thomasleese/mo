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
    parser.add_argument('task', nargs='?')
    args, extra_args = parser.parse_known_args()

    with open(args.file) as file:
        configuration = yaml.load(file.read())

    variables = parse_variables(args.variables)

    runner = Runner(configuration, variables)

    if args.task is not None:
        runner.run_task(args.task, extra_args)
    else:
        print()
        for task in runner.tasks.values():
            print('', task.name, '-', task.description,
                  '({})'.format(','.join(task.required_variables)))
