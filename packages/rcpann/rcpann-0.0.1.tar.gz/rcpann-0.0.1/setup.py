from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.1'
DESCRIPTION = 'Ring Current Proton Artifician Neural Network Model'
LONG_DESCRIPTION = 'Composed by Jinxing Li et al. This is the ann model for ring current protons from 13 keV to 598 keV'

# Setting up
setup(
    name="rcpann",
    version=VERSION,
    author="Jinxing Li",
    author_email="<jinxing.li.87@gmail.com>",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'Ring Current', 'Space', 'Space physics', 'Radiation belt', 'magnetosphere'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
