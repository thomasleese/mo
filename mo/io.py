from enum import Enum
import json
import sys

import colorama


class Urgency(Enum):
    normal = 'normal'
    warning = 'warning'
    error = 'error'


class Markup(Enum):
    plain = 'plain'
    stage = 'stage'
    progress = 'progress'
    separator = 'separator'


class Format(Enum):
    text = 'text'
    markdown = 'markdown'
    unknown = 'unknown'


class InputOutput:
    def begin(self):
        pass

    def end(self):
        pass

    def output(self, urgency, markup, format, content):
        pass


class Human(InputOutput):
    def begin(self):
        colorama.init()
        print()

    def end(self):
        print()

    def get_prefix(self, urgency, markup, format):
        s = ' '

        s += colorama.Fore.BLUE
        s += colorama.Style.BRIGHT

        if markup == Markup.stage:
            s += 'λ '
        elif markup == Markup.progress:
            s += '> '
        else:
            s += '  '

        if urgency == Urgency.normal:
            s += colorama.Fore.BLACK
        if urgency == Urgency.warning:
            s += colorama.Fore.YELLOW
        elif urgency == Urgency.error:
            s += colorama.Fore.RED

        if markup != Markup.stage:
            s += colorama.Style.NORMAL

        if format == Format.unknown:
            s += colorama.Style.DIM

        return s

    def get_suffix(self, urgency, markup, format):
        return colorama.Style.RESET_ALL

    def output(self, urgency, markup, format, content):
        lines = content.splitlines()

        if markup == Markup.separator:
            lines.append('')

        prefix = self.get_prefix(urgency, markup, format)
        suffix = self.get_suffix(urgency, markup, format)

        for line in lines:
            print('{}{}{}'.format(prefix, line, suffix))


class Json(InputOutput):
    def __call__(self, urgency, markup, format, content):
        print(json.dumps({'urgency': urgency.value, 'markup': markup.value,
                          'format': format.value, 'content': content}))


MAPPINGS = {
    'human': Human,
    'json': Json
}
