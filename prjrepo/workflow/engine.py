"""Workflow command execution engine."""


from prjrepo.workflow.repository import DefaultCommandRepository


class WorkflowEngine(object):
    def __init__(self, logger):
        """Initialize the command logger.

        Parameters
        ----------
        logger: prjrepo.DefaultLogger
            Logger for successful executed commands.
        """
        self.logger = logger

    def run_command(self, context, cmd_name, default_values, print_only=False):
        """Run the registered command with given name. Provides the context for
        execution and a list of arguments that override context settings. The
        command repository is accessible via the context manager.

        Parameters
        ----------
        context: prjrepo.config.context.ContextManager
            Execution context
        cmd_name: string
            Command name
        default_values: dict
            List of arguments that are used as default values for variables that
            are not set in the given context
        print_only: bool, optional
            If True, will only print the generated command line to STDOUT but
            not execute anything.
        """
        # Get command specification. Will raise ValueError if command name is
        # unknown
        cmd = DefaultCommandRepository(context.cmd_dir).get_command(cmd_name)
        # Get context variables
        settings = context.context_settings()
        cmd_components = []
        for el in cmd.components:
            val = el.to_cmd_string(settings, default_values)
            if el.ref_io and el.as_input:
                val = context.locate_input_file(val, el.ref_file)
            cmd_components.append(val)
        # If print_ony is True output command line and we are done
        cmd_line = ' '.join(cmd_components)
        if print_only:
            print cmd_line
            return
        stdin, stdout, result = cmd.compute(cmd_line, settings)
        if result == 0:
            self.logger.log(cmd, cmd_components)
