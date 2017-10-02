#!/home/heiko/.venv/prj/bin/python

import sys

import prjrepo as prj
import prjrepo.config as conf


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

  init                                 Initialize a new project repository

  context [--create] [<var> <value>]   List and set context variables
  project [<var> <value>]              List and set project variables

  log                                  Show execution history

  run <command-name> [<arguments>]     Run a registered script command
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
    if cmd_name == prj.CMD_INIT:
        # Initialize a new repository. Init does not take any further arguments.
        if len(args) == 1:
            conf.init_repository()
        else:
            print ' '.join(cmd_help)
    elif cmd_name == prj.CMD_CONTEXT:
        print ' '.join(cmd_help)
    elif cmd_name == prj.CMD_LOG:
        # Print the list of experiment script commands that have been run
        pass #cmd.print_log()
    elif cmd_name == prj.CMD_PROJECT:
        print ' '.join(cmd_help)
    elif cmd_name == prj.CMD_RUN:
        print ' '.join(cmd_help)
    elif cmd_name == '--help':
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
