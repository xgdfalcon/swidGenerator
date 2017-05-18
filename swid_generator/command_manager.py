
import os
import subprocess
from .exceptions import CommandManagerException
from .patches import py26_check_output


# Python 2.6 compatibility
if 'check_output' not in dir(subprocess):
    # Ugly monkey patching hack ahead
    # logging.debug('Monkey patching subprocess.check_output')
    subprocess.check_output = py26_check_output


def run_command(command_argumentlist, working_directory=os.getcwd()):
    """
    Executes a command. No output expected.
    :param command_argumentlist: Command-Arguments
    :param working_directory: The working directory of the command.
    """
    with open(os.devnull, 'w') as devnull:
        try:
            subprocess.call(command_argumentlist, stderr=devnull, cwd=working_directory)
        except Exception as e:
            raise CommandManagerException(e.message)


def run_command_check_output(command_argumentlist, stdin=None, working_directory=os.getcwd()):
    """
    Exectues a command. Output expected.
    :param command_argumentlist: Command-Arguments
    :param stdin: standard-input of the subprocess (e.x stdout from ohter subprocess)
    :param working_directory: Working directory of the command.
    :return: Console-Output of the command.
    """
    try:
        if stdin is None:
            output = subprocess.check_output(command_argumentlist, cwd=working_directory)
            if isinstance(output, bytes):
                output = output.decode('utf-8')
            return output
        else:
            subprocess.check_output(command_argumentlist, stdin=stdin, cwd=working_directory)
    except Exception as e:
        raise CommandManagerException(e.message)


def run_command_popen(command_argumentlist, stdout=None):
    """
    Runs a command with subprocess Library.
    :param command_argumentlist: Command arguments
    :param stdout: Standard output (e.x subprocess.PIPE)
    :return: Popen object to catch pipeline output
    """
    try:
        if stdout is not None:
            return subprocess.Popen(command_argumentlist, stdout=stdout)
        else:
            return subprocess.Popen(command_argumentlist)
    except Exception as e:
        raise CommandManagerException(e.message)
