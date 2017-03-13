from setuptools import setup

setup(
    name='Crabsnack',
    version='0.1',
    packages=['cli'],
    include_package_data=True,
    install_requires=['click'],
    entry_points="""
        [console_scripts]
        factory=cli:cli
    """,
)
