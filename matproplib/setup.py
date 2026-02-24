from setuptools import setup, find_packages

setup(
    name="matproplib",
    version="0.1.0",
    author="Tyson",
    description="Aerospace material property database for rocket engine design",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=[
        "numpy>=1.20.0",
    ],
    python_requires=">=3.8",
)
