from setuptools import setup, find_packages

setup(
    name='fchapuis_calculator_package',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        # List your dependencies here
    ],
    package_data={'': ['pyproject.toml']},
    author='Fabiano Chapuis',
    author_email='fabiano.chapuis@gmail.com',
)