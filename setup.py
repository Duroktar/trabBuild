from setuptools import setup

setup(
    name='trabBuild',
    version='0.1.0',
    packages=[''],
    url='',
    license='MIT',
    author='Scott Doucet',
    author_email='duroktar@gmail.com',
    description='A script for updating and building python dists',
    entry_points = {
        'console_scripts': [
            'trabbuild = trabbuild:main'
        ]
    }
)
