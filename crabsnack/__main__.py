import sys
from crabsnack import create_app


def main(args=None):
    """ The main routine """
    if args is None:
        args = sys.argv[1:]

    print("Starting the crabsnack server")
    app = create_app()
    app.run()


if __name__ == '__main__':
    sys.exit(main())
