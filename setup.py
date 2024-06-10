from setuptools import setup

setup(
    name='header-adder',
    version='1.0.0',
    description='Recursive header inserter for files in a directory tree',
    author='Ferenc Nandor Janky & Attila Gombos',
    author_email='info@effective-range.com',
    packages=['header_adder'],
    scripts=['bin/header-adder.py'],
    install_requires=['jinja2',
                      'python-context-logger@git+https://@github.com/EffectiveRange/python-context-logger.git@latest']
)
