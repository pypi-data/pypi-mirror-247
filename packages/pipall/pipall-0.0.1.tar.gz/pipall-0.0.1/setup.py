# setup.py
from setuptools import setup

setup(
    name='pipall',
    version='0.1',
    packages=['src.pipall'],
    entry_points={
        'console_scripts': [
            'pipall=pipall.installer:main',
        ],
    },
)
