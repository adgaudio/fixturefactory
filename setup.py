from setuptools import setup, find_packages
import os

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "fixturefactory",
    description = "Factory to generate Django model objects.  Easier than factoryboy and factorygirl",
    url = "git@github.com:adgaudio/fixturefactory.git",
    long_description=read('README'),
    version = "0.2",
    author = "Alex Gaudio",
    author_email = "adgaudio@gmail.com",
    keywords = "django factory fixture",

    install_requires = ['django'],

    py_modules=['fixturefactory'],
    #package_data = {'': ['*.md'] },
    #include_package_data=True,
    #package_data = {
        ## If any package contains *.txt or *.rst files, include them:
        #'': ['*.markdown', '*.txt', '*.rst'],
        ## And include any *.msg files found in the 'hello' package, too:
        ##'hello': ['*.msg'],
    #},
    #packages = find_packages(where='lib'),
    #package_dir = {"": "."},
    #scripts = ['say_hello.py'],
)
