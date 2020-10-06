import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="MegaLiveInstantActionPlotterDeluxe",
    version="0.0.1",
    author="Jakob Weimar",
    author_email="jakob.weimar@gmx.de",
    description="A small python liveplotter using PyQtGraph",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/JakobWe/MegaLiveInstantActionPlotterDeluxe",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "pyqtgraph>=0.10.0",
    ],
    python_requires='>=3.6',
)