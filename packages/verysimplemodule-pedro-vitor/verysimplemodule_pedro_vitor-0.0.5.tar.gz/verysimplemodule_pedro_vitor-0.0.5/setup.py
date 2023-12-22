from setuptools import setup, find_packages

VERSION = '0.0.5'
DESCRIPTION = 'My first Python packege'
LONG_DESCRIPTION = 'My first Python package with a sligthy longer description'

setup(
    name = "verysimplemodule_pedro_vitor",
    version = VERSION,
    author = "pedro vitor",
    author_email = "pedvitorpassos123@gmail.com",
    description = DESCRIPTION,
    long_description = LONG_DESCRIPTION,
    packages = find_packages(),
    install_requires = ['scikit-image', 'numpy'],
    keywords=['python', 'first package'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Operating System :: OS Independent",
    ]
) 