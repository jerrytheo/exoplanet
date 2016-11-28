from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as readme:
    long_description = readme.read()

setup(
    name='ExoPlanet',
    version='1.0.0b1',
    description='Graphical User Interface for common Machine Learning applications',
    long_description=long_description,
    url='https://gitlab.com/jerrytheo96/exoplanet',
    author='Abhijit J. Theophilus, Mohinish L. Reddy',
    author_email='abhitheo96@gmail.com, mohinishlokesh96@gmail.com',
    license='GNU General Public License v3 (GPLv3)',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3.5',
        'Natural Language :: English',
    ],
    keywords='machine learning classification clustering regression',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    install_requires=['numpy', 'scipy', 'scikit-learn', 'matplotlib'],
    package_data={
        '': ['*.json', '*.png', '*.ico', '*.ttf', '*.txt', '*.qss'],
    }
)
