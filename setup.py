import os
import sys
from setuptools import setup
import functools

_in_dir = functools.partial(os.path.join, os.path.dirname(__file__))

with open(_in_dir("crabsnack", "version.py")) as vf:
    exec(vf.read())
# ___________________________________


def readme():
    with open('README.rst', 'rb') as f:
        return f.read()
# ___________________________________

#         'flake8',
#         'coverage'


if sys.argv[-1] == 'test':
    test_requirements = [
        'pytest',
    ]
    try:
        modules = map(__import__, test_requirements)
    except ImportError as ie:
        errmsg = ie.message.replace("No module named ", "")
        msg = "%s is not installed. Install your test requirements." % errmsg
        raise ImportError(msg)
    os.system('pytest')
    sys.exit()
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
    author_email='mrkrabs@bottom.com',
    license='MIT',
    packages=['crabsnack'],
    zip_safe=False,
    install_requires=[
        'markdown',
    ]
)
