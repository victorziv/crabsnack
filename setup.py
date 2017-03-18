"""
Pytest integration as suggested by Jeff Knupp in his sandman app.
!!!! Doesn't work for me.
"""
import os
import sys
from setuptools import setup
from setuptools.command.test import test as TestCommand
import functools

_in_dir = functools.partial(os.path.join, os.path.dirname(__file__))

with open(_in_dir("crabsnack", "version.py")) as vf:
    exec(vf.read())
# ___________________________________


def readme():
    with open('README.rst', 'rb') as f:
        return f.read()
# ___________________________________


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = ['--strict', '--verbose', '-tb=long', 'crabsnack/tests']

    def run_tests(self):
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)

# ___________________________________


setup(
    name='Crabsnack',
    version=__version__,  # noqa
    description='The best sea food in the world',
    long_description=readme(),

    classifiers=[
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
    ],

    cmdclass={'test': PyTest},
    include_package_data=True,
    url='http://github.com/victorziv/crabsnack',
    author='Eugene H. Krabs',
    author_email='mrkrabs@bottom.com',
    license='MIT',
    packages=['crabsnack'],
    zip_safe=False,
    install_requires=[
        'markdown',
    ],
    test_suite='crabsnack',
    test_require=['pytest'],
    extras_require={
        'testing': ['pytest']
    }
)
