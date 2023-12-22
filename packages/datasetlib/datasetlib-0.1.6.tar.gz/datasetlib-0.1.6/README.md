# Introduction 
a simple library having access to some often used datasets in pandas dataframe format

# Getting Started
There are two main functions in the module:
- getDataSetList() returns a list with all the available datasets
- getDataSet() returns a specific dataset identified by a name

# Build and Test
1. Build a package:
python3 -m pip install --upgrade build
python3 -m build

2. Upload the package to pypi.org
python3 -m pip install --upgrade twine
python3 -m twine upload --repository testpypi dist/*

3. Install the package 
python3 -m pip install -i https://test.pypi.org/simple/ basefunctions

# Contribute
If you have some interesting dataset that maybe should be added to this lib, please let me know

