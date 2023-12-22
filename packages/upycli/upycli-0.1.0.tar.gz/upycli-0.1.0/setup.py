from setuptools import setup, find_packages

setup(
    name='upycli',
    version='0.1.0',
    packages=find_packages(),
    description='A microscopic library to turn any function into a CLI.',
    long_description=open('README.md', 'r').read(),
    long_description_content_type='text/markdown',
    entry_points = {
        'console_scripts': ['ucli=upycli.runner:run'],
    }
)
