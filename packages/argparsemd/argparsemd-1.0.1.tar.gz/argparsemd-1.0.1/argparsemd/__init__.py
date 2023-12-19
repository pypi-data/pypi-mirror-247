#  argparsemd, a python package that adds markdown help to an ArgumentParser
#
# (C) 2023 Michel Anders (varkenvarken)
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#  Version: 20231218154330

from argparse import ArgumentParser, Action, HelpFormatter, SUPPRESS
from typing import Sequence

class MarkdownHelpFormatter(HelpFormatter):
    def format_help(self):
        self._root_section.heading = f"# {self._prog}"
        return super().format_help()

    def add_usage(self, usage, actions, groups, prefix=None):
        if usage is not SUPPRESS:
            self.add_text("")
            self.add_text("```")
            super().add_usage(usage, actions, groups, prefix)
            self.add_text("```")

    def start_section(self, heading):
        super().start_section(f"## {heading}")

    # this breaks encapsulation because we override a private method
    # however, the whole HelpFormatter class is insanely complicated
    # with many public methods depending in a complicated way on
    # private methods which makes it very difficult to separate
    # concerns while still being able to customize things. That
    # probably while argparse.py is almost 3000 lines long!
    #
    # so use at own risk, may break in future :-)
    def _format_action(self, action):
        lines = []
        # options in bold, followed by type and default value (if any)
        lines.append(
            f'- {", ".join(["**"+opt+"**" for opt in action.option_strings])}{":"+action.type.__name__ if action.type is not None else ""} {"[" + str(action.default) + "]" if (action.default is not None and action.default != "==SUPPRESS==") else ""}\n'
        )
        # additional help is split into short lines, indented so it groups with the item
        if action.help:
            help_text = self._expand_help(action)
            lines.extend(["  " + line for line in self._split_lines(help_text, 78)])
        lines.extend(["", ""])

        # if there are any sub-actions, add their help as well
        for subaction in self._iter_indented_subactions(action):
            lines.append(self._format_action(subaction))

        return "\n".join(lines)


class MarkdownHelpAction(Action):
    """MD help action"""

    def __init__(
        self,
        option_strings,
        dest=SUPPRESS,
        default=SUPPRESS,
        **kwargs,
    ):
        super().__init__(
            option_strings=option_strings, dest=dest, default=default, nargs=0, **kwargs
        )

    def __call__(self, parser, namespace, values, option_string=None):
        parser.formatter_class = MarkdownHelpFormatter
        parser.print_help()
        parser.exit()


class ArgumentParserMD(ArgumentParser):
    """Object for parsing command line strings into Python objects.

    Automatically adds an option `-md` that will print markdown help.

    Keyword Arguments:
        - prog -- The name of the program (default:
            ``os.path.basename(sys.argv[0])``)
        - usage -- A usage message (default: auto-generated from arguments)
        - description -- A description of what the program does
        - epilog -- Text following the argument descriptions
        - parents -- Parsers whose arguments should be copied into this one
        - formatter_class -- HelpFormatter class for printing help messages
        - prefix_chars -- Characters that prefix optional arguments
        - fromfile_prefix_chars -- Characters that prefix files containing
            additional arguments
        - argument_default -- The default value for all arguments
        - conflict_handler -- String indicating how to handle conflicts
        - add_help -- Add a -h/-help option
        - allow_abbrev -- Allow long options to be abbreviated unambiguously
        - exit_on_error -- Determines whether or not ArgumentParser exits with
            error info when an error occurs
        - markdown_option -- name of the option used to display markdown help
    """

    # note: we don't work with *args, **kwargs here because we want change a single keyword defaul
    # but still keep the signature readable to vscode and the like
    def __init__(
        self,
        prog: str = None,
        usage: str = None,
        description: str = None,
        epilog: str = None,
        parents:Sequence[ArgumentParser]=[],
        formatter_class:HelpFormatter=HelpFormatter,
        prefix_chars:str="-",
        fromfile_prefix_chars:str=None,
        argument_default=None,
        conflict_handler:str="error",
        add_help:bool=True,
        allow_abbrev:bool=True,
        exit_on_error:bool=True,
        markdown_option:str="-md",
    ):
        super().__init__(
            prog=prog,
            usage=usage,
            description=description,
            epilog=epilog,
            parents=parents,
            formatter_class=formatter_class,
            prefix_chars=prefix_chars,
            fromfile_prefix_chars=fromfile_prefix_chars,
            argument_default=argument_default,
            conflict_handler=conflict_handler,
            add_help=add_help,
            allow_abbrev=allow_abbrev,
            exit_on_error=exit_on_error,
        )
        self.add_argument(
            markdown_option,
            action=MarkdownHelpAction,
            help="print Markdown-formatted help text and exit.",
        )
