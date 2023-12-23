from vt100logging import D
from subprocess import Popen, PIPE, DEVNULL, STDOUT
from os import getcwd
from embuild.helpers.verbosity import is_verbose


def run_process(cmd: str, cwd: str = getcwd()) -> str:
    """Run a process and return its output."""
    if is_verbose:
        D(f"Running: '{cmd}'")
    process = Popen(cmd, cwd=cwd, stdout=PIPE if is_verbose else DEVNULL,
                    stderr=STDOUT if is_verbose else DEVNULL, shell=True)
    output = process.communicate()[0]
    if process.returncode != 0:
        raise Exception(f"Failed to run: '{cmd}'")
    return output.decode('utf-8')
