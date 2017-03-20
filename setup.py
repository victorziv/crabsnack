import os
# import sys
from setuptools import setup
import functools

_in_dir = functools.partial(os.path.join, os.path.dirname(__file__))

with open(_in_dir("crabsnack", "version.py")) as vf:
    exec(vf.read())
# ___________________________________


def readme():
    with open('README.rst', 'r') as f:
        return f.read()
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

    include_package_data=True,
    url='http://github.com/victorziv/crabsnack',
    author='Eugene H. Krabs',
    author_email='mrkrabs@bottomup.com',
    license='MIT',
    packages=['crabsnack'],
    zip_safe=False,
    install_requires=[
        'markdown',
    ],
    tests_require=['pytest'],
    setup_requires=['pytest-runner'],
    entry_points={
        'console_scripts': [
            'crabtalks = crabsnack.command_line:main',
            'crab = crabsnack.__main__:main'
        ],
    }

)
