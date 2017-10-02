"""Everything related to configuration settings."""

import os
import yaml

import exprepo as exp


# ------------------------------------------------------------------------------
# Classes
# ------------------------------------------------------------------------------

class Config(object):
    """Object excapsulating the dictionary containing repository settings."""
    def __init__(self, settings, defaults=None):
        """Initialize the settings dictionary from the given dictionary and an
        optional dictionary containing default values.

        Parameters
        ----------
        settings: dict
            Dictionary of settings
        defaults: dict, optional
            Dictionary of default settings
        """
        if not defaults is None:
            self.settings = nested_merge(defaults.copy(), settings)
        else:
            self.settings = settings

    def get_value(self, para):
        """Return the value that is associated with the given parameter. The
        parameter expression can be a path expression.

        Raises ValueError if the specified parameter does not exist or if it
        references an internal dictionary in the nested settings dictionary.

        Parameters
        ----------
        para: string
            Configuration parameter expression

        Returns
        -------
        string
        """
        el = self.settings
        for comp in para.split('/'):
            if isinstance(el, dict):
                if comp in el:
                    el = el[comp]
                else:
                    raise ValueError('unknown parameter \'' + para + '\'')
            else:
                raise ValueError('cannot get value of \'' + para + '\'')
        if not isinstance(el, dict):
            return el
        else:
            raise ValueError('cannot get value of \'' + para + '\'')

    def print_values(self):
        """Print the current state of the settings dictionary. Output is in Yaml
        format.
        """
        print yaml.dump(self.settings, default_flow_style=False)

    def update_value(self, para, value=None):
        """Update the value of a configuration parameter. The para argument may
        contain a path expression. In this case all nested elements along the
        path are created if necessary.

        If the given value is None the parameter will be deleted.

        Raises ValueError if an invalid parameter name is given or if an
        existing text element is referenced as part of a path expression.

        Parameters
        ----------
        para: string
            Parameter path
        value: string, optional
            New parameter value or None (indicating delete)
        """
        # Remove potential starting and trailing '/'
        if para.startswith('/'):
            para = para[1:]
        if para.endswith('/'):
            para = para[:-1]
        path = para.split('/')
        key = path[-1].strip()
        if key == '':
            raise ValueError('invalid parameter name \'' + para + '\'')
        # Find the element that is referenced by the path prefix. Create elements
        # along the path if necessary
        el = self.settings
        for comp in path[:-1]:
            if not comp in el:
                el[comp] = dict()
            el = el[comp]
            if not isinstance(el, dict):
                raise ValueError('cannot create element under text value \'' + el + '\'')
        # Update the parameter value in the target element or delete the element if
        # the given value is None
        if not value is None:
            el[key] = str(value)
        else:
            del el[key]

    def write(self, filename):
        """Write a configuration dictionary to the given file.

        Parameters
        ----------
        filename: string
            Path for the output file
        """
        with open(filename, 'w') as f:
            yaml.dump(self.settings, f, default_flow_style=False)



# ------------------------------------------------------------------------------
# API Methods
# ------------------------------------------------------------------------------

def get_global_variables():
    """Get current state of the global variables. This will read the GLOBAL file
    in the base directory.

    Returns
    -------
    Config
    """
    return Config(read_yaml_file(get_global_variables_file()))


def get_settings(include_defaults=True):
    """Get current repository settings. This will read the settings file in the
    current working directory. By default, the settings from the repositories
    base directory are included as default values.

    Parameters
    ----------
    include_defaults: bool
        Flag indicating whether settings from the repositories base directory
        are included as default values.

    Returns
    -------
    Config
    """
    if include_defaults:
        filename =  get_settings_file(base_dir=exp.get_base())
        config = read_yaml_file(filename)
        # Only read local settings if this repository is a clone
        local_filename = get_settings_file()
        if os.path.abspath(filename) != os.path.abspath(local_filename):
            return Config(read_yaml_file(local_filename), defaults=config)
        else:
            return Config(config)
    else:
        return Config(read_yaml_file(get_settings_file()))


def print_global_variables():
    """Print the current state of the global variables."""
    get_global_variables().print_values()


def print_settings():
    """Print the current settings."""
    get_settings().print_values()


def update_global_variables(para, value=None):
    """Update the value of a global variable. The para argument may
    contain a path expression. In this case all nested elements along the path
    are created if necessary.

    If the given value is None the variable will be deleted.

    Raises ValueError if an invalid parameter name is given or if an existing
    text element is referenced as part of a path expression.

    Parameters
    ----------
    para: string
        Parameter path
    value: string, optional
        New variable value or None (indicating delete)
    """
    variables = get_global_variables()
    variables.update_value(para, value=value)
    variables.write(get_global_variables_file())


def update_settings(para, value=None):
    """Update the value of a configuration parameter. The para argument may
    contain a path expression. In this case all nested elements along the path
    are created if necessary.

    If the given value is None the parameter will be deleted.

    Raises ValueError if an invalid parameter name is given or if an existing
    text element is referenced as part of a path expression.

    Parameters
    ----------
    para: string
        Parameter path
    value: string, optional
        New parameter value or None (indicating delete)
    """
    # Make sure to only read the local settings file
    config = get_settings(include_defaults=False)
    config.update_value(para, value=value)
    config.write(get_settings_file())


# ------------------------------------------------------------------------------
# Helper Methods
# ------------------------------------------------------------------------------

def get_global_variables_file():
    """Return the file name of the default settings file. Allows to specify a
    base directory other than the current wirking directory.

    Parameters
    ----------
    base_dir: string, optional
        Base directory where the repository directory is expected. Use current
        working directory as default.

    Returns
    -------
    string
    """
    return os.path.join(exp.get_base(), exp.REPO_DIR, exp.GLOBAL_VARIABLES_FILE)


def get_settings_file(base_dir=None):
    """Return the file name of the default settings file. Allows to specify a
    base directory other than the current wirking directory.

    Parameters
    ----------
    base_dir: string, optional
        Base directory where the repository directory is expected. Use current
        working directory as default.

    Returns
    -------
    string
    """
    if not base_dir is None:
        return os.path.join(base_dir, exp.REPO_DIR, exp.SETTINGS_FILE)
    else:
        return os.path.join(exp.REPO_DIR, exp.SETTINGS_FILE)


def nested_merge(d1, d2):
    """Merge two dictionaries such that d1 will contain all the values from d2.

    Parameters
    ----------
    d1: dict
        Dictionary into which the second dictionary is merged
    d2: dict
        Dictionary of values that are merged into the first dictionary.

    Returns
    -------
    dict
    """
    for key in d2:
        if not key in d1:
            d1[key] = d2[key]
        elif isinstance(d1[key], dict) and isinstance(d2[key], dict):
            d1[key] = nested_merge(d1[key], d2[key])
        else:
            d1[key] = d2[key]
    return d1


def read_yaml_file(filename):
    """Read settings from the given file. Expets the file content to be in Yaml
    format. Returns an empty dictionary if the file does not exist.

    Parameters
    ----------
    filename: string
        Path to the input Yaml file

    Returns
    -------
    dict
    """
    # Read the settings file if it exist. Otherwise return an empty dictionary.
    if os.path.isfile(filename):
        with open(filename, 'r') as f:
            return yaml.load(f.read())
    else:
        return dict()
