from setuptools import setup, find_packages

setup(
    name='classidgraph',
    version='0.5.1',
    author='Sasson Margaliot',
    author_email='sasson@live.com',
    description='A Python library for creating and managing directed graphs for natural language processing and deep learning projects.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/sasson/classidgraph',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pyyaml'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',
)
