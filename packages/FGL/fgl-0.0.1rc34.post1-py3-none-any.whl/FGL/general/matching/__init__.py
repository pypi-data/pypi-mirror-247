import pyximport; pyximport.install()
from .matching import *
def __build():
    from setuptools import setup
    from setuptools.extension import Extension
    from Cython.Build import cythonize
    import numpy as np
    import os
    import glob

    cwd_bup = os.getcwd()

    try:
        modulePath = os.path.dirname(os.path.realpath(__file__))
        print("Building library '" + os.path.basename(modulePath) + "' ...")

        os.chdir(modulePath)

        sources = glob.glob('FMM/**/*.c', recursive=True)
        #print("   Sources:", sources)

        module1 = [
            Extension(
                name="matching",
                sources=[
                    "matching.pyx",
                ]+sources,
                include_dirs = ['.',np.get_include(),'FMM/src'],
            )
        ]

        setup(name='matching',
                ext_modules=cythonize(module1),
                script_args=["-q", "build_ext", "--inplace"])

    finally:
        os.chdir(cwd_bup)

#__build()

"""Python Package Template"""
__version__ = "0.0.1"