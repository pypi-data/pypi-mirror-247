from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name='finch-genetics',
    version='3.0.3',
    packages=find_packages(),
    install_requires=[
        "torch",
        "transformers",
        "diffusers",
        "numpy",
        "matplotlib",
        "typing_extensions"
    ],
    author='Daniel Losey',
    author_email='danieljlosey@gmail.com',
    description='GPU and CPU modular genetic algorithm framework.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/dadukhankevin/Finch',
    classifiers=[
        'Programming Language :: Python :: 3',
        # Add other classifiers as needed
    ],
)
