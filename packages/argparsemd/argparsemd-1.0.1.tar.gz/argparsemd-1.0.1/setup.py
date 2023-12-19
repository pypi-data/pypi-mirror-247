from setuptools import setup

from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="argparsemd",
    version="1.0.1",
    description="Add markdown help to ArgumentParser instances",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://varkenvarken.github.io/argparsemd/",
    author="varkenvarken",
    author_email="test@example.com",
    license="GPLv3",
    packages=["argparsemd"],
    python_requires=">=3.11",
    zip_safe=False,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
)