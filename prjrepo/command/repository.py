"""Command repository manager."""

from abc import abstractmethod
import os
import yaml

import prjrepo.command as cmd


class CommandRepository(object):
    """Interface for the command repository. Specifies methods to create, list,
    retrieve, and update commands.
    """
    @abstractmethod
    def get_command(self, name):
        """Retrieve specification for command with given name.

        Raises ValueError if no command with given name exists.

        Parameters
        ----------
        name: string
            Command name

        Returns
        -------
        Command
        """
        pass

    @abstractmethod
    def list_commands(self):
        """Get a list of commands that are registered in the repository.

        Returns
        -------
        list(string)
        """


class DefaultCommandRepository(CommandRepository):
    """Default implementation for the command repository. Command specifications
    are stored as files in a single directory. The file format is Yaml.
    """

    COMMAND_SPEC_SUFFIX = '.yaml'

    def __init__(self, base_dir):
        """Initialize the directory that contains the command specifications.

        Raises ValueError if base_dir does not exist or is not a directory.

        Parameter
        ---------
        base_dir: string
            Path to directory containing command specifications.
        """
        if not os.path.isdir(base_dir):
            raise ValueError('not a valid directory \'' + base_dir + '\'')
        self.base_dir = base_dir

    def get_command(self, name):
        """Retrieve specification for command with given name.

        Raises ValueError if no command with given name exists.

        Parameters
        ----------
        name: string
            Command name

        Returns
        -------
        Command
        """
        f_name = os.path.join(self.base_dir, name + self.COMMAND_SPEC_SUFFIX)
        if not os.path.isfile(f_name):
            print f_name
            raise ValueError('unknown command \'' + name + '\'')
        # Read the command specification in Yaml format
        with open(f_name, 'r') as f:
            doc = yaml.load(f.read())
        # Generate list of command elements (idependent of command type)
        elements = []
        for el in doc['spec']['elements']:
            if el['type'] == cmd.COMMAND_ELEMENT_CONST:
                elements.append(cmd.ConstantElement(el['value']))
            elif el['type'] == cmd.COMMAND_ELEMENT_VAR:
                if el['vartype'] == cmd.VARIABLE_TYPE_VALUE:
                    elements.append(
                        cmd.VariableElement(el['vartype'], el['value'])
                    )
                elif el['vartype'] in cmd.VARIABLE_IO_TYPES:
                    elements.append(
                        cmd.VariableIOElement(
                            el['vartype'],
                            el['value'],
                            el['isInput']
                        )
                    )
                else:
                    raise RuntimeError('unknown variable type \'' + el['vartype'] + '\'')
            else:
                raise RuntimeError('unknown element type \'' + el['type'] + '\'')
        if doc['type'] == cmd.COMMAND_TYPE_EXEC:
            return cmd.ExecCommand(name, elements, None)
        elif doc['type'] == cmd.COMMAND_TYPE_SQL:
            return cmd.SQLCommand(name, elements, None)
        else:
            raise RuntimeError('unknown command type \'' + doc['vartype'] + '\'')

    def list_commands(self):
        """Get a list of commands that are registered in the repository.

        Returns
        -------
        list(string)
        """
        commands = []
        for f_name in os.listdir(self.base_dir):
            if f_name.endswith(self.COMMAND_SPEC_SUFFIX):
                commands.append(f_name[:-len(self.COMMAND_SPEC_SUFFIX)].lower())
        return commands
