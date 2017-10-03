#!/home/heiko/.venv/prm/bin/python

import yaml
import sys

import prjrepo.config as conf
import prjrepo.config.context as cntxt


# ------------------------------------------------------------------------------
# Global Variables
# ------------------------------------------------------------------------------

"""Command names."""
# Manipulate local context
CMD_CONTEXT = 'context'
# Initialize the project repository
CMD_INIT = 'init'
# Command history
CMD_LOG = 'log'
# Run a script as part of an experiment
CMD_RUN = 'run'
# Manipulate project variables
CMD_PROJECT = 'project'


# ------------------------------------------------------------------------------
# API
# ------------------------------------------------------------------------------

def help(prg_name):
    """Print the default help statement containig a short description of the
    command line commands to manage project repositories.

    Paramaters
    ----------
    prg_name : string
        Name with which the program was called
    """
    return """Usage: """ + prg_name + """ <command> [<arguments>]

These are the commands for the project repository manager:

  init      Initialize a new project repository

  context   List and set context variables
            [--create [<var> <value>]]
            --delete <var>
            --delete-cascade <var>
  project   List and set project variables
            [<var> <value>]

  log       Show execution history

  run       Run a registered script command
            <command-name> [<arguments>]
"""


def main(prg_name, args):
    """Main routine to execute a repository command.

    Parameters
    ----------
    prg_name : string
        Name with which the program was called
    args: list(string)
        List of command line arguments
    """
    # The first argument is the command name
    cmd_name = args[0]
    cmd_help = ['usage:', prg_name, args[0]]
    if cmd_name == CMD_INIT:
        # Initialize a new repository. Init does not take any further arguments.
        if len(args) == 1:
            conf.init_repository()
        else:
            print ' '.join(cmd_help)
    elif cmd_name == CMD_CONTEXT:
        # Local context settings
        if len(args) == 1:
            # List context settings for current directory
            print yaml.dump(
                cntxt.ContextManager('.').context_settings().settings,
                default_flow_style=False
            )
        elif len(args) == 2 and args[-1] == '--create':
            # --create
            # Create an empty context in the current working directory
            cntxt.ContextManager('.').create_context()
        elif len(args) == 2:
            # <var>
            # Print variable value
            print cntxt.ContextManager('.').context_settings().get_value(args[1])
        elif len(args) == 3 and args[1] == '--delete':
            context = cntxt.ContextManager('.')
            context.context_settings().update_value(args[2], value=None)
        elif len(args) == 3 and args[1] == '--delete-cascade':
            context = cntxt.ContextManager('.')
            context.context_settings().update_value(args[2], value=None, cascade=True)
        elif len(args) == 3:
            context = cntxt.ContextManager('.')
            context.context_settings().update_value(args[1], value=args[2])
        elif len(args) == 4 and args[1] == '--create':
            context = cntxt.ContextManager('.')
            context.create_context()
            context.context_settings().update_value(args[2], value=args[3])
        else:
            cmd_help += [
                '[',
                '[--create] [<var> <value>]',
                '|',
                '--delete <var>',
                '|',
                '--delete-cascade <var>',
                ']'
            ]
            print ' '.join(cmd_help)
    elif cmd_name == CMD_LOG:
        # Print the list of experiment script commands that have been run
        if len(args) == 1:
            print_log()
        else:
            print ' '.join(cmd_help)
    elif cmd_name == CMD_PROJECT:
        # Global project settings
        if len(args) == 1:
            # List context settings for current directory
            print yaml.dump(
                cntxt.ContextManager('.').project_settings().settings,
                default_flow_style=False
            )
        elif len(args) == 3 and args[1] == '--delete':
            context = cntxt.ContextManager('.')
            context.project_settings().update_value(args[2], value=None)
        elif len(args) == 3:
            context = cntxt.ContextManager('.')
            context.project_settings().update_value(args[1], value=args[2])
        else:
            cmd_help += [
                '[',
                '<var> <value>',
                '|',
                '--delete <var>',
                ']'
            ]
            print ' '.join(cmd_help)
    elif cmd_name == CMD_RUN:
        print ' '.join(cmd_help)
    elif cmd_name == '--help':
        # Print help information
        print help(prg_name)
    else:
        print prg_name + ': \'' + cmd_name + '\' is not a ' + prg_name + ' command. See \'' + prg_name + ' --help.'


if __name__ == '__main__':
    # Extract the program name as the last component of the command path
    prg_name = sys.argv[0].split('/')[-1]
    if len(sys.argv) < 2:
        print help(prg_name)
        sys.exit(-1)
    else:
        try:
            main(prg_name, sys.argv[1:])
        except (ValueError, RuntimeError) as ex:
            print prg_name + ' (ERROR): ' + str(ex)
