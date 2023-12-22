from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='ShortestPathSearch',
    version='0.1.0',
    author='huangwenkang',
    author_email='h13714156233k@yahoo.com',
    description='A Python tool to visualize and find the shortest path using OSMnx in specified locations.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/huangwenkang99/Shortest-Path-Search/tree/main',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.7",
    install_requires=[
        'osmnx',
        'networkx',
        'matplotlib',
        'scikit-learn'
    ],
    entry_points={
        'console_scripts': [
            "shortestpathsearch=shortestpathsearch.main:main",
        ],
    },

)
