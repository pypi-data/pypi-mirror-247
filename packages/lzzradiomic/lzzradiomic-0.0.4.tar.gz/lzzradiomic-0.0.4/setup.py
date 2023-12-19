from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='lzzradiomic',
    version='0.0.4',
    license='MIT',
    author='lzz',
    description='A small example package',
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=['numpy','pyradiomics','pandas','scikit-learn','matplotlib','scipy','seaborn'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)