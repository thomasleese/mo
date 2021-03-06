"""Contains all the frontends available."""

import json

import colorama
from colorama import Fore, Style

from .events import Event, EventKind
from .project import Step, StepCollection, Task, Variable, VariableCollection


class Frontend:
    """A frontend takes output from the runner and displays it to the user."""

    def begin(self):
        """Begin processing output."""
        pass

    def end(self):
        """End processing output."""
        pass

    def output(self, event):
        """Process a single event."""
        pass


class Debug(Frontend):
    """The debug frontend simply prints the raw events."""

    def output(self, event):
        print(event)


class Human(Frontend):
    """
    The human frontend provides colourful textual output useful for humans
    to read.
    """

    ignored_events = (
        'FindingTask', 'StartingTask', 'RunningStep', 'FinishedTask'
    )

    def indent(self, string, n=1):
        new_lines = []

        for line in string.splitlines():
            new_lines.append(' ' * n + line)

        return '\n'.join(new_lines)

    def begin(self):
        colorama.init()
        print()

    def end(self):
        print()

    def get_character(self, event):
        if event.kind is EventKind.output:
            return ' '
        elif event.kind is EventKind.error:
            return '!'
        elif 'Task' in event.name:
            return 'λ'
        elif 'Command' in event.name:
            return '>'

    def get_character_style(self, event):
        if event.name == 'SkippingTask':
            return Fore.YELLOW
        elif event.kind is EventKind.error:
            return Fore.RED

        return Fore.BLUE

    def get_text_style(self, event):
        if event.name == 'RunningTask':
            return Style.BRIGHT
        elif event.name == 'SkippingTask':
            return Style.DIM
        elif event.name == 'RunningCommand':
            return Style.BRIGHT
        elif event.kind is EventKind.output:
            return Style.DIM
        elif event.kind is EventKind.error:
            return Style.BRIGHT + Fore.RED

    def output(self, event):
        if event.name in self.ignored_events:
            return

        character_style = self.get_character_style(event)
        character = self.get_character(event)
        text_style = self.get_text_style(event)

        if event.name == 'RunningTask':
            text = f'Running task: {Style.NORMAL}{event.args["task"].name}'
        elif event.name == 'SkippingTask':
            text = f'Skipping task: {Style.NORMAL}{event.args["name"]}'
        elif event.name == 'RunningCommand':
            text = f'Executing: {Style.NORMAL}{event.args["command"]}'
        elif event.name == 'CommandOutput':
            text = event.args['output']
            if event.args['pipe'] == 'stderr':
                text_style += Fore.RED
        elif event.name == 'CommandFailed':
            text = f'Command failed with exit code {event.args["code"]}'
            if event.args['description']:
                text += f'{Style.NORMAL}\n{self.indent(event.args["description"], 3)}'
        elif event.name == 'InvalidMofile':
            text = f'Invalid task file: {Style.NORMAL}{event.args["filename"]}'
        elif event.name == 'UndefinedVariable':
            text = f'Undefined variable: {Style.NORMAL}{event.args["variable"]}'
        elif event.name == 'TaskNotFound':
            text = f'No such task: {Style.NORMAL}{event.args["name"]}'
            if event.args['similarities']:
                similarities_str = ', '.join(event.args['similarities'])
                text += f' Did you mean? {similarities_str}'
        elif event.name == 'HelpOutput':
            print()
            for line in event.args['output'].splitlines():
                print('', line)
            return
        elif event.name == 'Help':
            print('Available tasks:')
            print()
            for name, task in event.args['tasks'].items():
                print(name, '-', task.description)
            return
        else:
            character = '?'
            character_style = Fore.YELLOW
            text = f'Unknown event: {Style.NORMAL}{event}'
            text_style = Fore.YELLOW

        character_style += Style.BRIGHT

        print(
            f' {character_style}{character}{Style.RESET_ALL}' +
            f' {text_style}{text}{Style.RESET_ALL}'
        )


class SerialisingFrontend(Frontend):
    """
    A serialising frontend first serialises events into dictionaries before
    outputting.
    """

    def serialise(self, obj):
        """
        Take an object from the project or the runner and serialise it into a
        dictionary.

        Parameters
        ----------
        obj : object
            An object to serialise.

        Returns
        -------
        object
            A serialised version of the input object.
        """

        if isinstance(obj, (list, VariableCollection, StepCollection)):
            return [self.serialise(element) for element in obj]
        elif isinstance(obj, dict):
            return {k: self.serialise(v) for k, v in obj.items()}
        elif isinstance(obj, str):
            return obj
        elif isinstance(obj, (Event, Task, Variable, Step)):
            return self.serialise(obj._asdict())
        elif obj is None:
            return None
        else:
            raise TypeError(type(obj))


class Json(SerialisingFrontend):
    """Display the output as line terminated JSON objects."""

    def output(self, event):
        print(json.dumps(self.serialise(event)))
