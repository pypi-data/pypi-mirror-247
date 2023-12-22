"""
This module is a finalized version of the initial svcco package.
"""

from setuptools import setup, find_packages, Extension
from Cython.Build import cythonize
import numpy

extensions = [
    Extension('svtoolkit.domain.routines.c_allocate', ['svtoolkit/domain/routines/c_allocate.pyx'],
              include_dirs=[numpy.get_include()], language='c++')
]

__version__ = "0.0.24"

CLASSIFIERS = ['Intended Audience :: Science/Research',
               'License :: OSI Approved :: MIT License',
               'Programming Language :: Python',
               'Programming Language :: Python :: 3.7',
               'Programming Language :: Python :: 3.8',
               'Programming Language :: Python :: 3.9',
               'Topic :: Scientific/Engineering',
               'Operating System :: Microsoft :: Windows',
               'Operating System :: POSIX :: Linux',
               'Operating System :: POSIX',
               'Operating System :: Unix',
               'Operating System :: MacOS']

PACKAGES = find_packages(include=['svtoolkit', 'svtoolkit.*'])

setup_info = dict(
    name='svtoolkit',
    version=__version__,
    author='Zachary Sexton',
    author_email='zsexton@stanford.edu',
    license='MIT',
    python_requires='>=3.7',
    classifiers=CLASSIFIERS,
    packages=PACKAGES,
    ext_modules=cythonize(extensions, annotate=True),
    include_dirs=[numpy.get_include()],
    include_package_data=True,
    zip_safe=False
    )

setup(**setup_info)