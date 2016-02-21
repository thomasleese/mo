from enum import Enum
import json
import sys

import colorama
from colorama import Fore, Style

from .project import CommandStep, HelpStep, StepCollection, Task, Variable, VariableCollection
from .runner import Event


class Frontend:
    def begin(self):
        pass

    def end(self):
        pass

    def output(self, event):
        pass


class Debug(Frontend):
    def output(self, event):
        print(event)


class Human(Frontend):
    def begin(self):
        colorama.init()

    def end(self):
        print()

    def output(self, event):
        character_style = Fore.BLUE + Style.BRIGHT

        if event.name == 'RunningTask':
            print()
            character = 'λ'
            text = 'Running task: {}{}'.format(Style.NORMAL,
                                               event.args['task'].name)
            text_style = Style.BRIGHT
        elif event.name == 'SkippingTask':
            print()
            character = 'λ'
            character_style = Fore.YELLOW + Style.BRIGHT
            text = 'Skipping task: {}{}'.format(Style.NORMAL,
                                                event.args['name'])
            text_style = Style.DIM
        elif event.name == 'RunningCommand':
            character = '>'
            text = 'Executing: {}{}'.format(Style.NORMAL,
                                            event.args['command'])
            text_style = Style.BRIGHT
        elif event.name == 'CommandOutput':
            character = ' '
            text = event.args['output']
            text_style = Style.DIM
            if event.args['pipe'] == 'stderr':
                text_style += Fore.RED
        elif event.name == 'UndefinedVariableError':
            character = '!'
            character_style = Fore.RED + Style.BRIGHT
            text = 'Undefined variable: {}'.format(event.args['variable'])
            text_style = Fore.RED
        elif event.name == 'HelpStepOutput':
            print()
            for line in event.args['output'].splitlines():
                print('', line)
            return
        else:
            return

        print(' {}{}{} {}{}{}'.format(
            character_style, character, Style.RESET_ALL,
            text_style, text, Style.RESET_ALL
        ))


class SerialisingFrontend(Frontend):
    def serialise(self, obj):
        if isinstance(obj, (list, VariableCollection, StepCollection)):
            return [self.serialise(element) for element in obj]
        elif isinstance(obj, dict):
            return {k: self.serialise(v) for k, v in obj.items()}
        elif isinstance(obj, str):
            return obj
        elif isinstance(obj, Event):
            return {'name': obj.name, 'args': self.serialise(obj.args)}
        elif isinstance(obj, Task):
            return self.serialise(obj._asdict())
        elif isinstance(obj, Variable):
            return self.serialise(obj._asdict())
        elif isinstance(obj, CommandStep):
            return {'type': 'command', 'command': obj.command}
        elif isinstance(obj, HelpStep):
            return {'type': 'help'}
        elif obj is None:
            return None
        else:
            raise TypeError(type(obj))


class Json(SerialisingFrontend):
    def output(self, event):
        print(json.dumps(self.serialise(event)))


MAPPINGS = {
    'human': Human,
    'debug': Debug,
    'json': Json
}
