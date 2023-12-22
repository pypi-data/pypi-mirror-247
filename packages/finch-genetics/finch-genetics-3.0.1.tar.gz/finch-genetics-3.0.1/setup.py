from setuptools import setup, find_packages

setup(
    name='finch-genetics',
    version='3.0.1',
    packages=find_packages(),
    install_requires=[
        "torch",
        "transformers",
        "diffusers",
        "numpy",
        "matplotlib",
        "typing_extensions"
    ],
)
