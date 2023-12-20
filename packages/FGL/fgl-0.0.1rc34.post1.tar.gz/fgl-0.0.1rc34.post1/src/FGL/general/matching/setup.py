from setuptools import setup
from setuptools.extension import Extension
from Cython.Build import cythonize
import numpy as np
import glob

# Specify the pattern for matching files
pattern = "FMM/src/*.c"

# Use glob to find all files matching the pattern
file_list = glob.glob(pattern)

ext_modules = [
    Extension(
        name="matching",
        sources=[
            "matching.pyx",
        ]+file_list,
        include_dirs = ['.',np.get_include(),'FMM/src'],
    )
]

if __name__ == "__main__":

    setup(
        ext_modules=cythonize(ext_modules)
    )