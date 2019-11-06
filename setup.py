#!/usr/bin/env python
# Future imports

from __future__ import absolute_import, division, print_function

import subprocess
from setuptools import setup, find_packages, Extension
import os
#import nose

eh_dir = os.path.join('.','cosmolopy','EH')

def generate_swig():
    cwd = os.path.abspath(os.path.dirname(__file__))
    print("Swigging sources")
    for d in ('power','tf_fit'):
        filename = os.path.join(cwd, 'cosmolopy', 'EH', d+'.i')        
        p = subprocess.call(['swig', '-python', filename],
                            cwd=cwd)
        if p != 0:
            raise RuntimeError("Running swig failed!")

generate_swig()

### I used to let distutils run swig for me on power.i to create
### power_wrap.c and power.py, but that stopped working for some
### reason.
# Stuff used to build the cosmolopy.EH._power module:
#power_module = Extension('cosmolopy.EH._power',
#                         sources=[os.path.join(eh_dir, 'power.i'),
#                                  os.path.join(eh_dir, 'power.c')]
#                         )
power_module = Extension('cosmolopy.EH._power',
                         sources=[os.path.join(eh_dir, 'power_wrap.c'),
                                  os.path.join(eh_dir, 'power.c')])

tf_fit_module = Extension('cosmolopy.EH._tf_fit',
                         sources=[os.path.join(eh_dir, 'tf_fit_wrap.c'),
                                  os.path.join(eh_dir, 'tf_fit.c')])

packages = find_packages()
setup(
    name = "cosmolopy",
    version = "0.4rc2",
    packages = packages,
#    package_data = {
#        # If any package contains *.so files, include them:
#        '': ['*.so'],
#        },
    install_requires = ['numpy', 'scipy',],

    ext_modules = [power_module, tf_fit_module],

    tests_require = ['nose', 'matplotlib'],
    test_suite = 'nose.collector',
    platforms=["Windows", "Linux", "Unix"],

    # metadata for upload to PyPI
    author = "Roban Hultman Kramer",
    author_email = "robanhk@gmail.com",
    description = "a cosmology package for Python.",
    url = "http://roban.github.com/CosmoloPy/",   # project home page
    keywords = ("astronomy cosmology cosmological distance density galaxy" +
                "luminosity magnitude reionization Press-Schechter Schecter"),
    license = "MIT",
    python_requires = ">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, <4",
    long_description = \
"""CosmoloPy is a package of cosmology routines built on NumPy/SciPy.

Capabilities include
--------------------

`cosmolopy.density`
  Various cosmological densities.

`cosmolopy.distance`
  Various cosmological distance measures.

`cosmolopy.luminosityfunction`
  Galaxy luminosity functions (Schecter functions).

`cosmolopy.magnitudes`
  Conversion in and out of the AB magnitude system.

`cosmolopy.parameters`
  Pre-defined sets of cosmological parameters (e.g. from WMAP).

`cosmolopy.perturbation`
  Perturbation theory and the power spectrum.

`cosmolopy.reionization`
  The reionization of the IGM.
  
""",
    classifiers = ['License :: OSI Approved :: MIT License',
                   'Programming Language :: Python',
                   'Programming Language :: Python :: 2.7',
                   'Programming Language :: Python :: 3.5',
                   'Programming Language :: Python :: 3.6',
                   'Programming Language :: Python :: 3.7',                   
                   'Programming Language :: Python :: 2',                   
                   'Programming Language :: Python :: 3',                   
                   'Topic :: Scientific/Engineering :: Astronomy',
                   'Operating System :: OS Independent'
                   ]
)
