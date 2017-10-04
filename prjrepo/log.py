"""Logger for workflow commands."""

import json


class DefaultLogger(object):
    """Default logger appends each command as Json object to log file."""
    def __init__(self, filename):
        """Initialize the log file.

        Parameters
        ----------
        filename: string
            Path to the log file
        """
        self.filename = filename

    def lines(self):
        """Get list of command lines in the log file.

        Returns
        -------
        list(string)
        """
        lines = list()
        with open(self.filename, 'r') as f:
            for line in f:
                entry = json.loads(line)
                cmd = []
                cmd.append(entry['name'])
                for comp in entry['components']:
                    cmd.append(comp['value'])
                lines.append(' '.join(cmd))
        return lines

    def log(self, cmd, cmd_components):
        """Add log entry for executed command.

        Parameters
        ----------
        cmd: prjrepo.workflow.command.Command
            Specification of executed command
        cmd_components: list(string)
            Command line components
        """
        entry = dict()
        entry['name'] = cmd.name
        entry['components'] = []
        for i in range(len(cmd.components)):
            comp = dict()
            entry['components'].append(comp)
            comp['value'] = cmd_components[i]
            c = cmd.components[i]
            if c.ref_io:
                if c.ref_file:
                    comp['io'] = 'FILE'
                else:
                    comp['io'] = 'DIR'
                comp['input'] = str(c.as_input)
        with open(self.filename, 'a') as f:
            f.write(json.dumps(entry) + '\n')
