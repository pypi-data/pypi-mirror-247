from vt100logging import vt100logging_init, I, E


def main():
    vt100logging_init('embuild')
    try:
        I("START")
        I("DONE")
    except Exception as e:
        E(e)
        exit(1)
