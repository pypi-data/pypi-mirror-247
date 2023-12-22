import setuptools

VERSION = "0.6.1"

# read the contents of your README file
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(name='termite_toolkit',
                 version=VERSION,
                 description='scibite-toolkit - python library for calling TERMite, TExpress and other tools, and processing results',
                 url='https://github.com/elsevier-health/scibite-toolkit',
                 install_requires=[
                     "requests>=2.8.1",
                     "pandas>=0.23.4",
                     "nltk>=3.3.0"
                 ],
                 author='SciBite',
                 author_email='help@scibite.com',
                 long_description=long_description,
                 long_description_content_type='text/markdown',
                 license='Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License',
                 packages=setuptools.find_packages(),
                 classifiers=[
                     "Programming Language :: Python :: 3",
                     "Operating System :: OS Independent",
                 ],
                 data_files=[("", ["LICENSE.txt"])],
                 zip_safe=False)
