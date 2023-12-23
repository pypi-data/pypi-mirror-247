from vt100logging import vt100logging_initialize, I, E


def main():
    vt100logging_initialize('embuild')
    try:
        I("START")
        I("DONE")
    except Exception as e:
        E(e)
        exit(1)
