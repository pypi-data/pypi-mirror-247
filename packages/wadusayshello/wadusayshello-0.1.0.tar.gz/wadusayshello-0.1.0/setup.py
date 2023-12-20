from setuptools import setup, find_packages

setup(
    name="wadusayshello",
    version="0.1.0",
    description="A test package made for an assignment that prints hello with your name",
    packages= find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3"
    ],
    python_requires=">=3.6",
)