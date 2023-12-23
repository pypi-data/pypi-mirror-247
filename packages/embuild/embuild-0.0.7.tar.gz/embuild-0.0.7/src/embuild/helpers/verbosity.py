VERBOSITY: bool = False


def set_verbosity(is_verbose: bool) -> None:
    global VERBOSITY
    VERBOSITY = is_verbose


def is_verbose() -> bool:
    return VERBOSITY
