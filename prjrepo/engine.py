"""Workflow command execution engine."""


class WorkflowEngine(object):
    def run_command(self, context, cmd_name, args):
        """Run the registered command with given name. Provides the context for
        execution and a list of arguments that override context settings. The
        command repository is accessible via the context manager.

        Parameters
        ----------
        context: prjrepo.config.context.ContextManager
            Execution context
        cmd_name: string
            Command name
        args: dict
            List of arguments that overrie context settings
        """
        # Get command specification. Will raise ValueError if command name is
        # unknown
        cmd = context.commands().get_command(cmd_name)
        # Get context variables
        settings = context.context_settings()
        for el in cmd.elements:
            

def run_command(prg_name, name, args, run_local=True):
    """Run the experiment script with the given name. Constructs the command
    to run the script from the current configuration settings and optional
    arguments that overwrite these settings. The script is only execute if the
    run local flag is True.

    Raises ValueError if the specified command is unknown or if the provided
    arguments are of invalid format.

    Parameters
    ----------
    name: string
        Name of the script that is being run_command
    args: list(string)
        Arguments that override the current configurations ettings (expected
        format is <key>=<value>)
    run_local: bool, optional
        Flag indicating whether to actuall execute the script or only print
        and log the command line command for submission on a remote machine.
    """
    commands = get_commands()
    if not name in commands:
        raise ValueError('unknown command \'' + name + '\'')
    # Get a dictionary of arguments that override the configuration settings
    local_args = dict()
    for arg in args:
        pos = arg.find('=')
        if pos < 0:
            raise ValueError('invalid argument \'' + arg + '\'')
        local_args[arg[:pos]] = arg[pos+1:]
    # Read the current experiment configuration settings and global variables
    config = get_settings()
    variables = get_global_variables()
    # Create the list of command components
    cmd = []
    for obj in commands[name]:
        val = None
        if obj.is_var:
            if obj.value in local_args:
                val = local_args[obj.value]
            else:
                val = config.get_value(obj.value)
        else:
            val = obj.value
        # Replace occurrences of variable names in val
        if '@(' in val:
            pos = val.find('@(')
            while pos >= 0:
                end_pos = val.find(')', pos)
                if end_pos < 0:
                    raise ValueError('invalid expression \'' + val + '\'')
                var_value = variables.get_value(val[pos+2:end_pos].strip())
                val = val[:pos] + var_value + val[end_pos + 1:]
                pos = val.find('@(')
        cmd.append(val)
    # Run the command if run local flag is True
    if run_local:
        print prg_name + ' (RUN): ' + ' '.join(cmd)
        result = subprocess.call(cmd)
        # Add command to log if successfule (i.e., result is 0)
        if result == 0:
            with open(get_log_file(), 'a') as f:
                f.write(' '.join(cmd) + '\n')
    else:
        print prg_name + ' (SUBMIT): ' + ' '.join(cmd)
        with open(get_log_file(), 'a') as f:
            f.write('*' + ' '.join(cmd) + '\n')
