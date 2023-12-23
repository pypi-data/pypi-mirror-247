from embuild.helpers.run_process import run_process
from vt100logging import I


def check_for(cmd: str):
    try:
        run_process(f'{cmd} --version')
    except Exception as e:
        raise Exception(f"{cmd} is not installed: {e}")


def check_environment():
    I("Checking environment")
    check_for('git')
    check_for('cmake')
    check_for('ninja')
