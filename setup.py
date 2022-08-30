import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mypygui",                     # This is the name of the package
    version="0.0.4",                        # The initial release version
    author="Dragon-KK",                     # Full name of the author
    description="Render basic html in python",
    long_description=long_description,      # Long description read from the the readme file
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(where="./src"),    # List of all python modules to be installed
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],                                      # Information to filter the project on PyPi website
    python_requires='>=3.10',                # Minimum version requirement of the package
    py_modules=[],             # Name of the python package
    license="LICENSE",
    package_dir={'':'src'},     # Directory of the source code of the package
    keywords=["html", "tkinter"],
    install_requires=[
        "pillow >= 9.1.0",
        "tinycss2 >= 1.1.1",
        "webcolors >= 1.12"
    ]                    # Install other dependencies if any
)