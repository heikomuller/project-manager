"""Objects representing commands that can be executed as part of a project ."""


# ------------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------------

"""Type of components in a command specification."""
COMMAND_ELEMENT_CONST = 'CONST'
COMMAND_ELEMENT_VAR = 'VAR'
COMMAND_ELEMENT_TYPES = [COMMAND_ELEMENT_CONST, COMMAND_ELEMENT_VAR]

"""Type identifier for executable commands."""
COMMAND_TYPE_EXEC = 'EXEC'
COMMAND_TYPE_SQL = 'SQL'
COMMAND_TYPES = [COMMAND_TYPE_EXEC, COMMAND_TYPE_SQL]

"""Variable types."""
VARIABLE_TYPE_DIR = 'DIR'
VARIABLE_TYPE_FILE = 'FILE'
VARIABLE_TYPE_VALUE = 'VAL'
VARIABLE_TYPES = [VARIABLE_TYPE_DIR, VARIABLE_TYPE_FILE, VARIABLE_TYPE_VALUE]
VARIABLE_IO_TYPES = [VARIABLE_TYPE_DIR, VARIABLE_TYPE_FILE]

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
        elements: list(CommandElement)
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
        elements: list(CommandElement)
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
        elements: list(CommandElement)
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


class CommandElement(object):
    """Component in the specification of an executable command. Command elements
    are either constant values or references to variables.
    """
    def __init__(self, element_type, value):
        """Initialize the element type and value.

        Raises ValueError if an invalid element type is given. Valid type
        identifier are defined in COMMAND_ELEMENT_TYPES.

        Parameters
        ----------
        element_type: string
            Unique identifier of the element type
        value: string
            Element value
        """
        if not element_type in COMMAND_ELEMENT_TYPES:
            raise ValueError('invalid element type \'' + element_type + '\'')
        self.element_type = element_type
        self.value = value

    @property
    def is_const(self):
        """Flag indicating whther this is a constant element.

        Returns
        -------
        bool
        """
        return self.element_type == COMMAND_ELEMENT_CONST

    @property
    def is_var(self):
        """Flag indicating whther this is a variable element.

        Returns
        -------
        bool
        """
        return self.element_type == COMMAND_ELEMENT_VAR


class ConstantElement(CommandElement):
    """Constant command element."""
    def __init__(self, value):
        """Initialize the element value.

        Parameters
        ----------
        value: string
            Element value
        """
        super(ConstantElement, self).__init__(COMMAND_ELEMENT_CONST, value)


class VariableElement(CommandElement):
    """Command element referencing a variable value. Variable elements further
    specify the type of the variable value they are referencing: VAL or IO.

    If the variable type is IO the variable value is expected to either
    reference a file or directory on disk. Furthermore, if the value is
    designated as an input to the command the system will search for the
    referenced file/directory along the project/database/experiment path.
    """
    def __init__(self, variable_type, variable_name):
        """Initialize variable type and name

        Raises ValueError if an invalid variable type is specified. Valid
        variable types are defined in VARIABLE_TYPES.

        Parameters
        ----------
        variable_type: string
            Unique variable type identifier
        variable_name: string
            Path expression referencing the variable name
        """
        if not variable_type in VARIABLE_TYPES:
            raise ValueError('invalid variable type \'' + variable_type + '\'')
        super(VariableElement, self).__init__(
            COMMAND_ELEMENT_VAR,
            variable_name
        )
        self.variable_type = variable_type

    @property
    def name(self):
        """The vaiable name is stored in the element value."""
        return self.value


class VariableIOElement(VariableElement):
    """Command element that references a file or directory. It is exoected that
    references to file system resources are relative paths. If the value is used
    as input to a command the system will search for an existing file/directory
    with the given name along the search pato of experiment, database, and
    project directory.
    """
    def __init__(self, variable_type, variable_name, is_input=False):
        """Initialize variable type, name, and input flag.

        Raises ValueError if an invalid IO variable type is specified. Valid
        variable types are defined in VARIABLE_IO_TYPES.

        Parameters
        ----------
        variable_type: string
            Unique variable type identifier
        variable_name: string
            Path expression referencing the variable name
        is_input: bool
            Flag indocating whether the variable value references a file/dir
            that is used as input by the executed program.
        """
        if not variable_type in VARIABLE_IO_TYPES:
            raise ValueError('invalid variable type \'' + variable_type + '\'')
        super(VariableIOElement, self).__init__(variable_type, variable_name)
        self.is_input = is_input
