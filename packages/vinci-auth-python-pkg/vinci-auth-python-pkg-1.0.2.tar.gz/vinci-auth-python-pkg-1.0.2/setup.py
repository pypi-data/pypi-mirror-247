import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="vinci-auth-python-pkg",
    version="1.0.2",
    author="Igor Lisbôa (TI-Sistemas)",
    author_email="ti-sistemas@vincipartners.com",
    description="A simple package to get vinci users auth token",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="http://tfs.util.vinci.net:8080/tfs/DefaultCollection/Vinci.Poc/Vinci.Poc%20Team/_git/vinci-auth-python-pkg",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)