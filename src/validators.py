import os
from argparse import Action


class FileExistValidator(Action):
    def __call__(self, parser, namespace, values, option_string=None):
        for value in values:
            if not os.path.exists(value):
                parser.error(f"File does not exists: {value}")
        setattr(namespace, self.dest, values)
