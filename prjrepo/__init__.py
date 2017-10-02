"""Experiment Reposirty
"""

import os
import sys

# ------------------------------------------------------------------------------
# Global Constants
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
# Helper Methods
# ------------------------------------------------------------------------------

def get_base():
    """Get the path to the repository base directory. Not that the value in the
    BASE_FILE is a path expression that is relative to the working dorectory,
    not the REPO_DIR.

    Raises RuntimeError if the current directory does not contain a REPO_DIR.

    Returns
    -------
    string
    """
    filename = os.path.join(REPO_DIR, BASE_FILE)
    if not os.path.isfile(filename):
        raise RuntimeError('not a valid experiment repository')
    with open(filename, 'r') as f:
        return f.read().strip()
