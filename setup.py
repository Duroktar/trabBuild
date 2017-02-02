from setuptools import setup


__version__ = '0.1.0'

setup(
    name='trabBuild',
    version=__version__,
    packages=['trabbuild'],
    license='MIT',
    author='Scott Doucet',
    author_email='duroktar@gmail.com',
    description='A script for updating and building python dists',
    entry_points={
        'console_scripts': [
            'trabbuild = trabbuild.__main__'
        ]
    }
)
