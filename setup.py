from setuptools import setup

setup(
    name='Crabsnack',
    version='0.1',
    description='The best sea food in the world',
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
