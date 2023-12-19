import codecs
import os.path
import re

from setuptools import setup, find_packages

this_folder = os.path.abspath(os.path.dirname(__file__))
with codecs.open(os.path.join(this_folder, "dialog/__init__.py"), encoding="utf-8") as init_file:
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", init_file.read(), re.M)
    version_string = version_match.group(1)


setup(
    name="spitch",
    version=version_string,
    description="",
    long_description="Use the adapter framework to run any large model.",
    author="Babs Technologies",
    author_email="",
    url="https://github.com/Babs-Technologies/dialog",
    packages=find_packages(exclude=["tests"]),
    include_package_data=True,
    license="MIT",
    install_requires=[],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords="speech, voice, text",
)
