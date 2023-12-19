from setuptools import setup, find_packages
import setuptools

setup(
    name='azfuncextbase',
    version='0.1.1',
    author='Your Name',
    author_email='your.email@example.com',
    description='A short description of your package',
    package_dir={'': 'src'},
    packages=setuptools.find_packages(where='src'),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)