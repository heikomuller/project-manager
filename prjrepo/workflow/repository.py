"""Command repository manager."""

from abc import abstractmethod
import os
import yaml

import prjrepo.workflow.command as cmd


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
            raise ValueError('unknown command \'' + name + '\'')
        # Read the command specification in Yaml format
        with open(f_name, 'r') as f:
            doc = yaml.load(f.read())
        # Generate list of command elements (idependent of command type).
        # Expected document structure is:
        # - type: EXEC or SQL
        #   spec:
        #       components:
        #           - type: CONST or VAR
        #             value: string
        #             ioType: FILE or DIR (optional)
        #             asInput: bool (optional)
        components = []
        for el in doc['spec']['components']:
            components.append(
                cmd.CommandComponent(
                    el['type'],
                    el['value'],
                    io_type=el['ioType'] if 'ioType' in el else None,
                    as_input=el['asInput'] if 'asInput' in el else False
                )
            )
        if doc['type'] == cmd.COMMAND_TYPE_EXEC:
            return cmd.ExecCommand(name, components, None)
        elif doc['type'] == cmd.COMMAND_TYPE_SQL:
            return cmd.SQLCommand(name, components, None)
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
