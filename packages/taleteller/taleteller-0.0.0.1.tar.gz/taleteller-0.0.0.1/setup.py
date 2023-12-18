from setuptools import setup
from distutils.core import setup

setup(
    name='taleteller',
    version='0.0.0.1',
    author='AX',
    description='Send file to every node',
    packages=['taleteller'],
    entry_points={
        'console_scripts': [
            'taleteller = taleteller.main:main'
        ]
    },
    install_requires=['PyYAML'],
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
)
