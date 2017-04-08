import os
from sphinx.websupport import WebSupport
CURDIR = os.path.dirname(os.path.abspath(__file__))


def main():
    print("Curdir: {}".format(CURDIR))
    support = WebSupport(
        srcdir=os.path.join(CURDIR, 'source'),
        builddir=os.path.join(CURDIR, 'builddoc')
    )

    support.build()
# _______________________________


if __name__ == '__main__':
    main()
