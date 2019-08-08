import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="selective_linter",
    version="0.0.1",
    author="Matt Boran",
    author_email="mattbo@zillowgroup.com",
    description="A script to be used as a pre-commit git hook for projects written in Swift",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="currently unknown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independant",
    ],
)