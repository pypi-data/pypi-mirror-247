from vt100logging import vt100logging_init, I, E
from helpers.check_environment import check_environment


def main():
    vt100logging_init('embuild')
    try:
        I("START")
        check_environment()
        I("DONE")
    except Exception as e:
        E(e)
        exit(1)


if __name__ == '__main__':
    main()
