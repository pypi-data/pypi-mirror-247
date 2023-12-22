# Introduction 
simple library to have some commonly used functions for everyday purpose 

# Getting Started
There are the following functionalities in this lib:
- filefunctions - some convienience functions for file handling

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
If you find a defect or suggest a new function, please let me know