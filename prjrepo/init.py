"""Everything needed to initialize the repository."""

import prjrepo as prj
from exprepo.command import COMMAND_SPEC_SUFFIX
import json
import os
from shutil import copyfile


def create_repository():
    """Creating the repository directory in the current working directory.

    Raises RuntimeError if a repository directory already exists in the current
    working directory.
    """


def init_repository():
    """Initialize an experiment repository by creating the required folders
    and files.

    Raises RuntimeError if a repository directory already exists in the current
    working directory.
    """
    if os.path.isfile(REPO_DIR) or os.path.isdir(REPO_DIR):
        raise RuntimeError('existing repository detected')
    os.mkdir(REPO_DIR)
    os.mkdir(os.path.join(REPO_DIR, COMMAND_DIR))
    os.mkdir(os.path.join(REPO_DIR, CONTEXT_DIR))
    open('a.file', 'a').close()
