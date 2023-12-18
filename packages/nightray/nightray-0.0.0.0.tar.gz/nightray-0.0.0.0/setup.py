from setuptools import setup
from distutils.core import setup

setup(
    name='nightray',
    version='0.0.0.0',
    author='AX',
    description='Find keywords in files',
    packages=['nightray'],
    entry_points={
        'console_scripts': [
            'nightray = nightray.main:main'
        ]
    },
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
)
