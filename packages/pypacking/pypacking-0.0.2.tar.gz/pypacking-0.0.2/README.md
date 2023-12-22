# PyPacking
## Use a short explanatory subtitle like, Create Python packages easily
<!-- Be sure to change `pypacking` for the name of your package -->

<!-- This are visual tags that you may add to your package at the beginning with useful information on your package --> 
[![version](https://img.shields.io/pypi/v/pypacking?color=blue)](https://pypi.org/project/pypacking/)
[![downloads](https://img.shields.io/pypi/dw/pypacking)](https://pypi.org/project/pypacking/)

`PyPacking` is a Python package template. It provides the minimal set of
files and functionalities to create and distribute a python package
using `PyPI`.  This `README` is one of the files you must provide with
the package. Change it according to the information you want to
provide the users.

To start a new package using this template follow this procedure (we
will assume that the name of your package is `mypack`):

- Get `pypacking` template: `git clone https://github.com/seap-udea/pypacking mypack`
- Remove the `.git` directory.
- Install system prerrequisites: `sudo apt install python3-pip gcc`
- Install python prerrequisites: `pip3 install build twine`
- Configure your package:
  - Change variables in `.packrc`.
  - Change key variables in setup file `setup.py`.
  - Change package prerrequisites in `pyroject.toml`.
  - Change package name in `src/__init__.py`
- Create an account in `PyPI` and get a token and place it in `$HOME/.pypirc`
- Release your first version: `make release VERSION=0.0.1`

Always start the README explaining clearly what your package do.  If
you can include here some beautiful image to call the attention of the
potential user do it!

This is an example:

<p align="center"><img src="https://drive.google.com/uc?export=view&id=1XWnQLEt_oBJjVzMLFVGEAm_uh4zmiYvC" alt="Logo""/></p>

## Download and install

Describe here how the package can be downloaded and install it in
different arquitectures.

If you are using `PyPI` installation it's as simple as:

```
pip install pypacking
```


## Quick start

In this section you should provide the most simple instructions to use
your package.

For instance:

```
import pypacking
print(pypacking.version)
```

## Code examples

Provide some detailed examples for more advanced users.

For instance:

```
import pypacking
obj = MyClass()
```

## What's new

If your package will be frequently updated with new features include a
section describing the new features added to it:

Version 0.0.*:

- First version of the package.

------------

This package has been designed and written by Fulanit@ de Tal (C) 202X