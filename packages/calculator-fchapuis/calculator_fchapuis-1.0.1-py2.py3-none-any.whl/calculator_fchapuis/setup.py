from setuptools import setup, find_packages

setup(
    name='calculator_fchapuis',
    version='1.0.1',
    packages=find_packages(),
    install_requires=[
        # List your dependencies here
    ],
    package_data={'': ['pyproject.toml']},
    author='Fabiano Chapuis',
    author_email='fabiano.chapuis@gmail.com',
)