
import re


def commands_from_sh(filename):
    """Parses an array job script for the individual per-processor commands

    The index of the commands in the returned list is exactly the same as
    the elements in the PBS submitter file

    Parameters
    ----------
    filename : str
        Name of the sh file created by qtools.Submitter

    Returns
    -------
    commands : list
        A 501-element list of all commands, in order of the commands from the
        file. For simplicity, the first element is 0 because BASH numbering
        starts at 1, so every item is accessible for each command using the
        same index as originally in the file.
    """

    # Up to 500 commands per submitted file for PBS
    commands = list(range(501))

    with open(filename) as f:
        for line in f:
            if line.startswith('cmd'):
                left, right = line.split('=')

                # Find the numbered index of the command
                matched = re.search('\[(\d+)\]', left)

                # Get the first item searched and turn it into an int
                index = int(matched.groups()[0])

                command = right.strip('""\n')

                commands[index] = command
    return commands
