from setuptools import setup,Extension
from pybind11.setup_helpers import Pybind11Extension

ext_modules=[
    Pybind11Extension("indicator",["indicator.cpp"])
]

setup (
    name="indicator",
    version="0.1",
    ext_modules=ext_modules
)
