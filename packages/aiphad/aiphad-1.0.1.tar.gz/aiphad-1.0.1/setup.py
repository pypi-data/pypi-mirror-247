from setuptools import setup, find_packages

setup(
    name='aiphad',
    version='1.0.1',
    author="AIPHAD developers",
    license="MIT",
    description='AIPHAD package',
    packages=["aiphad"],
    install_requires=[
    "matplotlib",
    "numpy",
    "physbo",
    "scikit-learn",
    "scipy"
    ]
)
