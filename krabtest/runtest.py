#!/usr/bin/env python


def test_crab_height(*, crab='Montenyo'):
    height = 10
    print("Crab {} height is {} cm".format(crab, height))
    assert height == 10


test_crab_height.name = 'crab_height'


def test_crab_width(crab):
    width = 18
    print("Crab {} width is {} cm".format(crab, width))
    assert width == 11


test_crab_width.name = 'crab_width'


def main():
    try:
        krab = 'mrkrabs'
        test_crab_height(crab=krab)
        print("Defaults: {}".format(test_crab_height.__kwdefaults__))
        print("Attrs: {}".format(test_crab_height.__code__))
        result = True
    except AssertionError as e:
        result = False

    print("Test {} finished with result {}".format(test_crab_height.name, result))


if __name__ == '__main__':
    main()
