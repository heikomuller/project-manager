"""Objects representing commands that can be executed as part of a project ."""


# ------------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------------

"""Type of components in a command specification."""
COMPONENT_TYPE_CONST = 'CONST'
COMPONENT_TYPE_VAR = 'VAR'
COMPONENT_TYPES = [COMPONENT_TYPE_CONST, COMPONENT_TYPE_VAR]

"""Type identifier for executable commands."""
COMMAND_TYPE_EXEC = 'EXEC'
COMMAND_TYPE_SQL = 'SQL'
COMMAND_TYPES = [COMMAND_TYPE_EXEC, COMMAND_TYPE_SQL]

"""IO component types."""
IO_TYPE_DIR = 'DIR'
IO_TYPE_FILE = 'FILE'
IO_TYPES = [IO_TYPE_DIR, IO_TYPE_FILE]

# ------------------------------------------------------------------------------
# Command Specification
# ------------------------------------------------------------------------------

class Command(object):
    """Specification fpr a command that executes a program or script in the
    context of the current project. Command specifications are composed of four
    parts: (1) the command name, (2) the command type, (3) a list of command
    elements, and (4) a description of the command output.

    There are currently two command types: EXEC and SQL. EXEC refers to an
    external executable and SQL refers to an SQL query statement.

    The command itself is defined as a list of elements that are either string
    constants or references to variables. In case of an EXEC command, the
    concatenation of all elements forms the command line that executes the
    command with all arguments. In case of a SQL command, the concatenation
    of all elements is the SQL statement that is being executed.
    """
    def __init__(self, name, command_type, elements, output_spec):
        """Initialize the components of a command specification.

        Raises ValueError if an invalid command type is given.

        Parameters
        ----------
        name: string
            Command name
        command_type : string
            Command type identifier. Valid type identifier are listed in
            COMMAND_TYPES
        elements: list(CommandComponent)
            List of command elements from which the executable command is being
            generated
        output_spec
        """
        if not command_type in COMMAND_TYPES:
            raise ValueError('invalid command type \'' + command_type + '\'')
        self.name = name
        self.command_type = command_type
        self.elements = elements
        self.output_spec = output_spec

    @property
    def is_exec(self):
        """Flag indicating whther this is an EXEC command.

        Returns
        -------
        bool
        """
        return self.command_type == COMMAND_TYPE_EXEC

    @property
    def is_sql(self):
        """Flag indicating whther this is an SQL command.

        Returns
        -------
        bool
        """
        return self.command_type == COMMAND_TYPE_SQL


class ExecCommand(Command):
    """Specification of a command that runs an external executable."""
    def __init__(self, name, elements, output_spec):
        """Initialize the command element list and output specification.

        Parameters
        ----------
        name: string
            Command name
        elements: list(CommandComponent)
            List of command elements from which the executable command is being
            generated
        output_spec
        """
        super(ExecCommand, self).__init__(
            name,
            COMMAND_TYPE_EXEC,
            elements,
            output_spec
        )


class SQLCommand(Command):
    """Specification for a command that executes a SQL query."""
    def __init__(self, name, elements, output_spec):
        """Initialize the command element list and output specification.

        Parameters
        ----------
        name: string
            Command name
        elements: list(CommandComponent)
            List of command elements from which the SQL statement is being
            generated
        output_spec
        """
        super(SQLCommand, self).__init__(
            name,
            COMMAND_TYPE_SQL,
            elements,
            output_spec
        )


class CommandComponent(object):
    """Component in the specification of an executable command. Componets are
    either constant values or contain references to variables (enclused in
    double square brackets). A command component may identify a file or
    directory (i.e., an IO component).

    For IO components the as_input flag defines whether ther referenced file/
    directory is used as input by the command. Input files do not need to
    exist in the current working directory event if references are relative. The
    system automatically will find the first existing file that matches the
    component value along the path from the current working directory to the
    project repository root.
    """
    def __init__(self, obj_type, value, io_type=None, as_input=False):
        """Initialize the component type and value.

        Raises ValueError if an invalid element type is given. Valid type
        identifier are defined in COMPONENT_TYPES.

        For variable components it is ensured that all variables are properly
        enclosed in double pairs of square brackes.

        The as_input flag is ignored if the component does not reference an IO
        resource.

        Parameters
        ----------
        obj_type: string
            Unique component type identifier
        value: string
            Component value
        io_type: string, optional
            IO type specifications for components that reference files or
            directories
        """
        # Make sure that given component type is valid
        if not obj_type in COMPONENT_TYPES:
            raise ValueError('invalid component type \'' + obj_type + '\'')
        # Make sure that IO type is valie (if given)
        if not io_type is None:
            if not io_type in IO_TYPES:
                raise ValueError('invalid IO type \'' + io_type + '\'')
        # If component type is variable, parse variable values
        if obj_type == COMPONENT_TYPE_VAR:
            self.tokens = []
            val = value
            while '[[' in val:
                i_start = val.find('[[')
                i_end = val.find(']]', i_start)
                if i_end == -1:
                    raise ValueError('invalid variable expression \'' + value + '\'')
                if i_start > 0:
                    self.tokens.append(val[:i_start])
                self.tokens.append(val[i_start:i_end+2])
                val = val[i_end + 2:]
            if val != '':
                self.tokens.append(val)
        self.obj_type = obj_type
        self.io_type = io_type
        self.value = value

    @property
    def is_const(self):
        """Flag indicating whether this is a constant component.

        Returns
        -------
        bool
        """
        return self.element_type == COMPONENT_TYPE_CONST

    @property
    def is_var(self):
        """Flag indicating whether this is a variable component.

        Returns
        -------
        bool
        """
        return self.element_type == COMPONENT_TYPE_VAR

    @property
    def ref_dir(self):
        """Flag indicating whether the component references a directory
        resource.

        Returns
        -------
        bool
        """
        return not self.io_type is None and self.io_type == IO_TYPE_DIR

    @property
    def ref_file(self):
        """Flag indicating whether the component references a file resource.

        Returns
        -------
        bool
        """
        return not self.io_type is None and self.io_type == IO_TYPE_FILE


    @property
    def refio(self):
        """Flag indicating whether the component references an IO resource.

        Returns
        -------
        bool
        """
        return not self.io_type is None
