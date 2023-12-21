'''Setup script to create the python AdHawk SDK
Usage:
To create the package, ensure all required files are in MANIFEST.in and run `python setup.py sdist`
pip install the resulting package and run adhawkdemo
'''

import setuptools

setuptools.setup(
    name='adhawk',
    version='6.0.1',
    description='AdHawk Microsystems SDK',
    url='http://www.adhawkmicrosystems.com/',
    author='AdHawk Microsystems',
    author_email='info@adhawkmicrosystems.com',
    packages=['adhawkapi', 'adhawkapi.frontend'],
    license="Proprietary",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    install_requires=[
        'numpy'
    ],
)