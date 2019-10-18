import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="selective_linter",
    version="1.0.1",
    author="Matt Boran",
    author_email="mattboran@gmail.com",
    description="A script to be run from Xcode to lint files as you make changes",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mattboran/SelectiveSwiftLinter",
    download_url="https://github.com/mattboran/SelectiveSwiftLinter/releases/download/1.0.1/selective_linter-1.0.1-py3-none-any.whl",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: MacOS :: MacOS X",
    ],
    install_requires=[
        'sh'
    ],
    python_requires='>3.0.0',
    entry_points = {
        'console_scripts': [
            'selective_linter = selective_linter.selective_linter:main'
        ]
    }
)
