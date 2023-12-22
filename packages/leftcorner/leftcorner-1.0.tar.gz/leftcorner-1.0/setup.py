from setuptools import setup

setup(
    name='leftcorner',
    install_requires = [
        'numpy',
        'networkx',
        'nltk',
        'svgling',    # nltk uses svgling to draw derivations
        'tabulate',
        'dill',
        'pytest',
        'graphviz',   # for notebook visualization of left-recursion graph
        'path'
    ],
    authors = [
        'Andreas Opedal',
        'Eleftheria Tsipidi'
        'Tiago Pimentel',
        'Ryan Cotterell',
        'Tim Vieira',
    ],
    version='1.0',
    scripts=[],
    packages=['leftcorner'],
)
